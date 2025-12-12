from __future__ import annotations

import getpass
from typing import Optional

import typer
from rich.console import Console

from .api_client import APIClient, APIError
from .config import Config, Profile, save_config


app = typer.Typer(help="Authentication commands")
console = Console()


def _get_context(ctx: typer.Context) -> tuple[Config, Profile, APIClient]:
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj.config, ctx.obj.profile, ctx.obj.client  # type: ignore[return-value]


@app.command("login")
def login(
    ctx: typer.Context,
    api_key: bool = typer.Option(
        False,
        "--api-key",
        help="Use API key authentication instead of email/password",
    ),
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        help="Configuration profile to use",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        help="Email address for login",
    ),
    password: Optional[str] = typer.Option(
        None,
        "--password",
        help="Password for login",
    ),
    api_key_value: Optional[str] = typer.Option(
        None,
        "--api-key-value",
        help="API key value (alternative to --api-key flag)",
    ),
    api_url: Optional[str] = typer.Option(
        None,
        "--api-url",
        help="API URL (defaults to https://api.doclayer.ai)",
    ),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Run in non-interactive mode (requires all parameters)",
    ),
) -> None:
    """Authenticate with Doclayer using email/password or API key."""
    cfg, prof, _ = _get_context(ctx)

    # Resolve profile
    if profile:
        prof = cfg.get_profile(profile) or Profile(name=profile)

    if api_url:
        prof.base_url = api_url.rstrip("/")
    elif not prof.base_url or prof.base_url == "http://localhost:8000":
        prof.base_url = (
            "https://api.doclayer.ai" if non_interactive else "https://api.doclayer.ai"
        )

    client = APIClient(base_url=prof.base_url)

    if api_key or api_key_value:
        final_key = api_key_value
        if not final_key:
            if non_interactive:
                console.print(
                    "[red]--api-key-value is required in non-interactive mode[/red]"
                )
                raise typer.Exit(code=1)
            final_key = getpass.getpass("API Key: ")
        if not final_key or not final_key.startswith("dly_"):
            console.print("[red]Invalid API key format[/red]")
            raise typer.Exit(code=1)

        client.api_key = final_key
        try:
            user = client.request("GET", "/api/v4/auth/me")
        except APIError as exc:
            console.print(f"[red]Invalid API key: {exc}[/red]")
            raise typer.Exit(code=1)

        prof.api_key = final_key
        prof.token = None
        console.print(
            f"[green]✓ Successfully authenticated as {user.get('email')}[/green]"
        )
    else:
        # Email / password login
        final_email = email
        final_password = password

        if not final_email:
            if non_interactive:
                console.print("[red]--email is required in non-interactive mode[/red]")
                raise typer.Exit(code=1)
            final_email = input("Email: ").strip()
        if "@" not in final_email:
            console.print("[red]Invalid email format[/red]")
            raise typer.Exit(code=1)

        if not final_password:
            if non_interactive:
                console.print(
                    "[red]--password is required in non-interactive mode[/red]"
                )
                raise typer.Exit(code=1)
            final_password = getpass.getpass("Password: ")

        payload = {"email": final_email, "password": final_password}
        try:
            resp = client.request("POST", "/api/v4/auth/login", json_body=payload)
        except APIError as exc:
            console.print(f"[red]Login failed: {exc}[/red]")
            raise typer.Exit(code=1)

        prof.token = resp.get("token")
        prof.api_key = None
        user = resp.get("user") or {}
        console.print(f"[green]✓ Successfully logged in as {user.get('email')}[/green]")

    # Load organization info (best-effort)
    client.api_key = prof.api_key
    client.token = prof.token
    try:
        org = client.request("GET", "/api/v4/auth/organization")
        if org:
            prof.tenant_id = org.get("id") or prof.tenant_id
            console.print(f"[cyan]  Organization: {org.get('name')}[/cyan]")
    except APIError:
        pass

    cfg.set_profile(prof)
    save_config(cfg, ctx.obj.config_path)  # type: ignore[arg-type]


@app.command("logout")
def logout(
    ctx: typer.Context,
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        help="Configuration profile to use",
    ),
) -> None:
    """Logout from Doclayer (clears stored credentials)."""
    cfg, prof, client = _get_context(ctx)

    if profile:
        prof = cfg.get_profile(profile) or prof

    # Best-effort server-side logout
    try:
        client.request("POST", "/api/v4/auth/logout")
    except APIError:
        # Ignore failure; local credentials will still be cleared
        pass

    prof.api_key = None
    prof.token = None
    cfg.set_profile(prof)
    save_config(cfg, ctx.obj.config_path)  # type: ignore[arg-type]

    console.print("[green]✓ Logged out[/green]")


@app.command("status")
def status(ctx: typer.Context) -> None:
    """Show current authentication status."""
    cfg, prof, client = _get_context(ctx)
    if not (client.api_key or client.token):
        console.print("[yellow]Not authenticated[/yellow]")
        raise typer.Exit(code=0)

    console.print(f"Profile: [cyan]{prof.name}[/cyan]")
    console.print(f"Base URL: [cyan]{prof.base_url}[/cyan]")
    try:
        user = client.request("GET", "/api/v4/auth/me")
        console.print(f"User: [green]{user.get('email')}[/green]")
    except APIError as exc:
        console.print(f"[red]Failed to fetch user info: {exc}[/red]")


@app.command("whoami")
def whoami(ctx: typer.Context) -> None:
    """Alias for auth status (prints current user)."""
    status(ctx)
