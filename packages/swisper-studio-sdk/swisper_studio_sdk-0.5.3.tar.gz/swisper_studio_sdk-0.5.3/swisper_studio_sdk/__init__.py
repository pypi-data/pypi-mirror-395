"""
SwisperStudio SDK

Simple integration for tracing Swisper LangGraph applications.

v0.5.3 - LLM TELEMETRY FIX (Critical):
- FIXED: LLM observations now correctly show as GENERATION (not SPAN)
- FIXED: obs_id context propagation issue with LangGraph orchestration
- The _store_llm_input/_store_llm_output functions now receive obs_id explicitly
  instead of fetching from context (prevents mismatch in async task spawning)
- Added comprehensive debug logging for telemetry flow tracing
- Enhanced has_llm_data detection to require actual input/output data

v0.5.2 - HITL/Checkpoint Compatibility:
- Removed upper bound on langgraph-checkpoint dependency
- Now compatible with langgraph-checkpoint 3.x (required for HITL Interrupt fix)
- No code changes - just dependency constraint relaxation

v0.5.1 - ROBUST FAILURE HANDLING:
- SDK NEVER blocks or crashes Swisper, even if:
  - Redis is misconfigured
  - Redis is unreachable
  - SwisperStudio is down
  - Any timeout occurs
- All operations have timeouts (default 3s)
- Graceful degradation - tracing silently disabled on failure
- Safe initialization wrapper for production use

v0.5.0 - Q2 Tracing Toggle + Tool Observations:
- Dynamic tracing toggle (on/off per project)
- Universal tool observation extraction (no decorators!)
- Redis-cached toggle checks (<2ms overhead)
- Full cost tracking (316 models, CHF for KVANT)
- LLM reasoning capture
- 50x faster than HTTP (10ms overhead)

v0.4.0 - Redis Streams Architecture:
- 50x faster (500ms → 10ms overhead)
- LLM reasoning capture
- Connection status verification
- Per-node configuration

Usage:
    from swisper_studio_sdk import create_traced_graph, safe_initialize

    # RECOMMENDED: Safe initialization (never raises, never blocks)
    await safe_initialize(
        redis_url="redis://redis:6379",
        project_id="your-project-id"
    )

    # One-line change to add tracing
    graph = create_traced_graph(
        GlobalSupervisorState,
        trace_name="supervisor"
    )
    
    # If initialization failed, create_traced_graph returns a normal StateGraph
    # Swisper continues to work normally, just without tracing
"""

# Define version BEFORE imports to avoid circular dependency
__version__ = "0.5.3"  # LLM telemetry fix - obs_id context propagation

import asyncio
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# ============================================================================
# CRITICAL DESIGN PRINCIPLE:
# The SDK must NEVER block or crash Swisper, even if:
# - Redis is misconfigured
# - Redis is unreachable
# - SwisperStudio is down
# - Any timeout occurs
#
# All SDK operations fail silently and gracefully.
# ============================================================================

# Import SDK components (these imports are always safe)
from swisper_studio_sdk.tracing.decorator import traced
from swisper_studio_sdk.tracing.graph_wrapper import create_traced_graph
from swisper_studio_sdk.tracing.client import initialize_tracing  # Deprecated, use Redis
from swisper_studio_sdk.tracing.redis_publisher import (
    initialize_redis_publisher, 
    close_redis_publisher,
    disable_tracing,
    is_tracing_initialized,
    DEFAULT_TIMEOUT,
)
from swisper_studio_sdk.wrappers import wrap_llm_adapter, wrap_tools


async def safe_initialize(
    redis_url: str,
    project_id: str,
    stream_name: str = "observability:events",
    max_stream_length: int = 100000,
    verify_consumer: bool = True,
    connection_timeout: float = 5.0,
    enabled: bool = True,
) -> Dict[str, bool]:
    """
    SAFELY initialize SwisperStudio SDK tracing.
    
    This function NEVER raises exceptions and NEVER blocks indefinitely.
    If initialization fails for any reason, tracing is silently disabled
    and Swisper continues to operate normally.
    
    This is the RECOMMENDED way to initialize the SDK in production.
    
    Args:
        redis_url: Redis connection URL (e.g., "redis://redis:6379")
        project_id: SwisperStudio project ID
        stream_name: Redis stream name for events
        max_stream_length: Max events to keep in stream
        verify_consumer: Whether to verify consumer is running
        connection_timeout: Max time to wait for Redis connection
        enabled: Whether to enable tracing (False = skip initialization)
    
    Returns:
        dict: Status of initialization (never raises)
            {
                "enabled": bool,      # Whether tracing is enabled
                "redis": bool,        # Redis connectivity OK
                "write": bool,        # Write permission OK
                "consumer": bool,     # Consumer detected
                "initialized": bool,  # Overall initialization status
            }
    
    Example:
        # At startup
        status = await safe_initialize(
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
            project_id=os.getenv("SWISPER_STUDIO_PROJECT_ID", ""),
        )
        
        if status["initialized"]:
            logger.info("✅ SwisperStudio tracing enabled")
        else:
            logger.info("⚠️ SwisperStudio tracing disabled (Swisper continues normally)")
    """
    result = {
        "enabled": enabled,
        "redis": False,
        "write": False,
        "consumer": False,
        "initialized": False,
    }
    
    if not enabled:
        logger.info("⏸️ SwisperStudio SDK disabled by configuration")
        return result
    
    if not redis_url:
        logger.warning("⚠️ No Redis URL provided, tracing disabled")
        return result
    
    if not project_id:
        logger.warning("⚠️ No project ID provided, tracing disabled")
        return result
    
    try:
        # Initialize with overall timeout to prevent any hanging
        init_result = await asyncio.wait_for(
            initialize_redis_publisher(
                redis_url=redis_url,
                stream_name=stream_name,
                project_id=project_id,
                max_stream_length=max_stream_length,
                verify_consumer=verify_consumer,
                connection_timeout=connection_timeout,
            ),
            timeout=connection_timeout + 5.0  # Extra buffer for verification
        )
        
        result.update(init_result)
        
        if result.get("initialized"):
            logger.info("✅ SwisperStudio SDK initialized successfully")
        else:
            logger.warning("⚠️ SwisperStudio SDK initialization incomplete, tracing disabled")
        
        return result
        
    except asyncio.TimeoutError:
        logger.warning(f"⚠️ SDK initialization timed out after {connection_timeout}s")
        logger.warning("   Tracing disabled, Swisper continues normally")
        return result
        
    except Exception as e:
        logger.warning(f"⚠️ SDK initialization failed: {e}")
        logger.warning("   Tracing disabled, Swisper continues normally")
        return result


def is_sdk_available() -> bool:
    """
    Check if SDK is initialized and ready.
    
    Returns:
        True if tracing is active, False otherwise
    """
    return is_tracing_initialized()


__all__ = [
    # Core functions
    "traced",
    "create_traced_graph",
    
    # Initialization (RECOMMENDED: use safe_initialize)
    "safe_initialize",
    "initialize_redis_publisher",
    "close_redis_publisher",
    "disable_tracing",
    
    # Status checks
    "is_sdk_available",
    "is_tracing_initialized",
    
    # Wrappers
    "wrap_llm_adapter",
    "wrap_tools",
    
    # Deprecated (kept for backwards compatibility)
    "initialize_tracing",
]
