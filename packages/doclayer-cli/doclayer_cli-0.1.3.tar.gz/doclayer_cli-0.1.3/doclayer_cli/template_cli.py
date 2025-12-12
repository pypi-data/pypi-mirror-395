from __future__ import annotations


import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIError


app = typer.Typer(help="Browse and use agent templates")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("list")
def list_templates(
    ctx: typer.Context,
    category: str = typer.Option("", "--category", help="Filter by category"),
    output: str = typer.Option("table", "--output", help="Output format (table, json)"),
) -> None:
    """List available agent templates from the gallery."""
    app_ctx = _get_ctx(ctx)
    
    # Template gallery is public - create unauthenticated client if needed
    from .api_client import APIClient
    client = APIClient(base_url=app_ctx.client.base_url)  # No auth required for listing

    params = {"category": category} if category else None
    try:
        templates = client.request(
            "GET", "/api/v4/template-gallery/templates", params=params
        )
    except APIError as exc:
        console.print(f"[red]Failed to list templates: {exc}[/red]")
        console.print("[yellow]Hint: Check your internet connection or try again later.[/yellow]")
        raise typer.Exit(code=1)

    if not templates:
        console.print("No templates found")
        return

    if output == "json":
        console.print_json(data=templates)
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Version")
    table.add_column("Rating")
    table.add_column("Uses")
    table.add_column("Description")

    for tmpl in templates:
        description = tmpl.get("description", "") or ""
        if len(description) > 50:
            description = description[:47] + "..."
        rating_val = tmpl.get("rating") or 0
        rating = f"{rating_val:.1f}⭐" if rating_val > 0 else ""
        table.add_row(
            tmpl.get("id", ""),
            tmpl.get("name", ""),
            tmpl.get("category", ""),
            tmpl.get("version", ""),
            rating,
            str(tmpl.get("usage_count", 0)),
            description,
        )

    console.print(table)


@app.command("info")
def template_info(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID"),
    show_manifest: bool = typer.Option(
        False,
        "--manifest",
        help="Show template manifest",
    ),
) -> None:
    """Show detailed template information."""
    app_ctx = _get_ctx(ctx)
    
    # Template gallery is public - create unauthenticated client if needed
    from .api_client import APIClient
    client = APIClient(base_url=app_ctx.client.base_url)  # No auth required

    try:
        template = client.request(
            "GET", f"/api/v4/template-gallery/templates/{template_id}"
        )
    except APIError as exc:
        console.print(f"[red]Failed to get template: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[bold cyan]Template Information[/bold cyan]")
    console.print(f"ID: {template.get('id')}")
    console.print(f"Name: {template.get('name')}")
    console.print(f"Description: {template.get('description')}")
    console.print(f"Category: {template.get('category')}")
    console.print(f"Version: {template.get('version')}")

    if template.get("author"):
        console.print(f"Author: {template.get('author')}")
    if template.get("rating"):
        console.print(f"Rating: {template.get('rating'):.1f}⭐")

    console.print(f"Usage Count: {template.get('usage_count', 0)}")
    tags = template.get("tags") or []
    if tags:
        console.print(f"Tags: {', '.join(tags)}")

    console.print(f"Created: {template.get('created_at')}")
    console.print(f"Updated: {template.get('updated_at')}")

    if show_manifest and template.get("manifest") is not None:
        console.print("\n[bold cyan]Manifest[/bold cyan]")
        console.print_json(data=template["manifest"])


@app.command("use")
def use_template(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID"),
    project_dir: str = typer.Option(
        "",
        "--dir",
        help="Project directory (default: ./[agent-name])",
    ),
    agent_name: str = typer.Option(
        "",
        "--name",
        help="Agent name (default: template name)",
    ),
) -> None:
    """Use a template to create a new agent project directory."""
    from pathlib import Path

    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        template = client.request(
            "GET", f"/api/v4/template-gallery/templates/{template_id}"
        )
    except APIError as exc:
        console.print(f"[red]Failed to get template: {exc}[/red]")
        raise typer.Exit(code=1)

    if not agent_name:
        agent_name = template.get("name") or template_id
    if not project_dir:
        project_dir = f"./{agent_name}"

    project_path = Path(project_dir)
    project_path.mkdir(parents=True, exist_ok=True)

    console.print(
        f"[blue]📦 Creating agent from template: {template.get('name')}[/blue]"
    )

    # Write manifest as JSON (can be converted to YAML later by the user)
    manifest_path = project_path / "manifest.json"
    if template.get("manifest") is not None:
        manifest_data = template["manifest"]
        import json

        manifest_path.write_text(json.dumps(manifest_data, indent=2))
        console.print("[green]✓ Created manifest.json[/green]")

    readme_path = project_path / "README.md"
    rating_val = template.get("rating") or 0
    rating = f"{rating_val:.1f}⭐" if rating_val > 0 else ""
    readme = (
        f"# {agent_name}\n\n{template.get('description','')}\n\n"
        f"Created from template: {template.get('name')} (v{template.get('version')})\n\n"
        f"## Usage\n\n```bash\ndoclayer agent run {agent_name} --document path/to/document.pdf\n```\n\n"
        f"## Template Information\n\n- **Category**: {template.get('category')}\n"
        f"- **Author**: {template.get('author')}\n- **Rating**: {rating}\n"
    )
    readme_path.write_text(readme)
    console.print("[green]✓ Created README.md[/green]")

    console.print("[green]🎉 Agent created successfully![/green]")
    console.print(f"  Directory: {project_path}")
    console.print(f"  Manifest: {manifest_path}")
    console.print(f"  README: {readme_path}")
