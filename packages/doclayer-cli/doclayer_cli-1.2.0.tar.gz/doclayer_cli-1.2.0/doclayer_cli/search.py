from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIError


app = typer.Typer(help="Vector and graph search")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("vector")
def vector_search(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", help="Maximum number of results"),
    threshold: float = typer.Option(
        0.0,
        "--threshold",
        help="Minimum similarity score",
    ),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        help="Filter by project ID",
    ),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (table, json)",
    ),
) -> None:
    """Perform vector similarity search."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    params: dict[str, str] = {
        "query": query,
        "limit": str(limit),
    }
    if threshold > 0:
        params["similarity_threshold"] = str(threshold)
    if project:
        params["project_id"] = project

    try:
        payload = client.request("GET", "/api/v4/search", params=params)
    except APIError as exc:
        console.print(f"[red]Vector search failed: {exc}[/red]")
        raise typer.Exit(code=1)

    results = payload.get("results") if isinstance(payload, dict) else payload

    if not results:
        console.print("No results found")
        return

    if output == "json":
        console.print_json(data=results)
        return

    console.print(f"[bold cyan]Search Results for: {query}[/bold cyan]\n")
    for i, result in enumerate(results, start=1):
        score = result.get("score")
        if score is not None:
            console.print(f"{i}. [green](Score: {score:.3f})[/green]")
        else:
            console.print(f"{i}.")
        content = str(result.get("content", ""))
        if len(content) > 200:
            content = content[:197] + "..."
        console.print(f"   {content}")
        if result.get("document_id"):
            line = f"   Document: {result['document_id']}"
            if result.get("chunk_id"):
                line += f" (Chunk: {result['chunk_id']})"
            console.print(line)
        if result.get("metadata"):
            meta = " ".join(f"{k}={v}" for k, v in result["metadata"].items())
            console.print(f"   Metadata: {meta}")
        console.print()


@app.command("hybrid")
def hybrid_search(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", help="Maximum number of results"),
    threshold: float = typer.Option(
        0.0,
        "--threshold",
        help="Minimum similarity score",
    ),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        help="Filter by project ID",
    ),
    alpha: float = typer.Option(
        0.5,
        "--alpha",
        help="Balance between vector (0) and keyword (1) search",
    ),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (table, json)",
    ),
) -> None:
    """Perform hybrid search (vector + keyword)."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    params: dict[str, str] = {
        "query": query,
        "limit": str(limit),
        "mode": "hybrid",
        "alpha": str(alpha),
    }
    if threshold > 0:
        params["similarity_threshold"] = str(threshold)
    if project:
        params["project_id"] = project

    try:
        payload = client.request("GET", "/api/v4/search", params=params)
    except APIError as exc:
        console.print(f"[red]Hybrid search failed: {exc}[/red]")
        raise typer.Exit(code=1)

    results = payload.get("results") if isinstance(payload, dict) else payload

    if not results:
        console.print("No results found")
        return

    if output == "json":
        console.print_json(data=results)
        return

    console.print(f"[bold cyan]Hybrid Search Results for: {query}[/bold cyan]\n")
    for i, result in enumerate(results, start=1):
        score = result.get("score")
        if score is not None:
            console.print(f"{i}. [green](Score: {score:.3f})[/green]")
        else:
            console.print(f"{i}.")
        content = str(result.get("content", ""))
        if len(content) > 200:
            content = content[:197] + "..."
        console.print(f"   {content}")
        if result.get("document_id"):
            line = f"   Document: {result['document_id']}"
            if result.get("chunk_id"):
                line += f" (Chunk: {result['chunk_id']})"
            console.print(line)
        if result.get("metadata"):
            meta = " ".join(f"{k}={v}" for k, v in result["metadata"].items())
            console.print(f"   Metadata: {meta}")
        console.print()


@app.command("graph")
def graph_search(
    ctx: typer.Context,
    entity: Optional[str] = typer.Option(
        None, "--entity", help="Search for specific entity"
    ),
    relationship: Optional[str] = typer.Option(
        None,
        "--relationship",
        help="Search for specific relationship type",
    ),
    query: Optional[str] = typer.Option(None, "--query", help="Raw graph query"),
    limit: int = typer.Option(50, "--limit", help="Maximum number of results"),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (table, json, cypher)",
    ),
) -> None:
    """Search the knowledge graph."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    if not any([entity, relationship, query]):
        console.print(
            "[red]At least one of --entity, --relationship, or --query must be specified[/red]"
        )
        raise typer.Exit(code=1)

    req = {
        "entity": entity,
        "relationship": relationship,
        "query": query,
        "limit": limit,
    }

    try:
        result = client.request("POST", "/api/v4/search/graph", json_body=req)
    except APIError as exc:
        console.print(f"[red]Graph search failed: {exc}[/red]")
        raise typer.Exit(code=1)

    nodes = result.get("nodes") or []
    edges = result.get("edges") or []
    if not nodes and not edges:
        console.print("No results found")
        return

    if output == "json":
        console.print_json(data=result)
        return
    if output == "cypher":
        console.print("// Nodes")
        for node in nodes:
            props = ", ".join(
                f"{k}: '{v}'" for k, v in (node.get("properties") or {}).items()
            )
            if props:
                console.print(f"({node.get('id')}:{node.get('type')} {{{props}}})")
            else:
                console.print(f"({node.get('id')}:{node.get('type')})")
        console.print("\n// Relationships")
        for edge in edges:
            console.print(
                f"({edge.get('source')})-[:{edge.get('type')}]->({edge.get('target')})"
            )
        return

    console.print("[bold cyan]Knowledge Graph Results[/bold cyan]")
    if nodes:
        console.print(f"\nNodes ({len(nodes)}):")
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID")
        table.add_column("Type")
        table.add_column("Properties")
        for node in nodes:
            props = ", ".join(
                f"{k}={v}" for k, v in (node.get("properties") or {}).items()
            )
            table.add_row(str(node.get("id", "")), node.get("type", ""), props)
        console.print(table)

    if edges:
        console.print(f"\nRelationships ({len(edges)}):")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Source")
        table.add_column("Type")
        table.add_column("Target")
        for edge in edges:
            table.add_row(
                str(edge.get("source", "")),
                edge.get("type", ""),
                str(edge.get("target", "")),
            )
        console.print(table)
