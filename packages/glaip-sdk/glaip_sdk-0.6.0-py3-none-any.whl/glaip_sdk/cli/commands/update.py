"""Update command for upgrading the glaip-sdk package.

Author:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence

import click
from rich.console import Console

from glaip_sdk.branding import ACCENT_STYLE, ERROR_STYLE, INFO_STYLE, SUCCESS_STYLE

PACKAGE_NAME = "glaip-sdk"


def _build_upgrade_command(include_prerelease: bool) -> Sequence[str]:
    """Return the pip command used to upgrade the SDK."""
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        PACKAGE_NAME,
    ]
    if include_prerelease:
        command.append("--pre")
    return command


@click.command(name="update")
@click.option(
    "--pre",
    "include_prerelease",
    is_flag=True,
    help="Include pre-release versions when upgrading.",
)
def update_command(include_prerelease: bool) -> None:
    """Upgrade the glaip-sdk package using pip."""
    console = Console()
    upgrade_cmd = _build_upgrade_command(include_prerelease)
    console.print(f"[{ACCENT_STYLE}]Upgrading {PACKAGE_NAME} using[/] [{INFO_STYLE}]{' '.join(upgrade_cmd)}[/]")

    try:
        subprocess.run(upgrade_cmd, check=True)
    except FileNotFoundError as exc:
        raise click.ClickException(
            "Unable to locate Python executable to run pip. Please ensure Python is installed and try again."
        ) from exc
    except subprocess.CalledProcessError as exc:
        console.print(
            f"[{ERROR_STYLE}]Automatic upgrade failed.[/] Please run `pip install -U {PACKAGE_NAME}` manually."
        )
        raise click.ClickException("Automatic upgrade failed.") from exc

    console.print(f"[{SUCCESS_STYLE}]✅ {PACKAGE_NAME} upgraded successfully.[/]")
