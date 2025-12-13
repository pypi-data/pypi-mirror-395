# Copyright 2025 Sushanth (https://github.com/sushanthpy)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
