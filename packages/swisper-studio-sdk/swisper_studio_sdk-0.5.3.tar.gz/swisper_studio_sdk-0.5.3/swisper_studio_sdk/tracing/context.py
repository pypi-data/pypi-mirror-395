"""
Context management for tracing

Uses contextvars to track current trace and observation IDs.
Supports nested observations (parent-child relationships).
"""

from contextvars import ContextVar
from typing import Optional

# Context variables
_current_trace_id: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
_current_observation_id: ContextVar[Optional[str]] = ContextVar('observation_id', default=None)


def get_current_trace() -> Optional[str]:
    """Get current trace ID from context"""
    return _current_trace_id.get()


def set_current_trace(trace_id: str) -> None:
    """Set current trace ID"""
    _current_trace_id.set(trace_id)


def get_current_observation() -> Optional[str]:
    """Get current observation ID (for nesting)"""
    return _current_observation_id.get()


def set_current_observation(obs_id: Optional[str], token=None):
    """Set current observation ID"""
    if token:
        _current_observation_id.reset(token)
    else:
        return _current_observation_id.set(obs_id)

