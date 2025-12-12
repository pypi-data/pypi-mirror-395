from __future__ import annotations

import json
import mimetypes
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import httpx
import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from .api_client import APIClient
from .config import env_bool
from .pgvector_probe import PgvectorProbeError, wait_for_vectors
from .state import UploadStateStore


app = typer.Typer(help="Ingestion helpers including bulk upload flows.")
console = Console()


@dataclass
class UploadResult:
    path: Path
    job_id: Optional[str] = None
    document_id: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    size_bytes: Optional[int] = None


def _get_ctx(ctx: typer.Context):
    from .cli import (
        AppContext,
        _ensure_authenticated,
    )  # Local import to avoid circular deps

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)

    _ensure_authenticated(ctx.obj)
    return ctx.obj  # type: ignore[return-value]


def _resolve_project(profile, override: Optional[str]) -> str:
    project = override or profile.default_project
    if not project:
        console.print(
            "[red]Project is required. Pass --project or set default_project on the active profile.[/red]"
        )
        raise typer.Exit(code=1)
    return project


def _prepare_metadata(raw: Optional[str]) -> Optional[Dict[str, object]]:
    if not raw:
        return None
    try:
        metadata = json.loads(raw)
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a JSON object")
        return metadata
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"Invalid metadata JSON: {exc}") from exc


def _upload_file(
    client: APIClient,
    path: Path,
    project_id: str,
    *,
    agent_id: Optional[str] = None,
    wait: bool = False,
    metadata: Optional[Dict[str, object]] = None,
    timeout: float = 90.0,
) -> UploadResult:
    result = UploadResult(path=path)
    url = client.base_url.rstrip("/") + "/api/v4/ingest"

    data: Dict[str, str] = {"project_id": project_id}
    if agent_id:
        data["agent_id"] = agent_id
    if wait:
        data["wait"] = "true"
    if metadata:
        data["metadata"] = json.dumps(metadata)

    mimetype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    headers = client._build_headers()  # type: ignore[attr-defined]
    start = time.perf_counter()

    with path.open("rb") as fp, httpx.Client(timeout=timeout) as http:
        response = http.post(
            url,
            data=data,
            files={"file": (path.name, fp, mimetype)},
            headers=headers,
        )

    duration_ms = int((time.perf_counter() - start) * 1000)
    result.duration_ms = duration_ms
    try:
        result.size_bytes = path.stat().st_size
    except OSError:
        result.size_bytes = None

    if response.status_code >= 400:
        try:
            payload = response.json()
            message = payload.get("message") or response.text
        except json.JSONDecodeError:
            message = response.text
        result.error = message or f"HTTP {response.status_code}"
        return result

    payload = response.json()
    result.job_id = payload.get("job_id")
    result.document_id = payload.get("document_id")
    result.status = payload.get("status", "pending")
    return result


def _format_size_bytes(size: Optional[int]) -> str:
    if not size:
        return "-"
    mb = size / (1024 * 1024)
    return f"{mb:.2f}"


def _log_upload_result(result: UploadResult) -> None:
    size = _format_size_bytes(result.size_bytes)
    duration = f"{result.duration_ms or 0} ms"
    if result.error:
        console.log(
            f"[red]FAILED[/red] {result.path.name} ({size} MB, {duration}) → {result.error}"
        )
    else:
        job = result.job_id or "-"
        console.log(
            f"[green]Uploaded[/green] {result.path.name} ({size} MB, {duration}) [job: {job}]"
        )


def _render_summary(results: Sequence[UploadResult]) -> None:
    table = Table(show_header=True, header_style="bold")
    table.add_column("File")
    table.add_column("Job ID")
    table.add_column("Document ID")
    table.add_column("Status")
    table.add_column("Size (MB)", justify="right")
    table.add_column("Duration (ms)", justify="right")
    table.add_column("Message")

    for res in results:
        table.add_row(
            res.path.name,
            res.job_id or "-",
            res.document_id or "-",
            "[red]failed[/red]" if res.error else res.status,
            _format_size_bytes(res.size_bytes),
            str(res.duration_ms or "-"),
            res.error or "",
        )

    console.print(table)


def _iter_files(source: Path, recursive: bool, pattern: Optional[str]) -> List[Path]:
    if source.is_file():
        return [source]
    if not source.is_dir():
        raise typer.BadParameter(f"{source} is not a file or directory")

    glob_pattern = pattern or "*"
    iterator = source.rglob(glob_pattern) if recursive else source.glob(glob_pattern)
    return [p for p in iterator if p.is_file()]


def _run_parallel_uploads(
    files: Sequence[Path],
    worker_fn,
    max_workers: int,
    *,
    state_store: Optional[UploadStateStore] = None,
) -> List[UploadResult]:
    pending: List[Path] = []
    for file_path in files:
        if state_store and state_store.should_skip(file_path):
            console.print(
                f"[cyan]Skipping {file_path} (already marked as uploaded)[/cyan]"
            )
            continue
        pending.append(file_path)

    if not pending:
        console.print(
            "[yellow]No files to upload (all skipped or none matched)[/yellow]"
        )
        return []

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        transient=False,
    )

    results: List[UploadResult] = []
    task_id = progress.add_task("Uploading", total=len(pending))

    with progress:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {executor.submit(worker_fn, path): path for path in pending}
            for future in as_completed(future_map):
                res = future.result()
                if state_store:
                    state_store.record(res)
                _log_upload_result(res)
                results.append(res)
                progress.update(task_id, advance=1)

    return results


def _maybe_verify_vectors(
    results: Sequence[UploadResult],
    *,
    enabled_flag: bool,
    pg_dsn: Optional[str],
    min_rows: int = 1,
    timeout: float = 30.0,
    poll_interval: float = 2.0,
) -> None:
    should_verify = enabled_flag or env_bool("DOCLAYER_VERIFY_PGVECTOR", False)
    if not should_verify:
        return

    dsn = pg_dsn or os.getenv("DOCLAYER_PG_DSN")
    if not dsn:
        console.print(
            "[yellow]Skipping pgvector verification (no DSN provided)[/yellow]"
        )
        return

    docs = [res.document_id for res in results if res.document_id and not res.error]
    if not docs:
        console.print("[yellow]No successful document IDs to verify[/yellow]")
        return

    console.print(
        f"[cyan]Verifying {len(docs)} document(s) exist in chunk_vectors (timeout={timeout}s)...[/cyan]"
    )

    try:
        counts = wait_for_vectors(
            docs, dsn, min_rows=min_rows, timeout=timeout, poll_interval=poll_interval
        )
    except PgvectorProbeError as exc:
        console.print(f"[red]pgvector verification failed: {exc}[/red]")
        raise typer.Exit(code=1) from exc

    missing = [doc_id for doc_id in docs if counts.get(doc_id, 0) < min_rows]
    if missing:
        console.print(
            f"[red]pgvector verification failed for {len(missing)} document(s): {', '.join(missing)}[/red]"
        )
        raise typer.Exit(code=1)

    console.print("[green]✓ pgvector entries detected for all documents[/green]")


@app.command("file")
def ingest_file(
    ctx: typer.Context,
    file: Path = typer.Argument(..., exists=True, readable=True, resolve_path=True),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Project ID"),
    agent: Optional[str] = typer.Option(
        None, "--agent", "-a", help="Agent ID to process with"
    ),
    wait: bool = typer.Option(False, "--wait", help="Wait for processing completion"),
    metadata: Optional[str] = typer.Option(
        None,
        "--metadata",
        help="Inline JSON metadata to attach to the ingestion job",
    ),
    verify_vectors: bool = typer.Option(
        False,
        "--verify-vectors/--no-verify-vectors",
        help="Block until chunk_vectors rows exist for the uploaded document",
    ),
    pg_dsn: Optional[str] = typer.Option(
        None,
        "--pg-dsn",
        help="Postgres DSN used for pgvector verification (defaults to DOCLAYER_PG_DSN)",
    ),
    pg_timeout: float = typer.Option(
        30.0, "--pg-timeout", help="Max seconds to wait for pgvector rows"
    ),
    pg_poll: float = typer.Option(
        2.0, "--pg-poll-interval", help="Polling interval in seconds"
    ),
) -> None:
    """Upload a single file through the ingest gateway."""
    app_ctx = _get_ctx(ctx)
    project_id = _resolve_project(app_ctx.profile, project)
    parsed_metadata = _prepare_metadata(metadata)

    result = _upload_file(
        app_ctx.client,
        file,
        project_id,
        agent_id=agent,
        wait=wait,
        metadata=parsed_metadata,
    )

    _render_summary([result])

    if result.error:
        raise typer.Exit(code=1)

    _maybe_verify_vectors(
        [result],
        enabled_flag=verify_vectors,
        pg_dsn=pg_dsn,
        timeout=pg_timeout,
        poll_interval=pg_poll,
    )


@app.command("batch")
def ingest_batch(
    ctx: typer.Context,
    path: Path = typer.Argument(
        ..., exists=True, resolve_path=True, help="File or directory to ingest"
    ),
    project: Optional[str] = typer.Option(
        None, "--project", "-p", help="Project ID (defaults to profile)"
    ),
    agent: Optional[str] = typer.Option(
        None, "--agent", "-a", help="Agent ID to process with"
    ),
    workers: int = typer.Option(
        4, "--workers", "-w", min=1, max=32, help="Concurrent uploads"
    ),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Include subdirectories"
    ),
    pattern: Optional[str] = typer.Option(
        None, "--pattern", "-g", help="Glob pattern filter (e.g. *.pdf)"
    ),
    throttle: float = typer.Option(
        0.0,
        "--throttle",
        help="Seconds to sleep between uploads (per worker) to avoid rate limits",
    ),
    metadata: Optional[str] = typer.Option(
        None,
        "--metadata",
        help="Inline JSON metadata applied to every file",
    ),
    verify_vectors: bool = typer.Option(
        False,
        "--verify-vectors/--no-verify-vectors",
        help="Block until chunk_vectors rows exist for all uploaded documents",
    ),
    pg_dsn: Optional[str] = typer.Option(
        None,
        "--pg-dsn",
        help="Postgres DSN used for pgvector verification (defaults to DOCLAYER_PG_DSN)",
    ),
    pg_timeout: float = typer.Option(
        60.0, "--pg-timeout", help="Max seconds to wait for pgvector rows"
    ),
    pg_poll: float = typer.Option(
        2.0, "--pg-poll-interval", help="Polling interval in seconds"
    ),
    state_file: Optional[Path] = typer.Option(
        None,
        "--state-file",
        help="Path to a JSON file that tracks upload progress for resume/retry workflows",
    ),
    resume: bool = typer.Option(
        False,
        "--resume/--no-resume",
        help="Skip files already marked as successful in --state-file",
    ),
) -> None:
    """Upload every matching file inside a directory."""
    # Validate --resume requires --state-file BEFORE authentication check
    if resume and not state_file:
        console.print("[red]--resume requires --state-file[/red]")
        raise typer.Exit(code=1)
    
    app_ctx = _get_ctx(ctx)
    project_id = _resolve_project(app_ctx.profile, project)
    parsed_metadata = _prepare_metadata(metadata)

    files = _iter_files(path, recursive, pattern)
    state_store = (
        UploadStateStore(state_file.resolve() if state_file else None, resume)
        if (state_file or resume)
        else None
    )

    def worker(file_path: Path) -> UploadResult:
        res = _upload_file(
            app_ctx.client,
            file_path,
            project_id,
            agent_id=agent,
            metadata=parsed_metadata,
        )
        if throttle > 0:
            time.sleep(throttle)
        return res

    results = _run_parallel_uploads(
        files, worker, max_workers=workers, state_store=state_store
    )
    if results:
        _render_summary(results)

    failed = [res for res in results if res.error]
    if failed:
        console.print(f"[red]{len(failed)} file(s) failed to upload[/red]")
        raise typer.Exit(code=1)

    _maybe_verify_vectors(
        results,
        enabled_flag=verify_vectors,
        pg_dsn=pg_dsn,
        timeout=pg_timeout,
        poll_interval=pg_poll,
    )


def _load_manifest(manifest_path: Path) -> List[Dict[str, object]]:
    import yaml  # Lazy import; PyYAML is declared as a dependency

    data = yaml.safe_load(manifest_path.read_text())
    if isinstance(data, dict) and "items" in data:
        entries = data["items"]
    elif isinstance(data, list):
        entries = data
    else:
        raise typer.BadParameter(
            "Manifest must be a list of entries or contain an 'items' list"
        )

    normalized: List[Dict[str, object]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise typer.BadParameter("Manifest entries must be objects")
        if "path" not in entry:
            raise typer.BadParameter("Manifest entry missing 'path'")
        normalized.append(entry)
    return normalized


@app.command("manifest")
def ingest_manifest(
    ctx: typer.Context,
    manifest: Path = typer.Argument(
        ..., exists=True, resolve_path=True, help="YAML or JSON manifest"
    ),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        "-p",
        help="Fallback project ID when entry does not specify one",
    ),
    workers: int = typer.Option(
        4, "--workers", "-w", min=1, max=32, help="Concurrent uploads"
    ),
    verify_vectors: bool = typer.Option(
        False,
        "--verify-vectors/--no-verify-vectors",
        help="Block until chunk_vectors rows exist for uploaded documents",
    ),
    pg_dsn: Optional[str] = typer.Option(
        None,
        "--pg-dsn",
        help="Postgres DSN used for pgvector verification (defaults to DOCLAYER_PG_DSN)",
    ),
    pg_timeout: float = typer.Option(
        60.0, "--pg-timeout", help="Max seconds to wait for pgvector rows"
    ),
    pg_poll: float = typer.Option(
        2.0, "--pg-poll-interval", help="Polling interval in seconds"
    ),
    state_file: Optional[Path] = typer.Option(
        None,
        "--state-file",
        help="Path to a JSON file that tracks upload progress for resume/retry workflows",
    ),
    resume: bool = typer.Option(
        False,
        "--resume/--no-resume",
        help="Skip manifest entries already marked as successful in --state-file",
    ),
) -> None:
    """
    Upload files described in a manifest.

    Manifest format:

    ```
    - path: ./docs/invoice.pdf
      project: 123e4567
      agent: finance
      metadata:
        tags: ["invoice"]
    ```
    """

    # Validate --resume requires --state-file BEFORE authentication check
    if resume and not state_file:
        console.print("[red]--resume requires --state-file[/red]")
        raise typer.Exit(code=1)
    
    app_ctx = _get_ctx(ctx)
    default_project = project or app_ctx.profile.default_project
    state_store = (
        UploadStateStore(state_file.resolve() if state_file else None, resume)
        if (state_file or resume)
        else None
    )

    entries = _load_manifest(manifest)
    root_dir = manifest.parent

    batch: List[Path] = []
    directives: Dict[Path, Dict[str, object]] = {}
    for entry in entries:
        entry_project = entry.get("project") or default_project
        if not entry_project:
            raise typer.BadParameter(
                "Manifest entry missing project and no default provided"
            )

        file_path = Path(entry["path"])
        if not file_path.is_absolute():
            file_path = (root_dir / file_path).resolve()

        if not file_path.is_file():
            raise typer.BadParameter(f"Manifest path not found: {file_path}")

        directives[file_path] = {
            "project": entry_project,
            "agent": entry.get("agent"),
            "metadata": entry.get("metadata"),
        }
        batch.append(file_path)

    def worker(file_path: Path) -> UploadResult:
        directive = directives[file_path]
        metadata = directive.get("metadata")
        if metadata and not isinstance(metadata, dict):
            raise typer.BadParameter("metadata entries must be JSON objects")
        return _upload_file(
            app_ctx.client,
            file_path,
            directive["project"],  # type: ignore[arg-type]
            agent_id=directive.get("agent"),  # type: ignore[arg-type]
            metadata=metadata,  # type: ignore[arg-type]
        )

    results = _run_parallel_uploads(
        batch, worker, max_workers=workers, state_store=state_store
    )
    if results:
        _render_summary(results)

    failed = [res for res in results if res.error]
    if failed:
        console.print(f"[red]{len(failed)} manifest item(s) failed[/red]")
        raise typer.Exit(code=1)

    _maybe_verify_vectors(
        results,
        enabled_flag=verify_vectors,
        pg_dsn=pg_dsn,
        timeout=pg_timeout,
        poll_interval=pg_poll,
    )
