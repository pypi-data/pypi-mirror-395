from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIError


app = typer.Typer(help="Tenant model configuration")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("config")
def config_cmd(ctx: typer.Context) -> None:
    """View current model configuration."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        config = client.request("GET", "/api/v4/models/config")
    except APIError as exc:
        console.print(f"[red]Failed to get model config: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[bold cyan]Current Model Configuration[/bold cyan]\n")
    console.print(f"LLM Provider: [yellow]{config.get('llm_provider')}[/yellow]")
    console.print(f"LLM Model: [yellow]{config.get('llm_model_id')}[/yellow]")
    console.print(
        f"Embedding Provider: [yellow]{config.get('embedding_provider')}[/yellow]"
    )
    console.print(
        f"Embedding Model: [yellow]{config.get('embedding_model_id')}[/yellow]"
    )


@app.command("set-llm")
def set_llm(
    ctx: typer.Context,
    provider: str = typer.Option(
        ..., "--provider", help="LLM provider (mistral, gemini, openai)"
    ),
    model: str = typer.Option(..., "--model", help="Model ID"),
) -> None:
    """Set LLM configuration."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    valid_providers = {"mistral", "gemini", "openai"}
    if provider not in valid_providers:
        console.print(
            f"[red]Invalid provider: {provider} (must be one of: {', '.join(sorted(valid_providers))})[/red]"
        )
        raise typer.Exit(code=1)

    payload = {"provider": provider, "model_id": model}
    try:
        client.request("PUT", "/api/v4/models/llm", json_body=payload)
    except APIError as exc:
        console.print(f"[red]Failed to update LLM config: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[green]✓ LLM configuration updated successfully[/green]")
    console.print(f"Provider: {provider}")
    console.print(f"Model: {model}")


@app.command("set-embedding")
def set_embedding(
    ctx: typer.Context,
    provider: str = typer.Option(..., "--provider", help="Embedding provider"),
    model: str = typer.Option(..., "--model", help="Model ID"),
) -> None:
    """Set embedding model configuration."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    payload = {"provider": provider, "model_id": model}
    try:
        client.request("PUT", "/api/v4/models/embedding", json_body=payload)
    except APIError as exc:
        console.print(f"[red]Failed to update embedding config: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print("[green]✓ Embedding configuration updated successfully[/green]")
    console.print(f"Provider: {provider}")
    console.print(f"Model: {model}")


@app.command("list")
def list_models(
    ctx: typer.Context,
    provider: str = typer.Option("", "--provider", help="Filter by provider"),
) -> None:
    """List available models."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    path = "/api/v4/models/available"
    params = {"provider": provider} if provider else None

    try:
        resp = client.request("GET", path, params=params)
    except APIError as exc:
        console.print(f"[red]Failed to list models: {exc}[/red]")
        raise typer.Exit(code=1)

    models = resp.get("models") or []
    if not models:
        console.print("No models found")
        return

    by_provider: dict[str, list[dict]] = {}
    for m in models:
        by_provider.setdefault(m.get("provider", "unknown"), []).append(m)

    for prov, items in by_provider.items():
        console.print(f"[bold cyan]{prov.title()} Models[/bold cyan]")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Model ID")
        table.add_column("Type")
        table.add_column("Cost/M Tokens")
        table.add_column("Description")

        for m in items:
            cost_val = m.get("cost_per_million_tokens", 0) or 0
            cost = "-" if not cost_val else f"${cost_val:.3f}"
            desc = m.get("description") or ""
            if len(desc) > 40:
                desc = desc[:37] + "..."
            table.add_row(
                m.get("model_id", ""),
                m.get("type", ""),
                cost,
                desc,
            )

        console.print(table)
        console.print()


@app.command("test")
def test_model(
    ctx: typer.Context,
    text: str = typer.Argument(..., help="Sample text to send to model"),
    provider: Optional[str] = typer.Option(
        None,
        "--provider",
        help="Provider override",
    ),
    model_id: Optional[str] = typer.Option(
        None,
        "--model",
        help="Model ID override",
    ),
) -> None:
    """Test model configuration with a sample text."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    payload = {"text": text}
    if provider:
        payload["provider"] = provider
    if model_id:
        payload["model_id"] = model_id

    try:
        resp = client.request("POST", "/api/v4/models/test", json_body=payload)
    except APIError as exc:
        console.print(f"[red]Failed to test model: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print(
        "[green]✓ Model test successful[/green]"
        if resp.get("success")
        else "[yellow]Model test completed[/yellow]"
    )
    console.print(f"Response Time: {resp.get('response_time_ms')} ms")
    if resp.get("token_count") is not None:
        console.print(f"Token Count: {resp.get('token_count')}")
    if resp.get("output"):
        console.print("\nOutput:")
        console.print(resp["output"])
