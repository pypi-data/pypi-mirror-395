from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from .config import (
    DEFAULT_BASE_URL,
    DEFAULT_OUTPUT_FORMAT,
    Config,
    Profile,
    save_config,
)


app = typer.Typer(help="CLI configuration management")
console = Console()


def _get_ctx(ctx: typer.Context):
    from .cli import AppContext  # local import to avoid cycles

    if not isinstance(ctx.obj, AppContext):  # type: ignore[arg-type]
        console.print("[red]Internal error: CLI context not initialized[/red]")
        raise typer.Exit(code=1)
    return ctx.obj  # type: ignore[return-value]


@app.command("show")
def show(ctx: typer.Context) -> None:
    """Show current configuration."""
    app_ctx = _get_ctx(ctx)
    cfg: Config = app_ctx.config

    console.print(f"Default Profile: [cyan]{cfg.default_profile}[/cyan]")
    console.print("\nProfiles:")
    for name, profile in cfg.profiles.items():
        prefix = "* " if name == cfg.default_profile else "  "
        label = f"[green]{name}[/green]" if name == cfg.default_profile else name
        console.print(f"{prefix}{label}")
        console.print(f"    Base URL: {profile.base_url}")
        if profile.tenant_id:
            console.print(f"    Tenant ID: {profile.tenant_id}")
        if profile.default_project:
            console.print(f"    Default Project: {profile.default_project}")
        console.print(f"    Output Format: {profile.output_format}")
        if profile.api_key:
            console.print("    Auth: API Key")
        elif profile.token:
            console.print("    Auth: JWT Token")
        else:
            console.print("    Auth: Not authenticated")


@app.command("set")
def set_value(
    ctx: typer.Context,
    key: str = typer.Argument(
        ..., help="Configuration key (base-url|output-format|default-project)"
    ),
    value: str = typer.Argument(..., help="Configuration value"),
) -> None:
    """Set a configuration value on the active profile."""
    app_ctx = _get_ctx(ctx)
    cfg = app_ctx.config
    profile = cfg.get_profile(cfg.default_profile)
    if profile is None:
        console.print("[red]No default profile found[/red]")
        raise typer.Exit(code=1)

    if key == "base-url":
        profile.base_url = value
    elif key == "output-format":
        if value not in {"json", "table", "yaml"}:
            console.print("[red]output-format must be json, table, or yaml[/red]")
            raise typer.Exit(code=1)
        profile.output_format = value
    elif key == "default-project":
        profile.default_project = value
    else:
        console.print(f"[red]Unknown configuration key: {key}[/red]")
        raise typer.Exit(code=1)

    cfg.set_profile(profile)
    save_config(cfg, app_ctx.config_path)
    console.print("[green]✓ Configuration updated[/green]")


@app.command("profile")
def profile_group(ctx: typer.Context) -> None:
    """List all configuration profiles."""
    # Changed from misleading "use subcommands" message to actually listing profiles
    app_ctx = _get_ctx(ctx)
    cfg = app_ctx.config
    console.print("[bold cyan]Profiles:[/bold cyan]")
    for name in cfg.profiles:
        if name == cfg.default_profile:
            console.print(f"  [green]* {name} (default)[/green]")
        else:
            console.print(f"    {name}")
    console.print("\n[dim]Tip: Use 'doclayer config profile-use <name>' to switch profiles[/dim]")


@app.command("profile-list", hidden=True)
def profile_list_compat(ctx: typer.Context) -> None:
    """Compatibility helper for old 'config profile list' (now 'config profile list')."""
    profile_list(ctx)


@app.command("profile-list-alias", hidden=True)
def profile_list(ctx: typer.Context) -> None:
    """List configuration profiles."""
    app_ctx = _get_ctx(ctx)
    cfg = app_ctx.config
    for name in cfg.profiles:
        if name == cfg.default_profile:
            console.print(f"[green]* {name} (default)[/green]")
        else:
            console.print(f"  {name}")


@app.command("profile-use")
def profile_use(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
) -> None:
    """Switch to a different profile."""
    app_ctx = _get_ctx(ctx)
    cfg = app_ctx.config

    if profile_name not in cfg.profiles:
        console.print(f"[red]Profile {profile_name} not found[/red]")
        raise typer.Exit(code=1)

    cfg.default_profile = profile_name
    save_config(cfg, app_ctx.config_path)
    console.print(f"[green]✓ Switched to profile: {profile_name}[/green]")


@app.command("profile-delete")
def profile_delete(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
) -> None:
    """Delete a configuration profile."""
    app_ctx = _get_ctx(ctx)
    cfg = app_ctx.config

    if profile_name not in cfg.profiles:
        console.print(f"[red]Profile {profile_name} not found[/red]")
        raise typer.Exit(code=1)

    cfg.profiles.pop(profile_name, None)
    if cfg.default_profile == profile_name:
        cfg.default_profile = next(iter(cfg.profiles), "default")
    save_config(cfg, app_ctx.config_path)
    console.print(f"[green]✓ Profile deleted: {profile_name}[/green]")


def _default_profiles_path() -> Path:
    return Path(__file__).resolve().parents[1] / "config" / "profiles.yaml"


@app.command("import-profiles")
def import_profiles(
    ctx: typer.Context,
    profiles: Optional[List[str]] = typer.Option(
        None,
        "--profile",
        "-n",
        help="Specific profile names to import (default: all presets)",
    ),
    from_file: Path = typer.Option(
        _default_profiles_path(),
        "--from-file",
        help="Path to a profiles.yaml file",
    ),
    force: bool = typer.Option(False, "--force", help="Overwrite existing profiles"),
    set_default: Optional[str] = typer.Option(
        None,
        "--set-default",
        help="Profile name to set as default after import",
    ),
) -> None:
    """Import profile presets from config/profiles.yaml."""
    app_ctx = _get_ctx(ctx)
    cfg = app_ctx.config

    if not from_file.exists():
        console.print(f"[red]Profiles file not found: {from_file}[/red]")
        raise typer.Exit(code=1)

    import yaml

    payload = yaml.safe_load(from_file.read_text()) or {}
    entries = payload.get("profiles")
    if not isinstance(entries, dict) or not entries:
        console.print(f"[red]No profiles found in {from_file}[/red]")
        raise typer.Exit(code=1)

    requested = {name for name in (profiles or [])}
    imported: List[str] = []
    for name, spec in entries.items():
        if requested and name not in requested:
            continue

        if not isinstance(spec, dict):
            console.print(
                f"[yellow]Skipping profile '{name}': entry must be a mapping[/yellow]"
            )
            continue

        profile = Profile(
            name=name,
            base_url=spec.get("base_url") or DEFAULT_BASE_URL,
            tenant_id=spec.get("tenant_id"),
            default_project=spec.get("default_project"),
            output_format=spec.get("output_format") or DEFAULT_OUTPUT_FORMAT,
        )

        if not force and name in cfg.profiles:
            console.print(
                f"[yellow]Skipping existing profile '{name}'. Use --force to overwrite.[/yellow]"
            )
            continue

        cfg.set_profile(profile)
        imported.append(name)

    if not imported:
        console.print("[yellow]No profiles imported[/yellow]")
        return

    if set_default:
        if set_default not in cfg.profiles:
            console.print(
                f"[red]Cannot set default to unknown profile '{set_default}'[/red]"
            )
            raise typer.Exit(code=1)
        cfg.default_profile = set_default
    elif not cfg.default_profile:
        cfg.default_profile = imported[0]

    save_config(cfg, app_ctx.config_path)
    console.print(f"[green]✓ Imported profiles: {', '.join(imported)}[/green]")
