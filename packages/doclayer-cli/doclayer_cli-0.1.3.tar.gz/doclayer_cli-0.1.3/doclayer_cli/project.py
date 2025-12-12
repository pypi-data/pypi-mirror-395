from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIError


app = typer.Typer(help="Project and organization management")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("create")
def create(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Project name"),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        help="Project description",
    ),
    set_default: bool = typer.Option(
        False,
        "--set-default",
        help="Set as default project",
    ),
) -> None:
    """Create a new project."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    if description is None:
        description = ""

    req = {"name": name, "description": description}
    try:
        project = client.request("POST", "/api/v4/projects", json_body=req)
    except APIError as exc:
        console.print(f"[red]Failed to create project: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[green]✓ Project created successfully[/green]")
    console.print(f"  ID: {project.get('id')}")
    console.print(f"  Name: {project.get('name')}")
    if project.get("description"):
        console.print(f"  Description: {project.get('description')}")

    if set_default:
        prof = app_ctx.profile
        prof.default_project = project.get("id")
        app_ctx.config.set_profile(prof)
        from .config import save_config

        save_config(app_ctx.config, app_ctx.config_path)
        console.print("[green]✓ Set as default project[/green]")


@app.command("list")
def list_projects(
    ctx: typer.Context,
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (table, json)",
    ),
) -> None:
    """List all projects."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        resp = client.request("GET", "/api/v4/projects")
    except APIError as exc:
        console.print(f"[red]Failed to list projects: {exc}[/red]")
        raise typer.Exit(code=1)

    projects = resp.get("projects") if isinstance(resp, dict) else resp
    if not projects:
        console.print("No projects found")
        return

    default_project = app_ctx.profile.default_project

    if output == "json":

        enriched = []
        for p in projects:
            p = dict(p)
            p["is_default"] = p.get("id") == default_project
            enriched.append(p)
        console.print_json(data=enriched)
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Status")
    table.add_column("Created")
    table.add_column("Default")

    for p in projects:
        table.add_row(
            p.get("id", ""),
            p.get("name", ""),
            p.get("description", ""),
            p.get("status", ""),
            (p.get("created_at") or "")[:10],
            "✓" if p.get("id") == default_project else "",
        )

    console.print(table)


@app.command("use")
def use(
    ctx: typer.Context,
    project_id: str = typer.Argument(..., help="Project ID"),
) -> None:
    """Switch to a project (set as default)."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        project = client.request("GET", f"/api/v4/projects/{project_id}")
    except APIError as exc:
        console.print(f"[red]Project not found: {exc}[/red]")
        raise typer.Exit(code=1)

    prof = app_ctx.profile
    prof.default_project = project_id
    app_ctx.config.set_profile(prof)
    from .config import save_config

    save_config(app_ctx.config, app_ctx.config_path)

    console.print(
        f"[green]✓ Switched to project: {project.get('name')} ({project.get('id')})[/green]"
    )


@app.command("info")
def info(
    ctx: typer.Context,
    project_id: Optional[str] = typer.Argument(
        None,
        help="Project ID (defaults to current profile's default project)",
    ),
) -> None:
    """Show detailed project information."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    if not project_id:
        project_id = app_ctx.profile.default_project
        if not project_id:
            console.print("[red]No project specified and no default project set[/red]")
            raise typer.Exit(code=1)

    try:
        project = client.request("GET", f"/api/v4/projects/{project_id}")
    except APIError as exc:
        console.print(f"[red]Failed to get project: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[bold cyan]Project Information[/bold cyan]")
    console.print(f"ID: {project.get('id')}")
    console.print(f"Name: {project.get('name')}")
    console.print(f"Description: {project.get('description')}")
    console.print(f"Status: {project.get('status')}")
    console.print(f"Organization: {project.get('organization_id')}")
    console.print(f"Created: {project.get('created_at')}")
    console.print(f"Updated: {project.get('updated_at')}")


@app.command("set-default")
def set_default(
    ctx: typer.Context,
    project_id: str = typer.Argument(..., help="Project ID"),
) -> None:
    """Set a project as the default for the active profile."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        project = client.request("GET", f"/api/v4/projects/{project_id}")
    except APIError as exc:
        console.print(f"[red]Project not found: {exc}[/red]")
        raise typer.Exit(code=1)

    prof = app_ctx.profile
    prof.default_project = project_id
    app_ctx.config.set_profile(prof)
    from .config import save_config

    save_config(app_ctx.config, app_ctx.config_path)
    console.print(
        f"[green]✓ Default project set to: {project.get('name')} ({project.get('id')})[/green]"
    )
