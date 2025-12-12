from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

import typer
from rich.console import Console


app = typer.Typer(
    help="Local development environment management (docker-compose based)"
)
console = Console()


def _project_root() -> Path:
    # Heuristic: walk up until we find docker-compose.yml
    path = Path.cwd()
    for parent in [path, *path.parents]:
        if (parent / "docker-compose.yml").exists():
            return parent
    return path


def _run_compose(args: List[str]) -> int:
    root = _project_root()
    cmd = ["docker", "compose", "-f", str(root / "docker-compose.yml"), *args]
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")
    try:
        return subprocess.call(cmd)
    except FileNotFoundError:
        console.print("[red]docker compose not found. Please install Docker.[/red]")
        return 1


@app.command("status")
def status() -> None:
    """Show local docker-compose service status."""
    code = _run_compose(["ps"])
    raise typer.Exit(code=code)


@app.command("start")
def start(
    services: List[str] = typer.Argument(
        None, help="Optional list of services to start"
    ),
    detach: bool = typer.Option(True, "--detach", "-d", help="Run in detached mode"),
) -> None:
    """Start local development services."""
    args = ["up"]
    if detach:
        args.append("-d")
    args.extend(services or [])
    code = _run_compose(args)
    raise typer.Exit(code=code)


@app.command("stop")
def stop(
    services: List[str] = typer.Argument(
        None, help="Optional list of services to stop"
    ),
    volumes: bool = typer.Option(
        False, "--volumes", help="Remove volumes when stopping"
    ),
) -> None:
    """Stop local development services."""
    args = ["down"]
    if volumes:
        args.append("--volumes")
    if services:
        # docker compose down does not accept services; use stop when given services
        args = ["stop", *services]
    code = _run_compose(args)
    raise typer.Exit(code=code)


@app.command("logs")
def logs(
    service: str = typer.Argument("", help="Service name (optional)"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output"),
    tail: str = typer.Option("100", "--tail", help="Number of lines to show"),
) -> None:
    """Show logs from local services."""
    args = ["logs", "--tail", tail]
    if follow:
        args.append("--follow")
    if service:
        args.append(service)
    code = _run_compose(args)
    raise typer.Exit(code=code)


@app.command("reset")
def reset(
    force: bool = typer.Option(False, "--force", help="Skip confirmation prompt"),
) -> None:
    """Reset local development environment (stop + remove containers/volumes)."""
    if not force:
        answer = (
            input("This will stop containers and remove volumes. Continue? [y/N]: ")
            .strip()
            .lower()
        )
        if answer not in {"y", "yes"}:
            console.print("[yellow]Aborted[/yellow]")
            raise typer.Exit(code=0)

    code = _run_compose(["down", "--volumes"])
    raise typer.Exit(code=code)
