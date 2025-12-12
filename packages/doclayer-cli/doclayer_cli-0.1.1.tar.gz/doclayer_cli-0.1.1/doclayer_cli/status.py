from __future__ import annotations

import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence

import typer
from rich.console import Console
from rich.live import Live
from rich.table import Table

from .api_client import APIClient, APIError
from .pgvector_probe import PgvectorProbeError, wait_for_vectors


app = typer.Typer(help="Monitor ingestion jobs and downstream processing status.")
console = Console()


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


def _fetch_jobs(
    client: APIClient,
    *,
    project: Optional[str],
    status_filters: Optional[Sequence[str]],
    limit: int,
    since: Optional[datetime],
) -> List[Dict[str, object]]:
    params: Dict[str, str] = {}
    if project:
        params["project_id"] = project
    if status_filters:
        params["status"] = ",".join(status_filters)
    if limit > 0:
        params["limit"] = str(limit)
    if since:
        params["since"] = since.isoformat()

    try:
        data = client.request("GET", "/api/v4/ingest/jobs", params=params)
    except APIError as exc:
        console.print(f"[red]Failed to fetch jobs: {exc}[/red]")
        raise typer.Exit(code=1)

    jobs = data.get("jobs") if isinstance(data, dict) else data
    if not isinstance(jobs, list):
        console.print(
            "[yellow]Unexpected response payload; nothing to display[/yellow]"
        )
        return []

    jobs = jobs[:limit] if limit else jobs
    if since:
        jobs = [
            job
            for job in jobs
            if _parse_datetime(job.get("updated_at")) is None
            or _parse_datetime(job.get("updated_at")) >= since
        ]

    if status_filters:
        statuses = {s.lower() for s in status_filters}
        jobs = [job for job in jobs if str(job.get("status", "")).lower() in statuses]
    return jobs


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _render_jobs_table(jobs: Sequence[Dict[str, object]]) -> Table:
    table = Table(show_header=True, header_style="bold")
    table.add_column("Job ID")
    table.add_column("Status")
    table.add_column("Updated")
    table.add_column("File Size", justify="right")
    table.add_column("Checksum")

    for job in jobs:
        table.add_row(
            str(job.get("job_id", "")),
            job.get("status", "unknown"),
            job.get("updated_at", "-"),
            str(job.get("file_size", "")),
            job.get("checksum", "") or "-",
        )
    return table


@app.command("list")
def list_jobs(
    ctx: typer.Context,
    project: Optional[str] = typer.Option(
        None, "--project", "-p", help="Filter by project ID"
    ),
    all_projects: bool = typer.Option(
        False,
        "--all-projects",
        help="Ignore the profile default project and list every job",
    ),
    status_filter: Optional[List[str]] = typer.Option(
        None,
        "--status",
        "-s",
        help="Comma-separated status filters (pending,processing,completed,failed)",
    ),
    limit: int = typer.Option(25, "--limit", "-l", help="Maximum jobs to display"),
    since: Optional[datetime] = typer.Option(
        None,
        "--since",
        formats=["%Y-%m-%dT%H:%M:%S"],
        help="ISO timestamp filter (UTC)",
    ),
    output: str = typer.Option(
        "table",
        "--output",
        "-o",
        help="Output format: table, json, or yaml",
    ),
) -> None:
    """List recent ingestion jobs."""
    app_ctx = _get_ctx(ctx)
    resolved_project = project or (
        None if all_projects else app_ctx.profile.default_project
    )

    jobs = _fetch_jobs(
        app_ctx.client,
        project=resolved_project,
        status_filters=status_filter,
        limit=limit,
        since=since,
    )

    if output == "json":
        console.print_json(data=jobs)
        return
    if output == "yaml":
        import yaml

        console.print(yaml.safe_dump(jobs, sort_keys=False))
        return

    table = _render_jobs_table(jobs)
    console.print(table)


@app.command("watch")
def watch_jobs(
    ctx: typer.Context,
    project: Optional[str] = typer.Option(
        None, "--project", "-p", help="Project filter"
    ),
    refresh: float = typer.Option(
        5.0, "--interval", "-i", help="Refresh interval in seconds"
    ),
    status_filter: Optional[List[str]] = typer.Option(
        None,
        "--status",
        "-s",
        help="Comma-separated status filters",
    ),
    limit: int = typer.Option(25, "--limit", "-l", help="Maximum jobs to display"),
) -> None:
    """Continuously watch ingestion job status."""
    app_ctx = _get_ctx(ctx)
    resolved_project = project or app_ctx.profile.default_project

    with Live(auto_refresh=False) as live:
        while True:
            jobs = _fetch_jobs(
                app_ctx.client,
                project=resolved_project,
                status_filters=status_filter,
                limit=limit,
                since=None,
            )
            live.update(_render_jobs_table(jobs), refresh=True)
            time.sleep(max(refresh, 1.0))


def _fetch_job(client: APIClient, job_id: str) -> Dict[str, object]:
    try:
        return client.request("GET", f"/api/v4/ingest/{job_id}")
    except APIError as exc:
        console.print(f"[red]Failed to fetch job {job_id}: {exc}[/red]")
        raise typer.Exit(code=1)


def _fetch_document(client: APIClient, document_id: str) -> Dict[str, object]:
    try:
        return client.request("GET", f"/api/v4/documents/{document_id}")
    except APIError:
        return {}


def _fetch_chunks(client: APIClient, document_id: str) -> List[Dict[str, object]]:
    try:
        data = client.request("GET", f"/api/v4/documents/{document_id}/chunks")
        return data if isinstance(data, list) else data.get("chunks", [])
    except APIError:
        return []


@app.command("inspect")
def inspect_job(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Ingestion job ID"),
    show_documents: bool = typer.Option(
        True, "--documents/--no-documents", help="Display document details"
    ),
    show_vectors: bool = typer.Option(
        False,
        "--vectors/--no-vectors",
        help="Query chunk count per document via /chunks",
    ),
) -> None:
    """Inspect a single ingestion job with optional document details."""
    app_ctx = _get_ctx(ctx)
    job = _fetch_job(app_ctx.client, job_id)

    console.print_json(data=job)

    if not show_documents:
        return

    documents = job.get("documents") or []
    if not documents:
        console.print("[yellow]No document metadata available for this job[/yellow]")
        return

    doc_table = Table(show_header=True, header_style="bold")
    doc_table.add_column("Document ID")
    doc_table.add_column("Filename")
    doc_table.add_column("Size", justify="right")
    doc_table.add_column("Chunks", justify="right")

    for doc in documents:
        doc_id = doc.get("id")
        chunk_count = "-"
        if show_vectors and doc_id:
            chunks = _fetch_chunks(app_ctx.client, doc_id)
            chunk_count = str(len(chunks))

        doc_table.add_row(
            doc_id or "-",
            doc.get("filename", "-"),
            str(doc.get("file_size") or "-"),
            chunk_count,
        )

    console.print("\n[bold]Documents[/bold]")
    console.print(doc_table)


@app.command("grounding")
def grounding_report(
    ctx: typer.Context,
    tenant: Optional[str] = typer.Option(
        None,
        "--tenant",
        "-t",
        help="Override tenant/organization ID (defaults to profile tenant)",
    ),
    job_id: Optional[str] = typer.Option(
        None,
        "--job-id",
        help="Filter by ingestion/job id",
    ),
    checksum: Optional[str] = typer.Option(
        None,
        "--checksum",
        help="Document checksum filter",
    ),
    status_filter: Optional[str] = typer.Option(
        None,
        "--status",
        help="Trace status filter (pending, complete, failed, ...)",
    ),
    field_name: Optional[str] = typer.Option(
        None,
        "--field",
        help="Only include traces referencing this field name",
    ),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum traces to inspect"),
) -> None:
    """Summarize LangExtract grounding coverage and highlight missing spans."""
    app_ctx = _get_ctx(ctx)
    tenant_filter = tenant or app_ctx.profile.tenant_id or app_ctx.client.tenant_id
    if not tenant_filter:
        console.print(
            "[red]Tenant/organization ID is required. Set profile.tenant_id or pass --tenant.[/red]"
        )
        raise typer.Exit(code=1)

    raw_traces = app_ctx.client.fetch_extraction_traces(
        tenant_id=tenant_filter,
        job_id=job_id,
        checksum=checksum,
        status=status_filter,
        field_name=field_name,
        limit=limit,
    )
    traces = raw_traces if isinstance(raw_traces, list) else raw_traces or []
    if not traces:
        console.print(
            "[yellow]No extraction traces found for the requested filters.[/yellow]"
        )
        return

    summaries = [_compute_grounding_metrics(trace) for trace in traces]
    _render_grounding_summary_table(summaries)
    _render_missing_groundings_table(summaries)


@app.command("verify-pgvector")
def verify_pgvector(
    ctx: typer.Context,
    document_ids: List[str] = typer.Argument(
        ..., help="Document UUIDs to verify in chunk_vectors"
    ),
    pg_dsn: Optional[str] = typer.Option(
        None,
        "--pg-dsn",
        help="Postgres DSN (defaults to DOCLAYER_PG_DSN)",
    ),
    min_rows: int = typer.Option(
        1, "--min-rows", help="Minimum rows required per document"
    ),
    timeout: float = typer.Option(30.0, "--timeout", help="Seconds to wait"),
    poll_interval: float = typer.Option(
        2.0, "--poll", help="Polling interval in seconds"
    ),
) -> None:
    """Validate that chunk_vectors contains rows for the provided document IDs."""
    _ = _get_ctx(ctx)  # Ensure authentication even though we only touch the database

    dsn = pg_dsn or os.getenv("DOCLAYER_PG_DSN")
    if not dsn:
        console.print("[red]--pg-dsn or DOCLAYER_PG_DSN must be provided[/red]")
        raise typer.Exit(code=1)

    try:
        counts = wait_for_vectors(
            document_ids,
            dsn,
            min_rows=min_rows,
            timeout=timeout,
            poll_interval=poll_interval,
        )
    except PgvectorProbeError as exc:
        console.print(f"[red]pgvector verification failed: {exc}[/red]")
        raise typer.Exit(code=1) from exc

    missing = [doc_id for doc_id, count in counts.items() if count < min_rows]
    if missing:
        console.print(
            f"[red]Missing or incomplete vectors for document(s): {', '.join(missing)}[/red]"
        )
        raise typer.Exit(code=1)

    console.print("[green]✓ pgvector rows verified for all documents[/green]")


def _compute_grounding_metrics(trace: Dict[str, Any]) -> Dict[str, Any]:
    expected_fields = _extract_expected_fields(trace)
    groundings = trace.get("groundings") or []

    coverage_fields = set()
    spanless_fields = {}
    field_examples = {}
    for item in groundings:
        field = item.get("field_name")
        if not field:
            continue
        has_span = (
            item.get("span_start") is not None and item.get("span_end") is not None
        )
        if has_span:
            coverage_fields.add(field)
        else:
            spanless_fields.setdefault(field, item)
        field_examples.setdefault(field, item)

    # Fall back to observed fields if the payload is empty
    baseline_fields = expected_fields or set(field_examples.keys())
    denominator = len(baseline_fields) if baseline_fields else 1
    coverage_ratio = len(coverage_fields) / denominator if denominator else 0.0

    missing_details: List[Dict[str, Any]] = []
    for field in sorted(baseline_fields):
        if field in coverage_fields:
            continue
        reason = (
            "missing span coordinates"
            if field in spanless_fields
            else "no grounding rows"
        )
        sample = spanless_fields.get(field) or field_examples.get(field) or {}
        missing_details.append(
            {
                "job_id": trace.get("job_id"),
                "field": field,
                "reason": reason,
                "page": sample.get("page") or sample.get("page_number"),
                "span_start": sample.get("span_start"),
                "span_end": sample.get("span_end"),
                "status": trace.get("status"),
                "quality": trace.get("quality_level"),
            }
        )

    return {
        "trace": trace,
        "coverage": coverage_ratio,
        "missing": missing_details,
        "expected_fields": sorted(baseline_fields),
    }


def _extract_expected_fields(trace: Dict[str, Any]) -> set[str]:
    payload = trace.get("result_payload") or {}
    extracted = payload.get("extracted_data")
    if isinstance(extracted, dict):
        return {str(key) for key in extracted.keys()}
    return set()


def _render_grounding_summary_table(summaries: List[Dict[str, Any]]) -> None:
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Job ID")
    table.add_column("Quality")
    table.add_column("Status")
    table.add_column("Coverage", justify="right")
    table.add_column("Missing Fields", justify="right")

    total_coverage = 0.0
    for item in summaries:
        trace = item["trace"]
        coverage_pct = f"{item['coverage'] * 100:.1f}%"
        table.add_row(
            str(trace.get("job_id", "-")),
            trace.get("quality_level", "-"),
            trace.get("status", "-"),
            coverage_pct,
            str(len(item["missing"])),
        )
        total_coverage += item["coverage"]

    avg_coverage = total_coverage / len(summaries)
    console.print(table)
    console.print(f"[bold]Average coverage:[/bold] {avg_coverage * 100:.1f}%")


def _render_missing_groundings_table(summaries: List[Dict[str, Any]]) -> None:
    missing_rows = [missing for item in summaries for missing in item["missing"]]
    if not missing_rows:
        console.print("[green]All inspected fields have span coverage.[/green]")
        return

    table = Table(show_header=True, header_style="bold red")
    table.add_column("Job ID")
    table.add_column("Field")
    table.add_column("Reason")
    table.add_column("Page", justify="right")
    table.add_column("Span", justify="right")

    for row in missing_rows:
        span = "-"
        if row.get("span_start") is not None or row.get("span_end") is not None:
            span = f"{row.get('span_start', '?')}–{row.get('span_end', '?')}"
        table.add_row(
            str(row.get("job_id", "-")),
            row.get("field", "-"),
            row.get("reason", "-"),
            str(row.get("page", "-")),
            span,
        )
    console.print(table)
