"""
AGENTICONTROL V0 MVP - Control plane for AI agents.

This package provides synchronous blocking checks and asynchronous logging
for AI agent execution, with support for LangChain integration.
"""

__version__ = "0.1.0"

from agenticontrol.client import AgenticontrolClient
from agenticontrol.exceptions import (
    LoopDetectedError,
    PolicyViolationError,
    PolicyV0ViolationError,
)
from agenticontrol.hooks.langchain_handler import AgenticontrolCallbackHandler
from agenticontrol.models import RiskResult, RunMetadata, TraceEvent
from agenticontrol.risk_engine import RiskEngine, get_risk_engine

# Optional viewer import
try:
    from agenticontrol.local.viewer import TraceViewer, get_viewer, start_viewer, stop_viewer
    _VIEWER_EXPORTS = [
        "TraceViewer",
        "get_viewer",
        "start_viewer",
        "stop_viewer",
    ]
except ImportError:
    _VIEWER_EXPORTS = []

__all__ = [
    "TraceEvent",
    "RunMetadata",
    "RiskResult",
    "PolicyViolationError",
    "PolicyV0ViolationError",
    "LoopDetectedError",
    "RiskEngine",
    "get_risk_engine",
    "AgenticontrolClient",
    "AgenticontrolCallbackHandler",
] + _VIEWER_EXPORTS

