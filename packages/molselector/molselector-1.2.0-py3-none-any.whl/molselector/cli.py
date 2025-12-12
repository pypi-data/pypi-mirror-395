"""Command line interface for launching MolSelector."""
from __future__ import annotations

import os
from importlib import metadata
from pathlib import Path
from typing import List, Optional

import typer
import uvicorn


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

cli = typer.Typer(help="Utilities for running the MolSelector web app.")


def _version_callback(value: bool) -> None:
    """Print the installed package version and exit."""

    if not value:
        return

    try:
        version = metadata.version("molselector")
    except metadata.PackageNotFoundError:
        version = "unknown"

    typer.echo(version)
    raise typer.Exit()


@cli.callback()
def _root_command(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the MolSelector version and exit.",
    ),
) -> None:
    """MolSelector command line utilities."""

    # The callback is used only for eager options like --version.


@cli.command()
def launch(
    host: str = typer.Option(
        DEFAULT_HOST,
        help="Interface to bind the server to.",
    ),
    port: int = typer.Option(
        DEFAULT_PORT,
        min=1,
        max=65535,
        help="Port to serve the application on.",
    ),
    reload: bool = typer.Option(
        False,
        "--reload/--no-reload",
        help="Enable auto-reload on code changes (development only).",
    ),
    reload_dir: Optional[List[Path]] = typer.Option(
        None,
        "--reload-dir",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Additional directories to watch when reloading.",
    ),
    log_level: str = typer.Option(
        "info",
        help="Log level to use for Uvicorn.",
    ),
    xyz_folder: Optional[Path] = typer.Option(
        None,
        "--xyz-folder",
        file_okay=False,
        dir_okay=True,
        exists=True,
        resolve_path=True,
        help="Folder containing molecule files to preload when the app starts.",
    ),
) -> None:
    """Launch the MolSelector web application using Uvicorn."""

    reload_dirs: Optional[List[str]]
    if reload_dir:
        reload_dirs = [str(path) for path in reload_dir]
    else:
        reload_dirs = None

    if xyz_folder is not None:
        os.environ["MOLSELECTOR_DEFAULT_FOLDER"] = str(xyz_folder)

    uvicorn.run(
        "molselector.app:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=reload_dirs,
        log_level=log_level,
    )


def main() -> None:  # pragma: no cover - console entrypoint
    """Invoke the Typer CLI."""

    cli()


__all__ = ["cli", "main"]
