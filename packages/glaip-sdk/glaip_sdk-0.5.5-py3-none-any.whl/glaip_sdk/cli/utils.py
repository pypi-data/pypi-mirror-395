"""CLI utilities for glaip-sdk.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
"""

from __future__ import annotations

import asyncio
import importlib
import json
import logging
import os
import re
import sys
from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager, contextmanager, nullcontext
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import click
import yaml
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.syntax import Syntax

from glaip_sdk import _version as _version_module
from glaip_sdk.branding import (
    ACCENT_STYLE,
    SUCCESS_STYLE,
    WARNING_STYLE,
)
from glaip_sdk.cli import display as cli_display
from glaip_sdk.cli import masking, pager
from glaip_sdk.cli.config import load_config
from glaip_sdk.cli.constants import LITERAL_STRING_THRESHOLD, TABLE_SORT_ENABLED
from glaip_sdk.cli.context import (
    _get_view,
    get_ctx_value,
)
from glaip_sdk.cli.context import (
    detect_export_format as _detect_export_format,
)
from glaip_sdk.cli.hints import command_hint
from glaip_sdk.cli.io import export_resource_to_file_with_validation
from glaip_sdk.cli.rich_helpers import markup_text, print_markup
from glaip_sdk.icons import ICON_AGENT
from glaip_sdk.rich_components import AIPPanel, AIPTable
from glaip_sdk.utils import format_datetime, is_uuid
from glaip_sdk.utils.rendering.renderer import (
    CapturingConsole,
    RendererFactoryOptions,
    RichStreamRenderer,
    make_default_renderer,
    make_verbose_renderer,
)

questionary = None  # type: ignore[assignment]


def _load_questionary_module() -> tuple[Any | None, Any | None]:
    """Return the questionary module and Choice class if available."""
    module = questionary
    if module is not None:
        return module, getattr(module, "Choice", None)

    try:  # pragma: no cover - optional dependency
        module = __import__("questionary")
    except ImportError:
        return None, None

    return module, getattr(module, "Choice", None)


def _make_questionary_choice(choice_cls: Any | None, **kwargs: Any) -> Any:
    """Create a questionary Choice instance or lightweight fallback."""
    if choice_cls is None:
        return kwargs
    return choice_cls(**kwargs)


@contextmanager
def bind_slash_session_context(ctx: Any, session: Any) -> Any:
    """Temporarily attach a slash session to the Click context.

    Args:
        ctx: Click context object.
        session: SlashSession instance to bind.

    Yields:
        None - context manager for use in with statement.
    """
    ctx_obj = getattr(ctx, "obj", None)
    has_context = isinstance(ctx_obj, dict)
    previous_session = ctx_obj.get("_slash_session") if has_context else None
    if has_context:
        ctx_obj["_slash_session"] = session
    try:
        yield
    finally:
        if has_context:
            if previous_session is None:
                ctx_obj.pop("_slash_session", None)
            else:
                ctx_obj["_slash_session"] = previous_session


def restore_slash_session_context(ctx_obj: dict[str, Any], previous_session: Any | None) -> None:
    """Restore slash session context after operation.

    Args:
        ctx_obj: Click context obj dictionary.
        previous_session: Previous session to restore, or None to remove.
    """
    if previous_session is None:
        ctx_obj.pop("_slash_session", None)
    else:
        ctx_obj["_slash_session"] = previous_session


def handle_best_effort_check(
    check_func: Callable[[], None],
) -> None:
    """Handle best-effort duplicate/existence checks with proper exception handling.

    Args:
        check_func: Function that performs the check and raises ClickException if duplicate found.
    """
    try:
        check_func()
    except click.ClickException:
        raise
    except Exception:
        # Non-fatal: best-effort duplicate check
        pass


def prompt_export_choice_questionary(
    default_path: Path,
    default_display: str,
) -> tuple[str, Path | None] | None:
    """Prompt user for export destination using questionary with numeric shortcuts.

    Args:
        default_path: Default export path.
        default_display: Formatted display string for default path.

    Returns:
        Tuple of (choice, path) or None if cancelled/unavailable.
        Choice can be "default", "custom", or "cancel".
    """
    questionary_module, choice_cls = _load_questionary_module()
    if questionary_module is None or choice_cls is None:
        return None

    try:
        question = questionary_module.select(
            "Export transcript",
            choices=[
                _make_questionary_choice(
                    choice_cls,
                    title=f"Save to default ({default_display})",
                    value=("default", default_path),
                    shortcut_key="1",
                ),
                _make_questionary_choice(
                    choice_cls,
                    title="Choose a different path",
                    value=("custom", None),
                    shortcut_key="2",
                ),
                _make_questionary_choice(
                    choice_cls,
                    title="Cancel",
                    value=("cancel", None),
                    shortcut_key="3",
                ),
            ],
            use_shortcuts=True,
            instruction="Press 1-3 (or arrows) then Enter.",
        )
        answer = questionary_safe_ask(question)
    except Exception:
        return None

    if answer is None:
        return ("cancel", None)
    return answer


def questionary_safe_ask(question: Any, *, patch_stdout: bool = False) -> Any:
    """Run `questionary.Question` safely even when an asyncio loop is active."""
    ask_fn = getattr(question, "unsafe_ask", None)
    if not callable(ask_fn):
        raise RuntimeError("Questionary prompt is missing unsafe_ask()")

    if not _asyncio_loop_running():
        return ask_fn(patch_stdout=patch_stdout)

    return _run_questionary_in_thread(question, patch_stdout=patch_stdout)


def _asyncio_loop_running() -> bool:
    """Return True when an asyncio event loop is already running."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


def _run_questionary_in_thread(question: Any, *, patch_stdout: bool = False) -> Any:
    """Execute a questionary prompt in a background thread."""
    if getattr(question, "should_skip_question", False):
        return getattr(question, "default", None)

    application = getattr(question, "application", None)
    run_callable = getattr(application, "run", None) if application is not None else None
    if callable(run_callable):
        try:
            if patch_stdout and pt_patch_stdout is not None:
                with pt_patch_stdout():
                    return run_callable(in_thread=True)
            return run_callable(in_thread=True)
        except TypeError:
            pass

    return question.unsafe_ask(patch_stdout=patch_stdout)


class _LiteralYamlDumper(yaml.SafeDumper):
    """YAML dumper that emits literal scalars for multiline strings."""


def _literal_str_representer(dumper: yaml.Dumper, data: str) -> yaml.nodes.ScalarNode:
    """Represent strings in YAML, using literal blocks for verbose values."""
    needs_literal = "\n" in data or "\r" in data
    if not needs_literal and LITERAL_STRING_THRESHOLD and len(data) >= LITERAL_STRING_THRESHOLD:  # pragma: no cover
        needs_literal = True

    style = "|" if needs_literal else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_LiteralYamlDumper.add_representer(str, _literal_str_representer)

# Optional interactive deps (fuzzy palette)
try:
    from prompt_toolkit.buffer import Buffer
    from prompt_toolkit.completion import Completion
    from prompt_toolkit.patch_stdout import patch_stdout as pt_patch_stdout
    from prompt_toolkit.selection import SelectionType
    from prompt_toolkit.shortcuts import PromptSession, prompt

    _HAS_PTK = True
except Exception:  # pragma: no cover - optional dependency
    Buffer = None  # type: ignore[assignment]
    SelectionType = None  # type: ignore[assignment]
    PromptSession = None  # type: ignore[assignment]
    prompt = None  # type: ignore[assignment]
    pt_patch_stdout = None  # type: ignore[assignment]
    _HAS_PTK = False

if TYPE_CHECKING:  # pragma: no cover - import-only during type checking
    from glaip_sdk import Client

console = Console()
pager.console = console
logger = logging.getLogger("glaip_sdk.cli.utils")
_version_logger = logging.getLogger("glaip_sdk.cli.version")
_WARNED_SDK_VERSION_FALLBACK = False


# ----------------------------- Context helpers ---------------------------- #


def detect_export_format(file_path: str | os.PathLike[str]) -> str:
    """Backward-compatible proxy to `glaip_sdk.cli.context.detect_export_format`."""
    return _detect_export_format(file_path)


def format_size(num: int | None) -> str:
    """Format byte counts using short human-friendly units.

    Args:
        num: Number of bytes to format (can be None or 0)

    Returns:
        Human-readable size string (e.g., "1.5KB", "2MB")
    """
    if not num or num <= 0:
        return "0B"

    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B" or value >= 100:
                return f"{value:.0f}{unit}"
            if value >= 10:
                return f"{value:.1f}{unit}"
            return f"{value:.2f}{unit}"
        value /= 1024
    return f"{value:.1f}TB"  # pragma: no cover - defensive fallback


def parse_json_line(line: str) -> dict[str, Any] | None:
    """Parse a JSON line into a dictionary payload.

    Args:
        line: JSON line string to parse

    Returns:
        Parsed dictionary or None if parsing fails or result is not a dict
    """
    line = line.strip()
    if not line:
        return None
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def format_datetime_fields(
    data: dict[str, Any], fields: tuple[str, ...] = ("created_at", "updated_at")
) -> dict[str, Any]:
    """Format datetime fields in a data dictionary for display.

    Args:
        data: Dictionary containing the data to format
        fields: Tuple of field names to format (default: created_at, updated_at)

    Returns:
        New dictionary with formatted datetime fields
    """
    formatted = data.copy()
    for field in fields:
        if field in formatted:
            formatted[field] = format_datetime(formatted[field])
    return formatted


def fetch_resource_for_export(
    ctx: Any,
    resource: Any,
    resource_type: str,
    get_by_id_func: Callable[[str], Any],
    console_override: Console | None = None,
) -> Any:
    """Fetch full resource details for export, handling errors gracefully.

    Args:
        ctx: Click context for spinner management
        resource: Resource object to fetch details for
        resource_type: Type of resource (e.g., "MCP", "Agent", "Tool")
        get_by_id_func: Function to fetch resource by ID
        console_override: Optional console override

    Returns:
        Resource object with full details, or original resource if fetch fails
    """
    active_console = console_override or console
    resource_id = str(getattr(resource, "id", "")).strip()

    if not resource_id:
        return resource

    try:
        with spinner_context(
            ctx,
            f"[bold blue]Fetching {resource_type} details…[/bold blue]",
            console_override=active_console,
        ):
            return get_by_id_func(resource_id)
    except Exception:
        # Return original resource if fetch fails
        return resource


def handle_resource_export(
    ctx: Any,
    resource: Any,
    export_path: Path,
    resource_type: str,
    get_by_id_func: Callable[[str], Any],
    console_override: Console | None = None,
) -> None:
    """Handle resource export to file with format detection and error handling.

    Args:
        ctx: Click context for spinner management
        resource: Resource object to export
        export_path: Target file path (format detected from extension)
        resource_type: Type of resource (e.g., "agent", "tool")
        get_by_id_func: Function to fetch resource by ID
        console_override: Optional console override
    """
    active_console = console_override or console

    # Auto-detect format from file extension
    detected_format = detect_export_format(export_path)

    # Try to fetch full details for export
    full_resource = fetch_resource_for_export(
        ctx,
        resource,
        resource_type.capitalize(),
        get_by_id_func,
        console_override=active_console,
    )

    # Export the resource
    try:
        with spinner_context(
            ctx,
            f"[bold blue]Exporting {resource_type}…[/bold blue]",
            console_override=active_console,
        ):
            export_resource_to_file_with_validation(full_resource, export_path, detected_format)
    except Exception:
        cli_display.handle_rich_output(
            ctx,
            markup_text(f"[{WARNING_STYLE}]⚠️  Failed to fetch full details, using available data[/]"),
        )
        # Fallback: export with available data
        export_resource_to_file_with_validation(resource, export_path, detected_format)

    print_markup(
        f"[{SUCCESS_STYLE}]✅ {resource_type.capitalize()} exported to: {export_path} (format: {detected_format})[/]",
        console=active_console,
    )


def sdk_version() -> str:
    """Return the current SDK version, warning if metadata is unavailable."""
    version = getattr(_version_module, "__version__", None)
    if isinstance(version, str) and version:
        return version

    global _WARNED_SDK_VERSION_FALLBACK
    if not _WARNED_SDK_VERSION_FALLBACK:
        _version_logger.warning("Unable to resolve glaip-sdk version metadata; using fallback '0.0.0'.")
        _WARNED_SDK_VERSION_FALLBACK = True

    return "0.0.0"


@contextmanager
def with_client_and_spinner(
    ctx: Any,
    spinner_message: str,
    *,
    console_override: Console | None = None,
) -> Any:
    """Context manager for commands that need client and spinner.

    Args:
        ctx: Click context.
        spinner_message: Message to display in spinner.
        console_override: Optional console override.

    Yields:
        Client instance.
    """
    client = get_client(ctx)
    with spinner_context(ctx, spinner_message, console_override=console_override):
        yield client


def spinner_context(
    ctx: Any | None,
    message: str,
    *,
    console_override: Console | None = None,
    spinner: str = "dots",
    spinner_style: str = ACCENT_STYLE,
) -> AbstractContextManager[Any]:
    """Return a context manager that renders a spinner when appropriate."""
    active_console = console_override or console
    if not _can_use_spinner(ctx, active_console):
        return nullcontext()

    status = active_console.status(
        message,
        spinner=spinner,
        spinner_style=spinner_style,
    )

    if not hasattr(status, "__enter__") or not hasattr(status, "__exit__"):
        return nullcontext()

    return status


def _can_use_spinner(ctx: Any | None, active_console: Console) -> bool:
    """Check if spinner output is allowed in the current environment."""
    if ctx is not None:
        tty_enabled = bool(get_ctx_value(ctx, "tty", True))
        view = (_get_view(ctx) or "rich").lower()
        if not tty_enabled or view not in {"", "rich"}:
            return False

    if not active_console.is_terminal:
        return False

    return _stream_supports_tty(getattr(active_console, "file", None))


def _stream_supports_tty(stream: Any) -> bool:
    """Return True if the provided stream can safely render a spinner."""
    target = stream if hasattr(stream, "isatty") else sys.stdout
    try:
        return bool(target.isatty())
    except Exception:
        return False


def update_spinner(status_indicator: Any | None, message: str) -> None:
    """Update spinner text when a status indicator is active."""
    if status_indicator is None:
        return

    try:
        status_indicator.update(message)
    except Exception:  # pragma: no cover - defensive update
        pass


def stop_spinner(status_indicator: Any | None) -> None:
    """Stop an active spinner safely."""
    if status_indicator is None:
        return

    try:
        status_indicator.stop()
    except Exception:  # pragma: no cover - defensive stop
        pass


# Backwards compatibility aliases for legacy callers
_spinner_update = update_spinner
_spinner_stop = stop_spinner


# ----------------------------- Client config ----------------------------- #


def get_client(ctx: Any) -> Client:  # pragma: no cover
    """Get configured client from context and account store (ctx > account)."""
    # Import here to avoid circular import
    from glaip_sdk.cli.auth import resolve_credentials  # noqa: PLC0415

    module = importlib.import_module("glaip_sdk")
    client_class = cast("type[Client]", module.Client)
    context_config_obj = getattr(ctx, "obj", None)
    context_config = context_config_obj or {}

    account_name = context_config.get("account_name")
    api_url, api_key, _ = resolve_credentials(
        account_name=account_name,
        api_url=context_config.get("api_url"),
        api_key=context_config.get("api_key"),
    )

    if not api_url or not api_key:
        configure_hint = command_hint("accounts add", slash_command="login", ctx=ctx)
        actions: list[str] = []
        if configure_hint:
            actions.append(f"Run `{configure_hint}` to add an account profile")
        else:
            actions.append("add an account with 'aip accounts add'")
        raise click.ClickException(f"Missing api_url/api_key. {' or '.join(actions)}.")

    # Get timeout from context or config
    timeout = context_config.get("timeout")
    if timeout is None:
        raw_timeout = os.getenv("AIP_TIMEOUT", "0") or "0"
        try:
            timeout = float(raw_timeout) if raw_timeout != "0" else None
        except ValueError:
            timeout = None
    if timeout is None:
        # Fallback to legacy config
        file_config = load_config() or {}
        timeout = file_config.get("timeout")

    return client_class(
        api_url=api_url,
        api_key=api_key,
        timeout=float(timeout or 30.0),
    )


# ----------------------------- Secret masking ---------------------------- #

# ----------------------------- Fuzzy palette ----------------------------- #


def _extract_display_fields(row: dict[str, Any]) -> tuple[str, str, str, str]:
    """Extract display fields from row data."""
    name = str(row.get("name", "")).strip()
    _id = str(row.get("id", "")).strip()
    type_ = str(row.get("type", "")).strip()
    fw = str(row.get("framework", "")).strip()
    return name, _id, type_, fw


def _build_primary_parts(name: str, type_: str, fw: str) -> list[str]:
    """Build primary display parts from name, type, and framework."""
    parts = []
    if name:
        parts.append(name)
    if type_:
        parts.append(type_)
    if fw:
        parts.append(fw)
    return parts


def _get_fallback_columns(columns: list[tuple]) -> list[tuple]:
    """Get first two visible columns for fallback display."""
    return columns[:2]


def _is_standard_field(k: str) -> bool:
    """Check if field is a standard field to skip."""
    return k in ("id", "name", "type", "framework")


def _extract_fallback_values(row: dict[str, Any], columns: list[tuple]) -> list[str]:
    """Extract fallback values from columns."""
    fallback_parts = []
    for k, _hdr, _style, _w in columns:
        if _is_standard_field(k):
            continue
        val = str(row.get(k, "")).strip()
        if val:
            fallback_parts.append(val)
        if len(fallback_parts) >= 2:
            break
    return fallback_parts


def _build_display_parts(
    name: str, _id: str, type_: str, fw: str, row: dict[str, Any], columns: list[tuple]
) -> list[str]:
    """Build complete display parts list."""
    parts = _build_primary_parts(name, type_, fw)

    if not parts:
        # Use fallback columns
        fallback_columns = _get_fallback_columns(columns)
        parts.extend(_extract_fallback_values(row, fallback_columns))

    if _id:
        parts.append(f"[{_id}]")

    return parts


def _row_display(row: dict[str, Any], columns: list[tuple]) -> str:
    """Build a compact text label for the palette.

    Prefers: name • type • framework • [id] (when available)
    Falls back to first 2 columns + [id].
    """
    name, _id, type_, fw = _extract_display_fields(row)
    parts = _build_display_parts(name, _id, type_, fw, row, columns)
    return " • ".join(parts) if parts else (_id or "(row)")


def _check_fuzzy_pick_requirements() -> bool:
    """Check if fuzzy picking requirements are met."""
    return _HAS_PTK and console.is_terminal and os.isatty(1)


def _build_unique_labels(
    rows: list[dict[str, Any]], columns: list[tuple]
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    """Build unique display labels and reverse mapping."""
    labels = []
    by_label: dict[str, dict[str, Any]] = {}

    for r in rows:
        label = _row_display(r, columns)
        # Ensure uniqueness: if duplicate, suffix with …#n
        if label in by_label:
            i = 2
            base = label
            while f"{base} #{i}" in by_label:
                i += 1
            label = f"{base} #{i}"
        labels.append(label)
        by_label[label] = r

    return labels, by_label


def _basic_prompt(
    message: str,
    completer: Any,
) -> str | None:
    """Fallback prompt handler when PromptSession is unavailable or fails."""
    if prompt is None:  # pragma: no cover - optional dependency path
        return None

    try:
        return prompt(
            message=message,
            completer=completer,
            complete_in_thread=True,
            complete_while_typing=True,
        )
    except (KeyboardInterrupt, EOFError):
        return None
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("Fallback prompt failed: %s", exc)
        return None


def _prompt_with_auto_select(
    message: str,
    completer: Any,
    choices: Iterable[str],
) -> str | None:
    """Prompt with fuzzy completer that auto-selects suggested matches."""
    if not _HAS_PTK or PromptSession is None or Buffer is None or SelectionType is None:
        return _basic_prompt(message, completer)

    try:
        session = PromptSession(
            message,
            completer=completer,
            complete_in_thread=True,
            complete_while_typing=True,
            reserve_space_for_menu=8,
        )
    except Exception as exc:  # pragma: no cover - depends on prompt_toolkit
        logger.debug("PromptSession init failed (%s); falling back to basic prompt.", exc)
        return _basic_prompt(message, completer)

    buffer = session.default_buffer
    valid_choices = set(choices)

    def _auto_select(_: Buffer) -> None:
        """Auto-select text when a valid choice is entered."""
        text = buffer.text
        if not text or text not in valid_choices:
            return
        buffer.cursor_position = 0
        buffer.start_selection(selection_type=SelectionType.CHARACTERS)
        buffer.cursor_position = len(text)

    handler_attached = False
    try:
        buffer.on_text_changed += _auto_select
        handler_attached = True
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("Failed to attach auto-select handler: %s", exc)

    try:
        return session.prompt()
    except (KeyboardInterrupt, EOFError):
        return None
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("PromptSession prompt failed (%s); falling back to basic prompt.", exc)
        return _basic_prompt(message, completer)
    finally:
        if handler_attached:
            try:
                buffer.on_text_changed -= _auto_select
            except Exception:  # pragma: no cover - defensive
                pass


class _FuzzyCompleter:
    """Fuzzy completer for prompt_toolkit."""

    def __init__(self, words: list[str]) -> None:
        """Initialize fuzzy completer with word list.

        Args:
            words: List of words to complete from.
        """
        self.words = words

    def get_completions(self, document: Any, _complete_event: Any) -> Any:  # pragma: no cover
        """Get fuzzy completions for the current word, ranked by score.

        Args:
            document: Document object from prompt_toolkit.
            _complete_event: Completion event (unused).

        Yields:
            Completion objects matching the current word, in ranked order.
        """
        # Get the entire buffer text (not just word before cursor)
        buffer_text = document.text_before_cursor
        if not buffer_text or not isinstance(buffer_text, str):
            return

        # Rank labels by fuzzy score
        ranked_labels = _rank_labels(self.words, buffer_text)

        # Yield ranked completions
        for label in ranked_labels:
            # Replace entire buffer text, not just the word before cursor
            # This prevents concatenation issues with hyphenated names
            yield Completion(label, start_position=-len(buffer_text))


def _perform_fuzzy_search(answer: str, labels: list[str], by_label: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    """Perform fuzzy search fallback and return best match.

    Returns:
        Selected resource dict or None if cancelled/no match.
    """
    # Exact label match
    if answer in by_label:
        return by_label[answer]

    # Fuzzy search fallback using ranked labels
    # Check if query actually matches anything before ranking
    query_lower = answer.lower()
    has_match = False
    for label in labels:
        if _fuzzy_score(query_lower, label.lower()) >= 0:
            has_match = True
            break

    if not has_match:
        return None

    ranked_labels = _rank_labels(labels, answer)
    if ranked_labels:
        # Return the top-ranked match
        best_match = ranked_labels[0]
        if best_match in by_label:
            return by_label[best_match]

    return None


def _fuzzy_pick(
    rows: list[dict[str, Any]], columns: list[tuple], title: str
) -> dict[str, Any] | None:  # pragma: no cover - requires interactive prompt toolkit
    """Open a minimal fuzzy palette using prompt_toolkit.

    Returns the selected row (dict) or None if cancelled/missing deps.
    """
    if not _check_fuzzy_pick_requirements():
        return None

    # Build display labels and mapping
    labels, by_label = _build_unique_labels(rows, columns)

    # Create fuzzy completer
    completer = _FuzzyCompleter(labels)
    answer = _prompt_with_auto_select(
        f"Find {title.rstrip('s')}: ",
        completer,
        labels,
    )
    if answer is None:
        return None

    return _perform_fuzzy_search(answer, labels, by_label) if answer else None


def _strip_spaces_for_matching(value: str) -> str:
    """Remove whitespace from a query for consistent fuzzy matching."""
    return re.sub(r"\s+", "", value)


def _is_fuzzy_match(search: Any, target: Any) -> bool:
    """Case-insensitive fuzzy match with optional spaces; returns False for non-string inputs."""
    # Ensure search is a string
    if not isinstance(search, str) or not isinstance(target, str):
        return False

    if not search:
        return True

    # Strip spaces from search query - treat them as optional separators
    # This allows "test agent" to match "test-agent", "test_agent", etc.
    search_no_spaces = _strip_spaces_for_matching(search).lower()
    if not search_no_spaces:
        # If search is only spaces, match everything
        return True

    search_idx = 0
    for char in target.lower():
        if search_idx < len(search_no_spaces) and search_no_spaces[search_idx] == char:
            search_idx += 1
            if search_idx == len(search_no_spaces):
                return True
    return False


def _calculate_exact_match_bonus(search: str, target: str) -> int:
    """Calculate bonus for exact substring matches.

    Spaces in search are treated as optional separators (stripped before matching).
    """
    # Strip spaces from search - treat them as optional separators
    search_no_spaces = _strip_spaces_for_matching(search).lower()
    if not search_no_spaces:
        return 0
    return 100 if search_no_spaces in target.lower() else 0


def _calculate_consecutive_bonus(search: str, target: str) -> int:
    """Case-insensitive consecutive-character bonus."""
    # Strip spaces from search - treat them as optional separators
    search_no_spaces = _strip_spaces_for_matching(search).lower()
    if not search_no_spaces:
        return 0

    consecutive = 0
    max_consecutive = 0
    search_idx = 0

    for char in target.lower():
        if search_idx < len(search_no_spaces) and search_no_spaces[search_idx] == char:
            consecutive += 1
            max_consecutive = max(max_consecutive, consecutive)
            search_idx += 1
        else:
            consecutive = 0

    return max_consecutive * 10


def _calculate_length_bonus(search: str, target: str) -> int:
    """Calculate bonus for shorter search terms.

    Spaces in search are treated as optional separators (stripped before calculation).
    """
    # Strip spaces from search - treat them as optional separators
    search_no_spaces = _strip_spaces_for_matching(search)
    if not search_no_spaces:
        return 0
    return max(0, (len(target) - len(search_no_spaces)) * 2)


def _fuzzy_score(search: Any, target: str) -> int:
    """Calculate fuzzy match score.

    Higher score = better match.
    Returns -1 if no match possible.

    Args:
        search: Search string (or any type - non-strings return -1)
        target: Target string to match against
    """
    # Ensure search is a string first
    if not isinstance(search, str):
        return -1

    if not search:
        return 0

    if not _is_fuzzy_match(search, target):
        return -1  # Not a fuzzy match

    # Calculate score based on different factors
    score = 0
    score += _calculate_exact_match_bonus(search, target)
    score += _calculate_consecutive_bonus(search, target)
    score += _calculate_length_bonus(search, target)

    return score


def _extract_id_suffix(label: str) -> str:
    """Extract ID suffix from label for tie-breaking.

    Args:
        label: Display label (e.g., "name • [abc123...]")

    Returns:
        ID suffix string (e.g., "abc123") or empty string if not found
    """
    # Look for pattern like "[abc123...]" or "[abc123]"
    match = re.search(r"\[([^\]]+)\]", label)
    return match.group(1) if match else ""


def _rank_labels(labels: list[str], query: Any) -> list[str]:
    """Rank labels by fuzzy score with deterministic tie-breaks.

    Args:
        labels: List of display labels to rank
        query: Search query string (or any type - non-strings return sorted labels)

    Returns:
        Labels sorted by fuzzy score (descending), then case-insensitive label,
        then id suffix for deterministic ordering.
    """
    suffix_cache = {label: _extract_id_suffix(label) for label in labels}

    if not query:
        # No query: sort by case-insensitive label, then id suffix
        return sorted(labels, key=lambda lbl: (lbl.lower(), suffix_cache[lbl]))

    # Ensure query is a string
    if not isinstance(query, str):
        return sorted(labels, key=lambda lbl: (lbl.lower(), suffix_cache[lbl]))

    query_lower = query.lower()

    # Calculate scores and create tuples for sorting
    scored_labels = []
    for label in labels:
        label_lower = label.lower()
        score = _fuzzy_score(query_lower, label_lower)
        if score >= 0:  # Only include matches
            scored_labels.append((score, label_lower, suffix_cache[label], label))

    if not scored_labels:
        # No fuzzy matches: fall back to deterministic label sorting
        return sorted(labels, key=lambda lbl: (lbl.lower(), suffix_cache[lbl]))

    # Sort by: score (desc), label (case-insensitive), id suffix, original label
    scored_labels.sort(key=lambda x: (-x[0], x[1], x[2], x[3]))

    return [label for _score, _label_lower, _id_suffix, label in scored_labels]


# ----------------------- Structured renderer helpers -------------------- #


def _coerce_result_payload(result: Any) -> Any:
    """Convert renderer outputs into plain dict/list structures when possible."""
    try:
        to_dict = getattr(result, "to_dict", None)
        if callable(to_dict):
            return to_dict()
    except Exception:
        return result
    return result


def _ensure_displayable(payload: Any) -> Any:
    """Best-effort coercion into JSON/str-safe payloads for console rendering."""
    if isinstance(payload, (dict, list, str, int, float, bool)) or payload is None:
        return payload

    if hasattr(payload, "__dict__"):
        try:
            return dict(payload)
        except Exception:
            try:
                return dict(payload.__dict__)
            except Exception:
                pass

    try:
        return str(payload)
    except Exception:
        return repr(payload)


def _render_markdown_output(data: Any) -> None:
    """Render markdown output using Rich when available."""
    try:
        console.print(Markdown(str(data)))
    except ImportError:
        click.echo(str(data))


def _format_yaml_text(data: Any) -> str:
    """Convert structured payloads to YAML for readability."""
    try:
        yaml_text = yaml.dump(
            data,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            Dumper=_LiteralYamlDumper,
        )
    except Exception:  # pragma: no cover - defensive YAML fallback
        try:
            return str(data)
        except Exception:  # pragma: no cover - defensive str fallback
            return repr(data)

    yaml_text = yaml_text.rstrip()
    if yaml_text.endswith("..."):  # pragma: no cover - defensive YAML cleanup
        yaml_text = yaml_text[:-3].rstrip()
    return yaml_text


def _build_yaml_renderable(data: Any) -> Any:
    """Return a syntax-highlighted YAML renderable when possible."""
    yaml_text = _format_yaml_text(data) or "# No data"
    try:
        return Syntax(yaml_text, "yaml", word_wrap=False)
    except Exception:  # pragma: no cover - defensive syntax highlighting fallback
        return yaml_text


def output_result(
    ctx: Any,
    result: Any,
    title: str = "Result",
    panel_title: str | None = None,
) -> None:
    """Output a result to the console with optional title.

    Args:
        ctx: Click context
        result: Result data to output
        title: Optional title for the output
        panel_title: Optional Rich panel title for structured output
    """
    fmt = _get_view(ctx)

    data = _coerce_result_payload(result)
    data = masking.mask_payload(data)
    data = _ensure_displayable(data)

    if fmt == "json":
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if fmt == "plain":
        click.echo(str(data))
        return

    if fmt == "md":
        _render_markdown_output(data)
        return

    renderable = _build_yaml_renderable(data)
    if panel_title:
        console.print(AIPPanel(renderable, title=panel_title))
    else:
        console.print(markup_text(f"[{ACCENT_STYLE}]{title}:[/]"))
        console.print(renderable)


# ----------------------------- List rendering ---------------------------- #

# Threshold no longer used - fuzzy palette is always default for TTY
# _PICK_THRESHOLD = 5


def _normalise_rows(items: list[Any], transform_func: Callable[[Any], dict[str, Any]] | None) -> list[dict[str, Any]]:
    """Convert heterogeneous item lists into table rows."""
    try:
        rows: list[dict[str, Any]] = []
        for item in items:
            if transform_func:
                rows.append(transform_func(item))
            elif hasattr(item, "to_dict"):
                rows.append(item.to_dict())
            elif hasattr(item, "__dict__"):
                rows.append(vars(item))
            elif isinstance(item, dict):
                rows.append(item)
            else:
                rows.append({"value": item})
        return rows
    except Exception:
        return []


def _render_plain_list(rows: list[dict[str, Any]], title: str, columns: list[tuple]) -> None:
    """Display tabular data as a simple pipe-delimited list."""
    if not rows:
        click.echo(f"No {title.lower()} found.")
        return
    for row in rows:
        row_str = " | ".join(str(row.get(key, "N/A")) for key, _, _, _ in columns)
        click.echo(row_str)


def _render_markdown_list(rows: list[dict[str, Any]], title: str, columns: list[tuple]) -> None:
    """Display tabular data using markdown table syntax."""
    if not rows:
        click.echo(f"No {title.lower()} found.")
        return
    headers = [header for _, header, _, _ in columns]
    click.echo(f"| {' | '.join(headers)} |")
    click.echo(f"| {' | '.join('---' for _ in headers)} |")
    for row in rows:
        row_str = " | ".join(str(row.get(key, "N/A")) for key, _, _, _ in columns)
        click.echo(f"| {row_str} |")


def _should_sort_rows(rows: list[dict[str, Any]]) -> bool:
    """Return True when rows should be name-sorted prior to rendering."""
    return TABLE_SORT_ENABLED and rows and isinstance(rows[0], dict) and "name" in rows[0]


def _create_table(columns: list[tuple[str, str, str, int | None]], title: str) -> Any:
    """Build a configured Rich table for the provided columns."""
    table = AIPTable(title=title, expand=True)
    for _key, header, style, width in columns:
        table.add_column(header, style=style, width=width)
    return table


def _build_table_group(rows: list[dict[str, Any]], columns: list[tuple], title: str) -> Group:
    """Return a Rich group containing the table and a small footer summary."""
    table = _create_table(columns, title)
    for row in rows:
        table.add_row(*[str(row.get(key, "N/A")) for key, _, _, _ in columns])
    footer = markup_text(f"\n[dim]Total {len(rows)} items[/dim]")
    return Group(table, footer)


def _handle_json_output(items: list[Any], rows: list[dict[str, Any]]) -> None:
    """Handle JSON output format."""
    data = rows if rows else [it.to_dict() if hasattr(it, "to_dict") else it for it in items]
    click.echo(json.dumps(data, indent=2, default=str))


def _handle_plain_output(rows: list[dict[str, Any]], title: str, columns: list[tuple]) -> None:
    """Handle plain text output format."""
    _render_plain_list(rows, title, columns)


def _handle_markdown_output(rows: list[dict[str, Any]], title: str, columns: list[tuple]) -> None:
    """Handle markdown output format."""
    _render_markdown_list(rows, title, columns)


def _handle_empty_items(title: str) -> None:
    """Handle case when no items are found."""
    console.print(markup_text(f"[{WARNING_STYLE}]No {title.lower()} found.[/]"))


def _should_use_fuzzy_picker() -> bool:
    """Return True when the interactive fuzzy picker can be shown."""
    return console.is_terminal and os.isatty(1)


def _try_fuzzy_pick(rows: list[dict[str, Any]], columns: list[tuple], title: str) -> dict[str, Any] | None:
    """Best-effort fuzzy selection; returns None if the picker fails."""
    if not _should_use_fuzzy_picker():
        return None

    try:
        return _fuzzy_pick(rows, columns, title)
    except Exception:
        logger.debug("Fuzzy picker failed; falling back to table output", exc_info=True)
        return None


def _resource_tip_command(title: str) -> str | None:
    """Resolve the follow-up command hint for the given table title."""
    title_lower = title.lower()
    mapping = {
        "agent": ("agents get", "agents"),
        "tool": ("tools get", None),
        "mcp": ("mcps get", None),
        "model": ("models list", None),  # models only ship a list command
    }
    for keyword, (cli_command, slash_command) in mapping.items():
        if keyword in title_lower:
            return command_hint(cli_command, slash_command=slash_command)
    return command_hint("agents get", slash_command="agents")


def _print_selection_tip(title: str) -> None:
    """Print the contextual follow-up tip after a fuzzy selection."""
    tip_cmd = _resource_tip_command(title)
    if tip_cmd:
        console.print(markup_text(f"\n[dim]Tip: use `{tip_cmd} <ID>` for details[/dim]"))


def _handle_fuzzy_pick_selection(rows: list[dict[str, Any]], columns: list[tuple], title: str) -> bool:
    """Handle fuzzy picker selection.

    Returns:
        True if a resource was selected and displayed,
        False if cancelled/no selection.
    """
    picked = _try_fuzzy_pick(rows, columns, title)
    if picked is None:
        return False

    table = _create_table(columns, title)
    table.add_row(*[str(picked.get(key, "N/A")) for key, _, _, _ in columns])
    console.print(table)
    _print_selection_tip(title)
    return True


def _handle_table_output(
    rows: list[dict[str, Any]],
    columns: list[tuple],
    title: str,
    *,
    use_pager: bool | None = None,
) -> None:
    """Handle table output with paging."""
    content = _build_table_group(rows, columns, title)
    should_page = (
        pager._should_page_output(len(rows), console.is_terminal and os.isatty(1)) if use_pager is None else use_pager
    )

    if should_page:
        ansi = pager._render_ansi(content)
        if not pager._page_with_system_pager(ansi):
            with console.pager(styles=True):
                console.print(content)
    else:
        console.print(content)


def output_list(
    ctx: Any,
    items: list[Any],
    title: str,
    columns: list[tuple[str, str, str, int | None]],
    transform_func: Callable | None = None,
    *,
    skip_picker: bool = False,
    use_pager: bool | None = None,
) -> None:
    """Display a list with optional fuzzy palette for quick selection."""
    fmt = _get_view(ctx)
    rows = _normalise_rows(items, transform_func)
    rows = masking.mask_rows(rows)

    if fmt == "json":
        _handle_json_output(items, rows)
        return

    if fmt == "plain":
        _handle_plain_output(rows, title, columns)
        return

    if fmt == "md":
        _handle_markdown_output(rows, title, columns)
        return

    if not items:
        _handle_empty_items(title)
        return

    if _should_sort_rows(rows):
        try:
            rows = sorted(rows, key=lambda r: str(r.get("name", "")).lower())
        except Exception:
            pass

    if not skip_picker and _handle_fuzzy_pick_selection(rows, columns, title):
        return

    _handle_table_output(rows, columns, title, use_pager=use_pager)


# ------------------------- Ambiguity handling --------------------------- #


def coerce_to_row(item: Any, keys: list[str]) -> dict[str, Any]:
    """Coerce an item (dict or object) to a row dict with specified keys.

    Args:
        item: The item to coerce (dict or object with attributes)
        keys: List of keys/attribute names to extract

    Returns:
        Dict with the extracted values, "N/A" for missing values
    """
    result = {}
    for key in keys:
        if isinstance(item, dict):
            value = item.get(key, "N/A")
        else:
            value = getattr(item, key, "N/A")
        result[key] = str(value) if value is not None else "N/A"
    return result


def _register_renderer_with_session(ctx: Any, renderer: RichStreamRenderer) -> None:
    """Attach renderer to an active slash session when present."""
    try:
        ctx_obj = getattr(ctx, "obj", None)
        session = ctx_obj.get("_slash_session") if isinstance(ctx_obj, dict) else None
        if session and hasattr(session, "register_active_renderer"):
            session.register_active_renderer(renderer)
    except Exception:
        # Never let session bookkeeping break renderer creation
        pass


def build_renderer(
    _ctx: Any,
    *,
    save_path: str | os.PathLike[str] | None,
    verbose: bool = False,
    _tty_enabled: bool = True,
    live: bool | None = None,
    snapshots: bool | None = None,
) -> tuple[RichStreamRenderer, Console | CapturingConsole]:
    """Build renderer and capturing console for CLI commands.

    Args:
        _ctx: Click context object for CLI operations.
        save_path: Path to save output to (enables capturing console).
        verbose: Whether to enable verbose mode.
        _tty_enabled: Whether TTY is available for interactive features.
        live: Whether to enable live rendering mode (overrides verbose default).
        snapshots: Whether to capture and store snapshots.

    Returns:
        Tuple of (renderer, capturing_console) for streaming output.
    """
    # Use capturing console if saving output
    working_console = CapturingConsole(console, capture=True) if save_path else console

    # Configure renderer based on verbose mode and explicit overrides
    live_enabled = bool(live) if live is not None else not verbose
    cfg_overrides = {
        "live": live_enabled,
        "append_finished_snapshots": bool(snapshots) if snapshots is not None else False,
    }
    renderer_console = (
        working_console.original_console if isinstance(working_console, CapturingConsole) else working_console
    )
    factory = make_verbose_renderer if verbose else make_default_renderer
    factory_options = RendererFactoryOptions(
        console=renderer_console,
        cfg_overrides=cfg_overrides,
        verbose=verbose if factory is make_default_renderer else None,
    )
    renderer = factory_options.build(factory)

    # Link the renderer back to the slash session when running from the palette.
    _register_renderer_with_session(_ctx, renderer)

    return renderer, working_console


def _build_resource_labels(resources: list[Any]) -> tuple[list[str], dict[str, Any]]:
    """Build unique display labels for resources."""
    labels = []
    by_label: dict[str, Any] = {}

    for resource in resources:
        name = getattr(resource, "name", "Unknown")
        _id = getattr(resource, "id", "Unknown")

        # Create display label
        label_parts = []
        if name and name != "Unknown":
            label_parts.append(name)
        label_parts.append(f"[{_id[:8]}...]")  # Show first 8 chars of ID
        label = " • ".join(label_parts)

        # Ensure uniqueness
        if label in by_label:
            i = 2
            base = label
            while f"{base} #{i}" in by_label:
                i += 1
            label = f"{base} #{i}"

        labels.append(label)
        by_label[label] = resource

    return labels, by_label


def _fuzzy_pick_for_resources(
    resources: list[Any], resource_type: str, _search_term: str
) -> Any | None:  # pragma: no cover - interactive selection helper
    """Fuzzy picker for resource objects, similar to _fuzzy_pick but without column dependencies.

    Args:
        resources: List of resource objects to choose from
        resource_type: Type of resource (e.g., "agent", "tool")
        search_term: The search term that led to multiple matches

    Returns:
        Selected resource object or None if cancelled/no selection
    """
    if not _check_fuzzy_pick_requirements():
        return None

    # Build labels and mapping
    labels, by_label = _build_resource_labels(resources)

    # Create fuzzy completer
    completer = _FuzzyCompleter(labels)
    answer = _prompt_with_auto_select(
        f"Find {ICON_AGENT} {resource_type.title()}: ",
        completer,
        labels,
    )
    if answer is None:
        return None

    return _perform_fuzzy_search(answer, labels, by_label) if answer else None


def _resolve_by_id(ref: str, get_by_id: Callable) -> Any | None:
    """Resolve resource by UUID if ref is a valid UUID."""
    if is_uuid(ref):
        return get_by_id(ref)
    return None


def _resolve_by_name_multiple_with_select(matches: list[Any], select: int) -> Any:
    """Resolve multiple matches using select parameter."""
    idx = int(select) - 1
    if not (0 <= idx < len(matches)):
        raise click.ClickException(f"--select must be 1..{len(matches)}")
    return matches[idx]


def _resolve_by_name_multiple_fuzzy(ctx: Any, ref: str, matches: list[Any], label: str) -> Any:
    """Resolve multiple matches preferring the fuzzy picker interface."""
    return handle_ambiguous_resource(ctx, label.lower(), ref, matches, interface_preference="fuzzy")


def _resolve_by_name_multiple_questionary(ctx: Any, ref: str, matches: list[Any], label: str) -> Any:
    """Resolve multiple matches preferring the questionary interface."""
    return handle_ambiguous_resource(ctx, label.lower(), ref, matches, interface_preference="questionary")


def resolve_resource(
    ctx: Any,
    ref: str,
    *,
    get_by_id: Callable,
    find_by_name: Callable,
    label: str,
    select: int | None = None,
    interface_preference: str = "fuzzy",
    status_indicator: Any | None = None,
) -> Any | None:
    """Resolve resource reference (ID or name) with ambiguity handling.

    Args:
        ctx: Click context
        ref: Resource reference (ID or name)
        get_by_id: Function to get resource by ID
        find_by_name: Function to find resources by name
        label: Resource type label for error messages
        select: Optional selection index for ambiguity resolution
        interface_preference: "fuzzy" for fuzzy picker, "questionary" for up/down list
        status_indicator: Optional Rich status indicator for wait animations

    Returns:
        Resolved resource object
    """
    spinner = status_indicator
    _spinner_update(spinner, f"[bold blue]Resolving {label}…[/bold blue]")

    # Try to resolve by ID first
    _spinner_update(spinner, f"[bold blue]Fetching {label} by ID…[/bold blue]")
    result = _resolve_by_id(ref, get_by_id)
    if result is not None:
        _spinner_update(spinner, f"[{SUCCESS_STYLE}]{label} found[/]")
        return result

    # If get_by_id returned None, the resource doesn't exist
    if is_uuid(ref):
        _spinner_stop(spinner)
        raise click.ClickException(f"{label} '{ref}' not found")

    # Find resources by name
    _spinner_update(spinner, f"[bold blue]Searching {label}s matching '{ref}'…[/bold blue]")
    matches = find_by_name(name=ref)
    if not matches:
        _spinner_stop(spinner)
        raise click.ClickException(f"{label} '{ref}' not found")

    if len(matches) == 1:
        _spinner_update(spinner, f"[{SUCCESS_STYLE}]{label} found[/]")
        return matches[0]

    # Multiple matches found, handle ambiguity
    if select:
        _spinner_stop(spinner)
        return _resolve_by_name_multiple_with_select(matches, select)

    # Choose interface based on preference
    _spinner_stop(spinner)
    preference = (interface_preference or "fuzzy").lower()
    if preference not in {"fuzzy", "questionary"}:
        preference = "fuzzy"
    if preference == "fuzzy":
        return _resolve_by_name_multiple_fuzzy(ctx, ref, matches, label)
    else:
        return _resolve_by_name_multiple_questionary(ctx, ref, matches, label)


def _handle_json_view_ambiguity(matches: list[Any]) -> Any:
    """Handle ambiguity in JSON view by returning first match."""
    return matches[0]


def _handle_questionary_ambiguity(resource_type: str, ref: str, matches: list[Any]) -> Any:
    """Handle ambiguity using questionary interactive interface."""
    questionary_module, choice_cls = _load_questionary_module()
    if not (questionary_module and os.getenv("TERM") and os.isatty(0) and os.isatty(1)):
        raise click.ClickException("Interactive selection not available")

    # Escape special characters for questionary
    safe_resource_type = resource_type.replace("{", "{{").replace("}", "}}")
    safe_ref = ref.replace("{", "{{").replace("}", "}}")

    picked_idx = questionary_module.select(
        f"Multiple {safe_resource_type}s match '{safe_ref}'. Pick one:",
        choices=[
            _make_questionary_choice(
                choice_cls,
                title=(
                    f"{getattr(m, 'name', '—').replace('{', '{{').replace('}', '}}')} — "
                    f"{getattr(m, 'id', '').replace('{', '{{').replace('}', '}}')}"
                ),
                value=i,
            )
            for i, m in enumerate(matches)
        ],
        use_indicator=True,
        qmark="🧭",
        instruction="↑/↓ to select • Enter to confirm",
    ).ask()
    if picked_idx is None:
        raise click.ClickException("Selection cancelled")
    return matches[picked_idx]


def _handle_fallback_numeric_ambiguity(resource_type: str, ref: str, matches: list[Any]) -> Any:
    """Handle ambiguity using numeric prompt fallback."""
    # Escape special characters for display
    safe_resource_type = resource_type.replace("{", "{{").replace("}", "}}")
    safe_ref = ref.replace("{", "{{").replace("}", "}}")

    console.print(markup_text(f"[{WARNING_STYLE}]Multiple {safe_resource_type}s found matching '{safe_ref}':[/]"))
    table = AIPTable(
        title=f"Select {safe_resource_type.title()}",
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("ID", style="dim", width=36)
    table.add_column("Name", style=ACCENT_STYLE)
    for i, m in enumerate(matches, 1):
        table.add_row(str(i), str(getattr(m, "id", "")), str(getattr(m, "name", "")))
    console.print(table)
    choice_str = click.prompt(
        f"Select {safe_resource_type} (1-{len(matches)})",
    )
    try:
        choice = int(choice_str)
    except ValueError as err:
        raise click.ClickException("Invalid selection") from err
    if 1 <= choice <= len(matches):
        return matches[choice - 1]
    raise click.ClickException("Invalid selection")


def _should_fallback_to_numeric_prompt(exception: Exception) -> bool:
    """Determine if we should fallback to numeric prompt for this exception."""
    # Re-raise cancellation - user explicitly cancelled
    if "Selection cancelled" in str(exception):
        return False

    # Fall back to numeric prompt for other exceptions
    return True


def _normalize_interface_preference(preference: str) -> str:
    """Normalize and validate interface preference."""
    normalized = (preference or "questionary").lower()
    return normalized if normalized in {"fuzzy", "questionary"} else "questionary"


def _get_interface_order(preference: str) -> tuple[str, str]:
    """Get the ordered interface preferences."""
    interface_orders = {
        "fuzzy": ("fuzzy", "questionary"),
        "questionary": ("questionary", "fuzzy"),
    }
    return interface_orders.get(preference, ("questionary", "fuzzy"))


def _try_fuzzy_selection(
    resource_type: str,
    ref: str,
    matches: list[Any],
) -> Any | None:
    """Try fuzzy interface selection."""
    picked = _fuzzy_pick_for_resources(matches, resource_type, ref)
    return picked if picked else None


def _try_questionary_selection(
    resource_type: str,
    ref: str,
    matches: list[Any],
) -> Any | None:
    """Try questionary interface selection."""
    try:
        return _handle_questionary_ambiguity(resource_type, ref, matches)
    except Exception as exc:
        if not _should_fallback_to_numeric_prompt(exc):
            raise
        return None


def _try_interface_selection(
    interface_order: tuple[str, str],
    resource_type: str,
    ref: str,
    matches: list[Any],
) -> Any | None:
    """Try interface selection in order, return result or None if all failed."""
    interface_handlers = {
        "fuzzy": _try_fuzzy_selection,
        "questionary": _try_questionary_selection,
    }

    for interface in interface_order:
        handler = interface_handlers.get(interface)
        if handler:
            result = handler(resource_type, ref, matches)
            if result:
                return result

    return None


def handle_ambiguous_resource(
    ctx: Any,
    resource_type: str,
    ref: str,
    matches: list[Any],
    *,
    interface_preference: str = "questionary",
) -> Any:
    """Handle multiple resource matches gracefully."""
    if _get_view(ctx) == "json":
        return _handle_json_view_ambiguity(matches)

    preference = _normalize_interface_preference(interface_preference)
    interface_order = _get_interface_order(preference)

    result = _try_interface_selection(interface_order, resource_type, ref, matches)

    if result is not None:
        return result

    return _handle_fallback_numeric_ambiguity(resource_type, ref, matches)
