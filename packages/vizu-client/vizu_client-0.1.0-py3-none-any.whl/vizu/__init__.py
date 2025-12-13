"""Vizu Python SDK - Agent Trace Engine for LLM Agents."""

from vizu.client import VizuClient
from vizu.models import SpanType, AgentFlowEdge
from vizu.span import Span
from vizu.config import VizuConfig, get_config, set_config, reset_config
from vizu.batching import BatchingVizuClient
from vizu.session import Session
from vizu.retry import retry_with_backoff
from vizu.exceptions import (
    VizuError,
    AuthenticationError,
    RateLimitError,
    ServerError,
    ValidationError,
    NotFoundError,
    NetworkError,
)

# Agent Context Tracking
from vizu.context import AgentContext

# Auto-instrumentation (Pure OpenTelemetry)
from vizu.auto_instrument import auto_instrument, setup_instrumentation

# OTEL Bridge & Bootstrap
from vizu.bootstrap import init_otel_instrumentation, is_initialized
from vizu.otel_bridge import get_tracer

__version__ = "0.1.0"

__all__ = [
    # Core client
    "VizuClient",
    "BatchingVizuClient",
    # Models
    "SpanType",
    "AgentFlowEdge",
    "Span",
    # Configuration
    "VizuConfig",
    "get_config",
    "set_config",
    "reset_config",
    # Session management
    "Session",
    # Retry utilities
    "retry_with_backoff",
    # Agent Context
    "AgentContext",
    # Auto-instrumentation (Pure OpenTelemetry)
    "auto_instrument",
    "setup_instrumentation",
    # OTEL Initialization
    "init_otel_instrumentation",
    "is_initialized",
    # OTEL Bridge
    "get_tracer",
    # Exceptions
    "VizuError",
    "AuthenticationError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "NotFoundError",
    "NetworkError",
]
