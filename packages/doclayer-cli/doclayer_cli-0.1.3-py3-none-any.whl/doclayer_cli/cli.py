from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .api_client import APIClient
from .config import (
    Config,
    Profile,
    env_bool,
    load_config,
    resolve_profile_name,
)
from .version import BUILD_DATE, COMMIT, VERSION


console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit when --version is passed."""
    if value:
        console.print(f"Doclayer CLI {VERSION}")
        console.print(f"Commit: {COMMIT}")
        console.print(f"Built: {BUILD_DATE}")
        raise typer.Exit()


app = typer.Typer(
    help="Doclayer CLI - Document Intelligence Platform", no_args_is_help=True
)


@dataclass
class AppContext:
    config: Config
    profile: Profile
    config_path: Optional[Path]
    client: APIClient
    verbose: bool = False


def _init_client(profile: Profile) -> APIClient:
    base_url = profile.base_url or "https://api.doclayer.ai"

    # Environment overrides
    env_base = os.getenv("DOCLAYER_BASE_URL")
    if env_base:
        base_url = env_base.rstrip("/")

    api_key = profile.api_key or os.getenv("DOCLAYER_API_KEY") or None
    token = profile.token or os.getenv("DOCLAYER_TOKEN") or None

    return APIClient(
        base_url=base_url,
        api_key=api_key,
        token=token,
        tenant_id=profile.tenant_id or None,
    )


def _ensure_authenticated(ctx: AppContext) -> None:
    if not (ctx.client.api_key or ctx.client.token):
        console.print(
            "[red]✗ Not authenticated. Please run 'doclayer auth login' or configure DOCLAYER_API_KEY.[/red]"
        )
        raise typer.Exit(code=1)


@app.callback()
def main(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Config file (default: ~/.doclayer/config.json)",
        dir_okay=False,
        readable=True,
    ),
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        "-p",
        help="Configuration profile to use",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Global entrypoint that prepares configuration and API client."""
    # Verbose can be enabled via env as well
    verbose = verbose or env_bool("DOCLAYER_VERBOSE", False)

    cfg = load_config(config)
    profile_name = resolve_profile_name(
        cfg, cli_profile=profile, env_profile=os.getenv("DOCLAYER_PROFILE")
    )
    prof = cfg.get_profile(profile_name)
    if prof is None:
        # Create a new profile with sensible defaults
        prof = Profile(name=profile_name)
        cfg.set_profile(prof)

    api_client = _init_client(prof)

    ctx.obj = AppContext(
        config=cfg,
        profile=prof,
        config_path=config,
        client=api_client,
        verbose=verbose,
    )


@app.command("version")
def version() -> None:
    """Print the version number of Doclayer CLI."""
    console.print(f"Doclayer CLI {VERSION}")
    console.print(f"Commit: {COMMIT}")
    console.print(f"Built: {BUILD_DATE}")


@app.command("completion")
def completion(
    shell: str = typer.Argument(..., help="Shell type: bash|zsh|fish|powershell")
) -> None:
    """Show instructions for enabling shell completion."""
    shell = shell.lower()
    if shell not in {"bash", "zsh", "fish", "powershell"}:
        console.print("[red]Supported shells: bash, zsh, fish, powershell[/red]")
        raise typer.Exit(code=1)

    # Typer/Click provide completion via environment variables; document that usage.
    console.print("Doclayer CLI uses Click-style completions.")
    console.print("Add one of the following lines to your shell configuration:")
    if shell == "bash":
        console.print(
            '  eval "$(_DOCLAYER_COMPLETE=bash_source doclayer)"',
            highlight=False,
        )
    elif shell == "zsh":
        console.print(
            '  eval "$(_DOCLAYER_COMPLETE=zsh_source doclayer)"',
            highlight=False,
        )
    elif shell == "fish":
        console.print(
            "  eval (env _DOCLAYER_COMPLETE=fish_source doclayer)",
            highlight=False,
        )
    else:  # powershell
        console.print(
            "  Invoke-Expression -Command (env _DOCLAYER_COMPLETE=powershell_source doclayer)",
            highlight=False,
        )


#
# Sub-command groups: auth, project, document, search, etc.
# Only core ones are wired here; detailed command behavior is implemented
# in their respective modules.
#
from . import auth as auth_commands  # noqa: E402
from . import project as project_commands  # noqa: E402
from . import document as document_commands  # noqa: E402
from . import search as search_commands  # noqa: E402
from . import billing as billing_commands  # noqa: E402
from . import workflow as workflow_commands  # noqa: E402
from . import model as model_commands  # noqa: E402
from . import agent as agent_commands  # noqa: E402
from . import template_cli as template_commands  # noqa: E402
from . import config_cli as config_commands  # noqa: E402
from . import local_cli as local_commands  # noqa: E402
from . import ingest as ingest_commands  # noqa: E402
from . import status as status_commands  # noqa: E402


app.add_typer(auth_commands.app, name="auth")
app.add_typer(agent_commands.app, name="agent")
app.add_typer(billing_commands.app, name="billing")
app.add_typer(model_commands.app, name="model")
app.add_typer(project_commands.app, name="project")
app.add_typer(document_commands.app, name="document")
app.add_typer(workflow_commands.app, name="workflow")
app.add_typer(search_commands.app, name="search")
app.add_typer(template_commands.app, name="template")
app.add_typer(local_commands.app, name="local")
app.add_typer(config_commands.app, name="config")
app.add_typer(ingest_commands.app, name="ingest")
app.add_typer(status_commands.app, name="status")
