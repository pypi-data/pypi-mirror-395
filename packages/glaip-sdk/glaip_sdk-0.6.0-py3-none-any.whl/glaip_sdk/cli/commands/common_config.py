"""Shared helpers for configuration/account flows."""

import click
from rich.console import Console
from rich.text import Text

from glaip_sdk import Client
from glaip_sdk.branding import PRIMARY, SUCCESS_STYLE, WARNING_STYLE, AIPBranding
from glaip_sdk.cli.utils import sdk_version


def render_branding_header(console: Console, rule_text: str) -> None:
    """Render the standard CLI branding header with a custom rule text."""
    branding = AIPBranding.create_from_sdk(sdk_version=sdk_version(), package_name="glaip-sdk")
    heading = "[bold]>_ GDP Labs AI Agents Package (AIP CLI)[/bold]"
    console.print(heading)
    console.print()
    console.print(branding.get_welcome_banner())
    console.rule(rule_text, style=PRIMARY)


def check_connection(
    api_url: str,
    api_key: str,
    console: Console,
    *,
    abort_on_error: bool = False,
    extra_hint: str | None = None,
) -> bool:
    """Test connectivity and report results.

    Returns True on success, False on handled failures. Raises click.Abort when
    abort_on_error is True and a fatal error occurs.
    """
    console.print("\n🔌 Testing connection...")
    client: Client | None = None
    try:
        # Import lazily so test patches targeting glaip_sdk.Client are honored
        from importlib import import_module  # noqa: PLC0415

        client_module = import_module("glaip_sdk")
        client = client_module.Client(api_url=api_url, api_key=api_key)
        try:
            agents = client.list_agents()
            console.print(Text(f"✅ Connection successful! Found {len(agents)} agents", style=SUCCESS_STYLE))
            return True
        except Exception as exc:  # pragma: no cover - API failures depend on network
            console.print(Text(f"⚠️  Connection established but API call failed: {exc}", style=WARNING_STYLE))
            console.print("   You may need to check your API permissions or network access")
            if extra_hint:
                console.print(extra_hint)
            if abort_on_error:
                raise click.Abort() from exc
            return False
    except Exception as exc:
        console.print(Text(f"❌ Connection failed: {exc}"))
        console.print("   Please check your API URL and key")
        if extra_hint:
            console.print(extra_hint)
        if abort_on_error:
            raise click.Abort() from exc
        return False
    finally:
        if client is not None:
            client.close()
