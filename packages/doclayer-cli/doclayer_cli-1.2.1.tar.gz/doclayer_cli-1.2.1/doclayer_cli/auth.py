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


def _validate_password(password: str) -> bool:
    """Validate password meets requirements."""
    if len(password) < 8:
        return False
    if len(password) > 128:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit


@app.command("register")
def register(
    ctx: typer.Context,
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        help="Configuration profile to use",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        help="Email address for registration",
    ),
    password: Optional[str] = typer.Option(
        None,
        "--password",
        help="Password for registration (min 8 chars, must contain uppercase, lowercase, and digit)",
    ),
    first_name: Optional[str] = typer.Option(
        None,
        "--first-name",
        help="First name",
    ),
    last_name: Optional[str] = typer.Option(
        None,
        "--last-name",
        help="Last name",
    ),
    org_name: Optional[str] = typer.Option(
        None,
        "--org-name",
        help="Organization name",
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
    """Register a new Doclayer account."""
    cfg, prof, _ = _get_context(ctx)

    # Resolve profile
    if profile:
        prof = cfg.get_profile(profile) or Profile(name=profile)

    if api_url:
        prof.base_url = api_url.rstrip("/")
    elif not prof.base_url or prof.base_url == "http://localhost:8000":
        prof.base_url = "https://api.doclayer.ai"

    client = APIClient(base_url=prof.base_url)

    # Collect registration data
    final_email = email
    final_password = password
    final_first_name = first_name
    final_last_name = last_name
    final_org_name = org_name

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
        # Confirm password
        confirm_password = getpass.getpass("Confirm Password: ")
        if final_password != confirm_password:
            console.print("[red]Passwords do not match[/red]")
            raise typer.Exit(code=1)

    # Validate password requirements
    if not _validate_password(final_password):
        console.print(
            "[red]Password must be 8-128 characters and contain at least one uppercase letter, one lowercase letter, and one digit[/red]"
        )
        raise typer.Exit(code=1)

    if not final_first_name:
        if non_interactive:
            console.print(
                "[red]--first-name is required in non-interactive mode[/red]"
            )
            raise typer.Exit(code=1)
        final_first_name = input("First Name: ").strip()
    if not final_first_name:
        console.print("[red]First name is required[/red]")
        raise typer.Exit(code=1)

    if not final_last_name:
        if non_interactive:
            console.print(
                "[red]--last-name is required in non-interactive mode[/red]"
            )
            raise typer.Exit(code=1)
        final_last_name = input("Last Name: ").strip()
    if not final_last_name:
        console.print("[red]Last name is required[/red]")
        raise typer.Exit(code=1)

    if not final_org_name:
        if non_interactive:
            # Organization name is optional, but recommended
            pass
        else:
            final_org_name = input("Organization Name (optional): ").strip() or None

    # Prepare registration payload (camelCase for API)
    payload = {
        "email": final_email,
        "password": final_password,
        "firstName": final_first_name,
        "lastName": final_last_name,
    }
    if final_org_name:
        payload["organizationName"] = final_org_name

    try:
        resp = client.request("POST", "/api/v4/register-user", json_body=payload)
    except APIError as exc:
        error_msg = str(exc)
        if "already exists" in error_msg.lower() or "409" in error_msg:
            console.print(
                f"[red]Registration failed: A user with this email already exists[/red]"
            )
            console.print("[yellow]Try logging in instead: doclayer auth login[/yellow]")
        else:
            console.print(f"[red]Registration failed: {exc}[/red]")
        raise typer.Exit(code=1)

    # Extract token and user info
    token = resp.get("token") or resp.get("access_token")
    if not token:
        console.print("[red]Registration succeeded but no token received[/red]")
        raise typer.Exit(code=1)

    prof.token = token
    prof.api_key = None

    # Extract tenant/organization ID if available
    tenant_id = (
        resp.get("tenant_id")
        or resp.get("organization_id")
        or (resp.get("user") or {}).get("organization_id")
    )
    if tenant_id:
        prof.tenant_id = str(tenant_id)

    user_info = resp.get("user") or {}
    user_email = user_info.get("email") or final_email

    console.print(f"[green]✓ Successfully registered and logged in as {user_email}[/green]")

    # Load organization info (best-effort)
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
        # The /auth/me endpoint returns JWT claims which may not have 'email'
        # Check for email, user_id, or email in claims
        email = user.get("email") or user.get("username") or user.get("user_id")
        if email:
            console.print(f"User: [green]{email}[/green]")
        else:
            # If no email found, show user_id if available
            user_id = user.get("user_id") or user.get("id")
            if user_id:
                console.print(f"User ID: [green]{user_id}[/green]")
            else:
                console.print("[green]✓ Authenticated[/green]")
    except APIError as exc:
        console.print(f"[red]Failed to fetch user info: {exc}[/red]")


@app.command("whoami")
def whoami(ctx: typer.Context) -> None:
    """Alias for auth status (prints current user)."""
    status(ctx)
