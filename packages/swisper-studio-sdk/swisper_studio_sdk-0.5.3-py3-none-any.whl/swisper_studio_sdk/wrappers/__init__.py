"""
SDK Wrappers for automatic telemetry capture

These wrappers intercept LLM and tool calls to automatically capture
prompts, responses, tokens, and set correct observation types.

Status: Infrastructure ready, implementation requires Swisper code access.
"""

from .llm_wrapper import wrap_llm_adapter
from .tool_wrapper import wrap_tools

__all__ = [
    "wrap_llm_adapter",
    "wrap_tools",
]


