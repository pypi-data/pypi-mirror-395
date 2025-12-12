from __future__ import annotations


import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIError


app = typer.Typer(help="Agent template management")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("list")
def list_agents(
    ctx: typer.Context,
    category: str = typer.Option("", "--category", help="Filter by category"),
) -> None:
    """List available agent templates."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    params = {"category": category} if category else None
    try:
        resp = client.request("GET", "/api/v4/agents/templates", params=params)
    except APIError as exc:
        console.print(f"[red]Failed to list templates: {exc}[/red]")
        raise typer.Exit(code=1)

    public = resp.get("public_templates", {}) if isinstance(resp, dict) else {}
    templates = public.get("templates") or []
    if not templates:
        console.print("No templates found")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Category")

    for tmpl in templates:
        template_id = tmpl.get("id", "")
        parts = template_id.split(".")
        cat = parts[0] if len(parts) > 1 else ""
        table.add_row(
            template_id,
            tmpl.get("name", ""),
            tmpl.get("version", ""),
            cat,
        )

    console.print(table)


@app.command("get")
def get_agent(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID"),
    verbose: bool = typer.Option(False, "--verbose", help="Show full manifest YAML"),
) -> None:
    """Get agent template details."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    # For parity with Go CLI, this endpoint returns raw YAML.
    try:
        manifest_yaml = client.request("GET", f"/api/v4/agents/templates/{template_id}")
    except APIError as exc:
        console.print(f"[red]Failed to get template: {exc}[/red]")
        raise typer.Exit(code=1)

    if isinstance(manifest_yaml, dict):
        # In case API wraps YAML in JSON, just pretty print JSON.
        console.print_json(data=manifest_yaml)
        return

    if verbose:
        console.print(str(manifest_yaml))
    else:
        # Basic summary: ID + first few lines
        lines = str(manifest_yaml).splitlines()
        console.print(f"[bold cyan]Template: {template_id}[/bold cyan]")
        console.print("\n".join(lines[:20]))
        if len(lines) > 20:
            console.print(f"\n... ({len(lines) - 20} more lines)")
