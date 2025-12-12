from __future__ import annotations

import time

import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIError


app = typer.Typer(help="Temporal workflow management")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("list")
def list_workflows(
    ctx: typer.Context,
    page_size: int = typer.Option(
        20, "--page-size", help="Number of workflows per page"
    ),
    status: str = typer.Option("", "--status", help="Filter by status"),
    start_time_from: str = typer.Option("", "--from", help="Start time from (RFC3339)"),
    start_time_to: str = typer.Option("", "--to", help="Start time to (RFC3339)"),
) -> None:
    """List workflows."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    params = {
        "page_size": page_size,
        "status": status,
        "start_time_from": start_time_from,
        "start_time_to": start_time_to,
    }
    params = {k: v for k, v in params.items() if v}

    try:
        resp = client.request("GET", "/api/v4/workflows", params=params)
    except APIError as exc:
        console.print(f"[red]Failed to list workflows: {exc}[/red]")
        raise typer.Exit(code=1)

    workflows = resp.get("workflows") or []
    if not workflows:
        console.print("No workflows found")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Workflow ID")
    table.add_column("Type")
    table.add_column("Status")
    table.add_column("Start Time")
    table.add_column("Duration (ms)")

    for wf in workflows:
        table.add_row(
            str(wf.get("workflow_id", "")),
            wf.get("workflow_type", ""),
            wf.get("status", ""),
            wf.get("start_time", ""),
            str(wf.get("execution_time", "")),
        )

    console.print(table)
    if resp.get("next_page_token"):
        console.print(
            f"\nMore results available. Use --page-token {resp['next_page_token']}"
        )


@app.command("status")
def status(
    ctx: typer.Context,
    workflow_id: str = typer.Argument(..., help="Workflow ID"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow workflow status"),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (table, json)",
    ),
) -> None:
    """Get workflow status."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    while True:
        try:
            details = client.request("GET", f"/api/v4/workflows/{workflow_id}")
        except APIError as exc:
            console.print(f"[red]Failed to get workflow: {exc}[/red]")
            raise typer.Exit(code=1)

        if output == "json":
            console.print_json(data=details)
        else:
            console.print(
                f"[bold cyan]Workflow: {details.get('workflow_id')}[/bold cyan]"
            )
            console.print(f"Type: {details.get('workflow_type')}")
            console.print(f"Status: {details.get('status')}")
            console.print(f"Start Time: {details.get('start_time')}")
            if details.get("close_time"):
                console.print(f"Close Time: {details.get('close_time')}")
            if details.get("execution_time"):
                console.print(f"Duration: {details.get('execution_time')} ms")

        if not follow or str(details.get("status", "")).lower() in {
            "completed",
            "failed",
            "canceled",
            "terminated",
        }:
            break
        time.sleep(2.0)


@app.command("history")
def history(
    ctx: typer.Context,
    workflow_id: str = typer.Argument(..., help="Workflow ID"),
    page_size: int = typer.Option(50, "--page-size", help="Events per page"),
) -> None:
    """Show workflow execution history."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    params = {"page_size": page_size}
    try:
        hist = client.request(
            "GET", f"/api/v4/workflows/{workflow_id}/history", params=params
        )
    except APIError as exc:
        console.print(f"[red]Failed to get workflow history: {exc}[/red]")
        raise typer.Exit(code=1)

    events = hist.get("events") or []
    if not events:
        console.print("No history events found")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Event ID")
    table.add_column("Time")
    table.add_column("Type")

    for ev in events:
        table.add_row(
            str(ev.get("event_id", "")),
            ev.get("event_time", ""),
            ev.get("event_type", ""),
        )

    console.print(table)


@app.command("cancel")
def cancel(
    ctx: typer.Context,
    workflow_id: str = typer.Argument(..., help="Workflow ID"),
    reason: str = typer.Option("", "--reason", help="Cancellation reason"),
) -> None:
    """Cancel a running workflow."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    payload = {"reason": reason} if reason else {}
    try:
        client.request(
            "POST", f"/api/v4/workflows/{workflow_id}/cancel", json_body=payload
        )
    except APIError as exc:
        console.print(f"[red]Failed to cancel workflow: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[green]✓ Cancellation requested[/green]")


@app.command("retry")
def retry(
    ctx: typer.Context,
    workflow_id: str = typer.Argument(..., help="Workflow ID"),
    reason: str = typer.Option("", "--reason", help="Retry reason"),
    reset_to_event_id: int = typer.Option(
        0,
        "--reset-to-event-id",
        help="Reset to specific event ID",
    ),
) -> None:
    """Retry a failed workflow."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    payload: dict[str, object] = {}
    if reason:
        payload["reason"] = reason
    if reset_to_event_id > 0:
        payload["reset_to_event_id"] = reset_to_event_id

    try:
        result = client.request(
            "POST", f"/api/v4/workflows/{workflow_id}/retry", json_body=payload
        )
    except APIError as exc:
        console.print(f"[red]Failed to retry workflow: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[green]✓ Retry started[/green]")
    console.print(f"Workflow ID: {result.get('workflow_id')}")
    console.print(f"New Run ID: {result.get('new_run_id')}")
