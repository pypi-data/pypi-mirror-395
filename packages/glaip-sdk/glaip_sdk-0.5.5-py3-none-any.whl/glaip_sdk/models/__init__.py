"""Models package for AIP SDK.

This package re-exports models from the legacy models.py file for backward compatibility.

Authors:
    Raymond Christopher (raymond.christopher@gdplabs.id)
"""

import importlib.util
import sys
from pathlib import Path

# Export new agent runs models first (no dependencies on legacy models)
from glaip_sdk.models.agent_runs import (  # noqa: F401
    RunOutputChunk,
    RunSummary,
    RunsPage,
    RunWithOutput,
)

# Import from the parent models.py file
_parent_file = Path(__file__).parent.parent / "models.py"
if _parent_file.exists():
    spec = importlib.util.spec_from_file_location("glaip_sdk.models_legacy", _parent_file)
    models_legacy = importlib.util.module_from_spec(spec)
    sys.modules["glaip_sdk.models_legacy"] = models_legacy
    spec.loader.exec_module(models_legacy)

    # Re-export all models
    Agent = models_legacy.Agent
    Tool = models_legacy.Tool
    MCP = models_legacy.MCP
    LanguageModelResponse = models_legacy.LanguageModelResponse
    TTYRenderer = models_legacy.TTYRenderer
else:
    # Fallback: try direct import (won't work if models/ exists)
    # pragma: no cover - defensive fallback path, unlikely to execute
    from glaip_sdk import models as models_legacy  # type: ignore  # pragma: no cover

    Agent = models_legacy.Agent  # pragma: no cover
    Tool = models_legacy.Tool  # pragma: no cover
    MCP = models_legacy.MCP  # pragma: no cover
    LanguageModelResponse = models_legacy.LanguageModelResponse  # pragma: no cover
    TTYRenderer = models_legacy.TTYRenderer  # pragma: no cover

__all__ = [
    "Agent",
    "Tool",
    "MCP",
    "LanguageModelResponse",
    "TTYRenderer",
    "RunSummary",
    "RunsPage",
    "RunWithOutput",
    "RunOutputChunk",
]
