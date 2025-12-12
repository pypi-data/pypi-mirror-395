from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIClient, APIError
from . import ingest as ingest_commands


app = typer.Typer(help="Document upload and processing")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


def _ensure_file_exists(path: Path) -> None:
    if not path.is_file():
        console.print(f"[red]File not found: {path}[/red]")
        raise typer.Exit(code=1)


@app.command("upload")
def upload(
    ctx: typer.Context,
    file: Path = typer.Argument(..., exists=True, readable=True, help="File to upload"),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        help="Project ID (defaults to profile)",
    ),
    agent: Optional[str] = typer.Option(
        None,
        "--agent",
        help="Agent ID to store alongside the job metadata",
    ),
    metadata: Optional[str] = typer.Option(
        None,
        "--metadata",
        help="Inline JSON metadata attached to the ingestion job",
    ),
    wait: bool = typer.Option(
        False,
        "--wait",
        help="Wait for processing to complete",
    ),
) -> None:
    """Upload a document via the ingest-service endpoint."""
    app_ctx = _get_ctx(ctx)
    client: APIClient = app_ctx.client

    _ensure_file_exists(file)

    project_id = ingest_commands._resolve_project(app_ctx.profile, project)
    parsed_metadata = ingest_commands._prepare_metadata(metadata)

    result = ingest_commands._upload_file(
        client,
        file,
        project_id,
        agent_id=agent,
        wait=wait,
        metadata=parsed_metadata,
    )

    ingest_commands._render_summary([result])

    if result.error:
        raise typer.Exit(code=1)


@app.command("list")
def list_documents(
    ctx: typer.Context,
    project: Optional[str] = typer.Option(
        None,
        "--project",
        help="Filter by project ID",
    ),
    status: Optional[str] = typer.Option(
        None,
        "--status",
        help="Filter by status",
    ),
    limit: int = typer.Option(
        20,
        "--limit",
        help="Maximum number of documents to list",
    ),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (json, table)",
    ),
) -> None:
    """List documents."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    params: dict[str, str] = {}
    if project:
        params["project_id"] = project
    if status:
        params["status"] = status
    if limit > 0:
        params["limit"] = str(limit)

    try:
        data = client.request("GET", "/api/v4/documents", params=params)
    except APIError as exc:
        console.print(f"[red]Failed to list documents: {exc}[/red]")
        raise typer.Exit(code=1)

    documents = data.get("documents") if isinstance(data, dict) else data
    if not documents:
        console.print("No documents found")
        return

    if output == "json":
        console.print_json(data=documents)
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Size")
    table.add_column("Created")

    for doc in documents:
        table.add_row(
            doc.get("id", ""),
            doc.get("name", ""),
            doc.get("status", ""),
            str(doc.get("file_size", "")),
            doc.get("created_at", ""),
        )

    console.print(table)


@app.command("get")
def get_document(
    ctx: typer.Context,
    document_id: str = typer.Argument(..., help="Document ID"),
    show_chunks: bool = typer.Option(
        False,
        "--show-chunks",
        help="Show chunk previews",
    ),
    show_extractions: bool = typer.Option(
        False,
        "--show-extractions",
        help="Show extraction summaries",
    ),
) -> None:
    """Get document details."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        doc = client.request("GET", f"/api/v4/documents/{document_id}")
    except APIError as exc:
        console.print(f"[red]Failed to get document: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold cyan]Document: {doc.get('name')}[/bold cyan]")
    console.print(f"ID: {doc.get('id')}")
    console.print(f"Status: {doc.get('status')}")
    console.print(f"Size: {doc.get('file_size')}")
    console.print(f"Type: {doc.get('mime_type')}")
    console.print(f"Created: {doc.get('created_at')}")

    if doc.get("project_id"):
        console.print(f"Project: {doc.get('project_id')}")

    if show_chunks:
        try:
            chunks = client.request("GET", f"/api/v4/documents/{document_id}/chunks")
        except APIError:
            chunks = []
        if chunks:
            console.print(f"\nChunks: {len(chunks)}")
            for i, chunk in enumerate(chunks[:3]):
                content = str(chunk.get("content", ""))
                if len(content) > 60:
                    content = content[:57] + "..."
                console.print(f"  {i+1}. {content}")
            if len(chunks) > 3:
                console.print(f"  ... and {len(chunks) - 3} more")

    if show_extractions:
        try:
            extractions = client.request(
                "GET", f"/api/v4/documents/{document_id}/extractions"
            )
        except APIError:
            extractions = []
        if extractions:
            console.print(f"\nExtractions: {len(extractions)}")
            for ex in extractions[:3]:
                console.print(f"  {ex.get('type')}: confidence={ex.get('confidence')}")


@app.command("metadata")
def metadata(
    ctx: typer.Context,
    document_id: str = typer.Argument(..., help="Document ID"),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (json, table)",
    ),
) -> None:
    """Get document metadata."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        doc = client.request("GET", f"/api/v4/documents/{document_id}")
    except APIError as exc:
        console.print(f"[red]Failed to get document metadata: {exc}[/red]")
        raise typer.Exit(code=1)

    if output == "json":
        console.print_json(data=doc)
        return

    console.print("[bold cyan]Document Metadata[/bold cyan]")
    for key, value in doc.items():
        console.print(f"{key}: {value}")


@app.command("chunks")
def chunks(
    ctx: typer.Context,
    document_id: str = typer.Argument(..., help="Document ID"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum chunks to display"),
    output: str = typer.Option(
        "table",
        "--output",
        "-o",
        help="Output format (table, json)",
    ),
) -> None:
    """List document chunks."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        chunks_data = client.request("GET", f"/api/v4/documents/{document_id}/chunks")
    except APIError as exc:
        console.print(f"[red]Failed to get chunks: {exc}[/red]")
        raise typer.Exit(code=1)

    chunks_list = chunks_data if isinstance(chunks_data, list) else chunks_data.get("chunks", [])
    if not chunks_list:
        console.print("No chunks found")
        return

    # Limit results
    chunks_list = chunks_list[:limit]

    if output == "json":
        console.print_json(data=chunks_list)
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Chunk ID")
    table.add_column("Page")
    table.add_column("Seq")
    table.add_column("Text")

    for chunk in chunks_list:
        chunk_id = str(chunk.get("id", chunk.get("chunk_id", "")))
        page = str(chunk.get("page", chunk.get("page_number", "-")))
        seq = str(chunk.get("seq", chunk.get("sequence", "-")))
        text = str(chunk.get("content", chunk.get("text", "")))
        if len(text) > 50:
            text = text[:47] + "..."
        table.add_row(chunk_id, page, seq, text)

    console.print(table)


@app.command("extractions")
def extractions(
    ctx: typer.Context,
    document_id: str = typer.Argument(..., help="Document ID"),
    status: Optional[str] = typer.Option(
        None,
        "--status",
        help="Filter by status (e.g., 'ready')",
    ),
    output: str = typer.Option(
        "table",
        "--output",
        "-o",
        help="Output format (table, json)",
    ),
) -> None:
    """List document extractions."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    params: dict[str, str] = {}
    if status:
        params["status"] = status

    try:
        extractions_data = client.request(
            "GET", f"/api/v4/documents/{document_id}/extractions", params=params
        )
    except APIError as exc:
        console.print(f"[red]Failed to get extractions: {exc}[/red]")
        raise typer.Exit(code=1)

    extractions_list = (
        extractions_data
        if isinstance(extractions_data, list)
        else extractions_data.get("extractions", [])
    )
    if not extractions_list:
        console.print("No extractions found")
        return

    if output == "json":
        console.print_json(data=extractions_list)
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Type")
    table.add_column("Field")
    table.add_column("Status")
    table.add_column("Confidence")
    table.add_column("Page")

    for ex in extractions_list:
        table.add_row(
            str(ex.get("type", "-")),
            str(ex.get("field_name", "-")),
            str(ex.get("status", "-")),
            str(ex.get("confidence", "-")),
            str(ex.get("page", ex.get("page_number", "-"))),
        )

    console.print(table)


@app.command("annotations")
def annotations(
    ctx: typer.Context,
    document_id: str = typer.Argument(..., help="Document ID"),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (json, table)",
    ),
) -> None:
    """Get document annotations."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        doc = client.request("GET", f"/api/v4/documents/{document_id}")
        annotations_data = doc.get("annotations", [])
    except APIError as exc:
        console.print(f"[red]Failed to get annotations: {exc}[/red]")
        raise typer.Exit(code=1)

    if not annotations_data:
        console.print("No annotations found")
        return

    if output == "json":
        console.print_json(data=annotations_data)
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Type")
    table.add_column("Content")
    table.add_column("Page")
    table.add_column("Position")

    for ann in annotations_data:
        table.add_row(
            str(ann.get("type", "-")),
            str(ann.get("content", ""))[:50] + ("..." if len(str(ann.get("content", ""))) > 50 else ""),
            str(ann.get("page", "-")),
            str(ann.get("position", "-")),
        )

    console.print(table)


@app.command("download")
def download(
    ctx: typer.Context,
    document_id: str = typer.Argument(..., help="Document ID"),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output file path",
    ),
) -> None:
    """Download document results/extractions."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        # Try to get extractions/results first
        try:
            results = client.request("GET", f"/api/v4/documents/{document_id}/extractions")
        except APIError:
            # Fallback to document metadata
            results = client.request("GET", f"/api/v4/documents/{document_id}")

        import json

        output.write_text(json.dumps(results, indent=2))
        console.print(f"[green]✓ Downloaded to {output}[/green]")
    except APIError as exc:
        console.print(f"[red]Failed to download document: {exc}[/red]")
        raise typer.Exit(code=1)
    except Exception as exc:
        console.print(f"[red]Failed to write file: {exc}[/red]")
        raise typer.Exit(code=1)


@app.command("delete")
def delete(
    ctx: typer.Context,
    document_id: str = typer.Argument(..., help="Document ID"),
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip confirmation prompt",
    ),
) -> None:
    """Delete a document (GDPR)."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    if not force:
        answer = (
            input(f"Are you sure you want to delete document {document_id}? [y/N]: ")
            .strip()
            .lower()
        )
        if answer not in {"y", "yes"}:
            console.print("[yellow]Aborted[/yellow]")
            raise typer.Exit(code=0)

    try:
        client.request("DELETE", f"/api/v4/documents/{document_id}")
        console.print("[green]✓ Document deleted[/green]")
    except APIError as exc:
        console.print(f"[red]Failed to delete document: {exc}[/red]")
        raise typer.Exit(code=1)


@app.command("cleanup")
def cleanup(
    ctx: typer.Context,
    document_id: Optional[str] = typer.Argument(
        None,
        help="Document ID (optional if using --project)",
    ),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        "-p",
        help="Project ID for bulk cleanup",
    ),
    mode: str = typer.Option(
        ...,
        "--mode",
        help="Cleanup mode: soft or gdpr",
    ),
    reason: Optional[str] = typer.Option(
        None,
        "--reason",
        help="Reason for cleanup",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip confirmation for GDPR mode",
    ),
    older_than: Optional[str] = typer.Option(
        None,
        "--older-than",
        help="Age filter (e.g., '30d' for 30 days)",
    ),
    confirm: bool = typer.Option(
        False,
        "--confirm",
        help="Confirm bulk operation",
    ),
    pg_dsn: Optional[str] = typer.Option(
        None,
        "--pg-dsn",
        help="Postgres DSN for verification (defaults to DOCLAYER_PG_DSN)",
    ),
) -> None:
    """Cleanup document (soft delete or GDPR purge)."""
    import os
    from datetime import datetime, timedelta

    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    if mode not in {"soft", "gdpr"}:
        console.print("[red]Mode must be 'soft' or 'gdpr'[/red]")
        raise typer.Exit(code=1)

    if not document_id and not project:
        console.print("[red]Either document_id or --project must be provided[/red]")
        raise typer.Exit(code=1)

    if document_id:
        # Single document cleanup
        try:
            # Confirm document status
            doc = client.request("GET", f"/api/v4/documents/{document_id}")
            console.print(f"[cyan]Document: {doc.get('name', document_id)}[/cyan]")

            if mode == "gdpr" and not force:
                answer = (
                    input(
                        f"Are you sure you want to GDPR delete document {document_id}? This cannot be undone. [y/N]: "
                    )
                    .strip()
                    .lower()
                )
                if answer not in {"y", "yes"}:
                    console.print("[yellow]Aborted[/yellow]")
                    raise typer.Exit(code=0)

            # Perform cleanup
            payload: dict[str, object] = {"mode": mode}
            if reason:
                payload["reason"] = reason

            endpoint = (
                f"/api/v4/documents/{document_id}/gdpr-delete"
                if mode == "gdpr"
                else f"/api/v4/documents/{document_id}/cleanup"
            )
            client.request("POST", endpoint, json_body=payload)

            console.print(f"[green]✓ Cleanup initiated (mode: {mode})[/green]")

            # Verify pgvector cleanup if DSN provided
            dsn = pg_dsn or os.getenv("DOCLAYER_PG_DSN")
            if dsn and mode == "gdpr":
                from .pgvector_probe import wait_for_vectors

                console.print("[cyan]Verifying pgvector cleanup...[/cyan]")
                try:
                    counts = wait_for_vectors([document_id], dsn, min_rows=0, timeout=30.0)
                    if counts.get(document_id, 0) == 0:
                        console.print("[green]✓ pgvector cleanup verified[/green]")
                    else:
                        console.print(
                            f"[yellow]Warning: {counts.get(document_id, 0)} rows still exist[/yellow]"
                        )
                except Exception as exc:
                    console.print(f"[yellow]Could not verify pgvector cleanup: {exc}[/yellow]")

        except APIError as exc:
            console.print(f"[red]Failed to cleanup document: {exc}[/red]")
            raise typer.Exit(code=1)
    else:
        # Bulk cleanup by project
        if not confirm:
            console.print(
                "[red]Bulk cleanup requires --confirm flag[/red]"
            )
            raise typer.Exit(code=1)

        console.print(f"[yellow]Bulk cleanup for project {project} is not yet implemented[/yellow]")
        console.print("[yellow]Please use document-level cleanup instead[/yellow]")
        raise typer.Exit(code=1)
