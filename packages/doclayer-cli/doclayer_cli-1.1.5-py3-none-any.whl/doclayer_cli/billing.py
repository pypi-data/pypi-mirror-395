from __future__ import annotations


import typer
from rich.console import Console
from rich.table import Table

from .api_client import APIError


app = typer.Typer(help="Usage tracking and billing information")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("usage")
def usage(
    ctx: typer.Context,
    period: str = typer.Option(
        "",
        "--period",
        help="Period (YYYY-MM format, default: current month)",
    ),
    output: str = typer.Option(
        "table",
        "--output",
        help="Output format (table, json)",
    ),
) -> None:
    """View detailed usage breakdown."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    # For parity with Go, first attempt trial usage; here we go straight to billing usage.
    try:
        usage = client.request(
            "GET",
            "/api/v4/billing/usage",
            params={"period": period} if period else None,
        )
    except APIError as exc:
        console.print(f"[red]Failed to get usage: {exc}[/red]")
        raise typer.Exit(code=1)

    if output == "json":
        console.print_json(data=usage)
        return

    console.print(f"[bold cyan]Usage Summary - {usage.get('period')}[/bold cyan]\n")
    console.print(f"Vendor Cost: [yellow]${usage.get('vendor_cost', 0):.2f}[/yellow]")
    tier = usage.get("current_tier") or {}
    console.print(
        f"Markup ({tier.get('markup_percentage', 0)}%): "
        f"[yellow]${usage.get('markup', 0):.2f}[/yellow]"
    )
    console.print(f"Platform Fee: [yellow]${usage.get('platform_fee', 0):.2f}[/yellow]")
    console.print(
        f"Total Cost: [bold green]${usage.get('total_cost', 0):.2f}[/bold green]"
    )

    if usage.get("usage_by_model"):
        console.print("\nUsage by Model:")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Provider")
        table.add_column("Model")
        table.add_column("Input Tokens")
        table.add_column("Output Tokens")
        table.add_column("Total Tokens")
        table.add_column("Cost")
        for m in usage["usage_by_model"].values():
            table.add_row(
                m.get("provider", ""),
                m.get("model", ""),
                f"{m.get('input_tokens', 0):,}",
                f"{m.get('output_tokens', 0):,}",
                f"{m.get('total_tokens', 0):,}",
                f"${m.get('cost', 0):.2f}",
            )
        console.print(table)


@app.command("history")
def history(
    ctx: typer.Context,
    limit: int = typer.Option(12, "--limit", help="Number of months to show"),
) -> None:
    """View billing history."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        hist = client.request("GET", "/api/v4/billing/history", params={"limit": limit})
    except APIError as exc:
        console.print(f"[red]Failed to get billing history: {exc}[/red]")
        raise typer.Exit(code=1)

    months = hist.get("months") or []
    if not months:
        console.print("No billing history found")
        return

    console.print("[bold cyan]Billing History[/bold cyan]\n")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Period")
    table.add_column("Total")
    table.add_column("Vendor")
    table.add_column("Markup")
    table.add_column("Platform")
    table.add_column("Tier")
    table.add_column("Status")

    for m in months:
        table.add_row(
            m.get("period", ""),
            f"${m.get('total_cost', 0):.2f}",
            f"${m.get('vendor_cost', 0):.2f}",
            f"${m.get('markup', 0):.2f}",
            f"${m.get('platform_fee', 0):.2f}",
            m.get("tier", ""),
            m.get("status", ""),
        )

    console.print(table)


@app.command("tier")
def tier(ctx: typer.Context) -> None:
    """View current tier information."""
    app_ctx = _get_ctx(ctx)
    client = app_ctx.client

    try:
        tier = client.request("GET", "/api/v4/billing/tier")
    except APIError as exc:
        console.print(f"[red]Failed to get tier info: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold cyan]Current Tier: {tier.get('name')}[/bold cyan]\n")
    console.print(f"Platform Fee: ${tier.get('platform_fee', 0):.2f}/month")
    console.print(f"Markup: {tier.get('markup_percentage', 0):.0f}%")
    console.print(f"Rate Limit: {tier.get('rate_limit', 0)} requests/minute")
    console.print(f"Concurrent Workflows: {tier.get('concurrent_limit', 0)}")
