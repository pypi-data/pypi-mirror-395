"""
LangGraph wrapper for automatic tracing

create_traced_graph() enables ONE-LINE integration for Swisper.

v0.5.1: ROBUST FAILURE HANDLING
- SDK NEVER blocks Swisper, even with misconfiguration
- All operations have timeouts
- All exceptions caught and logged, never propagated
- Graceful degradation to standard StateGraph on any error
- Checks Redis availability before every operation
- Handles disconnected Redis gracefully

Usage:
    # Before:
    # graph = StateGraph(GlobalSupervisorState)

    # After (ONE LINE CHANGE):
    graph = create_traced_graph(GlobalSupervisorState, trace_name="supervisor")

    # All nodes added to this graph are automatically traced!
"""

from typing import Type, TypeVar
from langgraph.graph import StateGraph
import asyncio
import copy
import functools
import logging
import uuid
from datetime import datetime

from .decorator import traced
from .client import get_studio_client
from .context import set_current_trace, set_current_observation, get_current_trace, get_current_observation
from .redis_publisher import (
    publish_event, 
    get_redis_client, 
    is_tracing_enabled_for_project, 
    get_project_id,
    is_tracing_initialized,
    DEFAULT_TIMEOUT,
)
from .. import __version__

logger = logging.getLogger(__name__)

# ============================================================================
# CRITICAL DESIGN PRINCIPLE:
# The SDK must NEVER block or crash Swisper, even if:
# - Redis is misconfigured
# - Redis is unreachable
# - Redis connection drops mid-operation
# - SwisperStudio is down
# - Any timeout occurs
#
# All tracing operations are wrapped in try-except with timeouts.
# If tracing fails, Swisper continues normally.
# ============================================================================

TState = TypeVar('TState')

# Global heartbeat task tracker (one per project)
_heartbeat_tasks = {}


async def _is_redis_healthy(timeout: float = 1.0) -> bool:
    """
    Quick health check for Redis connection.
    
    Returns True if Redis is connected and responsive, False otherwise.
    NEVER blocks for more than timeout seconds.
    """
    client = get_redis_client()
    if not client:
        return False
    
    try:
        # Quick ping with short timeout
        await asyncio.wait_for(client.ping(), timeout=timeout)
        return True
    except Exception:
        return False


async def _publish_heartbeat_loop(project_id: str):
    """
    Publish heartbeat events every 10 seconds.
    
    Allows Swisper to show green indicator when:
    - Tracing toggle is ON
    - SDK is alive and publishing
    
    ROBUST: Never crashes, logs errors and continues.
    """
    try:
        while True:
            try:
                # Check if Redis is still healthy before publishing
                if not await _is_redis_healthy(timeout=1.0):
                    logger.debug("Heartbeat skipped - Redis not healthy")
                    await asyncio.sleep(10)
                    continue
                
                # Heartbeat is non-critical, use shorter timeout
                await publish_event(
                    event_type="heartbeat",
                    trace_id=None,  # Not tied to specific trace
                    data={
                        "project_id": project_id,
                        "sdk_version": __version__,
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                    timeout=2.0  # Short timeout for heartbeat
                )
                logger.debug(f"💓 Heartbeat published for project {project_id[:8]}...")
            except Exception as e:
                # Never crash the heartbeat loop
                logger.debug(f"Failed to publish heartbeat: {e}")
            
            await asyncio.sleep(10)  # Heartbeat every 10 seconds
    except asyncio.CancelledError:
        logger.debug(f"Heartbeat task cancelled for project {project_id[:8]}...")
        raise
    except Exception as e:
        # Catch-all to prevent any crash
        logger.debug(f"Heartbeat loop error: {e}")


def _start_heartbeat_task(project_id: str):
    """
    Start heartbeat publishing task for a project (if not already running).
    
    Only one heartbeat task per project_id.
    Task runs in background and publishes every 10 seconds.
    
    ROBUST: Never raises exceptions.
    """
    try:
        if project_id not in _heartbeat_tasks:
            task = asyncio.create_task(_publish_heartbeat_loop(project_id))
            _heartbeat_tasks[project_id] = task
            logger.debug(f"💓 Started heartbeat task for project {project_id[:8]}...")
    except Exception as e:
        logger.debug(f"Failed to start heartbeat task: {e}")


def create_traced_graph(
    state_class: Type[TState],
    trace_name: str,
    auto_trace_all_nodes: bool = True,
) -> StateGraph:
    """
    Create a StateGraph with automatic node tracing.

    This is the key integration feature - enables tracing with minimal code changes.
    
    ROBUST: If tracing setup fails, returns a normal StateGraph.
    The SDK will NEVER block or crash Swisper.

    Args:
        state_class: The LangGraph state class
        trace_name: Name for traces created by this graph
        auto_trace_all_nodes: If True, automatically wraps all nodes with @traced

    Returns:
        StateGraph instance with tracing enabled (or plain StateGraph on error)

    Example:
        graph = create_traced_graph(GlobalSupervisorState, trace_name="supervisor")
        graph.add_node("intent_classification", intent_classification_node)
        # intent_classification_node is automatically traced!
    """
    # Always create the base graph first
    graph = StateGraph(state_class)

    try:
        if auto_trace_all_nodes:
            # Save original add_node method
            original_add_node = graph.add_node

            # Create wrapper that auto-traces
            def traced_add_node(name: str, func):
                """
                Replacement for add_node that automatically wraps functions with @traced.

                This is the "magic" that makes the one-line integration work.
                """
                try:
                    # Wrap function with @traced decorator
                    # Use "AUTO" to trigger type detection based on captured LLM data
                    wrapped_func = traced(
                        name=name,
                        observation_type="AUTO"  # Will auto-detect GENERATION/TOOL/AGENT/SPAN
                    )(func)

                    # Call original add_node with wrapped function
                    return original_add_node(name, wrapped_func)
                except Exception as e:
                    # If tracing wrapper fails, use original function
                    logger.debug(f"Failed to wrap node {name} with tracing: {e}")
                    return original_add_node(name, func)

            # Replace add_node with auto-tracing version
            graph.add_node = traced_add_node

        # Wrap compile to create trace on invocation
        original_compile = graph.compile

        def traced_compile(*args, **kwargs):
            """Wrap compile to intercept ainvoke and create traces"""
            try:
                compiled_graph = original_compile(*args, **kwargs)
                original_ainvoke = compiled_graph.ainvoke

                @functools.wraps(original_ainvoke)
                async def traced_ainvoke(input_state, config=None, **invoke_kwargs):
                    """
                    Create trace before running graph (Redis Streams version).

                    ROBUST: If tracing fails at any point, runs graph normally.
                    
                    Pre-flight checks:
                    1. Is tracing initialized?
                    2. Is Redis client available?
                    3. Is Redis connection healthy?
                    
                    If any check fails, skip tracing and run normally.
                    """
                    # ============================================================
                    # PRE-FLIGHT CHECKS - Quick fail if tracing unavailable
                    # ============================================================
                    
                    # Check 1: Is tracing even initialized?
                    if not is_tracing_initialized():
                        return await original_ainvoke(input_state, config, **invoke_kwargs)
                    
                    # Check 2: Is Redis client available?
                    redis_client = get_redis_client()
                    if not redis_client:
                        return await original_ainvoke(input_state, config, **invoke_kwargs)
                    
                    # Check 3: Is Redis connection healthy? (quick 1s ping)
                    # This catches the case where client exists but connection dropped
                    try:
                        is_healthy = await asyncio.wait_for(
                            _is_redis_healthy(timeout=1.0),
                            timeout=2.0  # Extra safety timeout
                        )
                        if not is_healthy:
                            logger.debug("Redis not healthy, skipping tracing")
                            return await original_ainvoke(input_state, config, **invoke_kwargs)
                    except Exception:
                        # If health check fails, skip tracing
                        logger.debug("Redis health check failed, skipping tracing")
                        return await original_ainvoke(input_state, config, **invoke_kwargs)

                    # ============================================================
                    # TRACING ENABLED - Proceed with trace creation
                    # ============================================================
                    
                    # Check if we're already in a trace context (nested agent call)
                    existing_trace_id = get_current_trace()
                    existing_parent_obs = get_current_observation()

                    if existing_trace_id:
                        # NESTED AGENT: We're inside another traced graph
                        return await _handle_nested_agent(
                            original_ainvoke, input_state, config, invoke_kwargs,
                            trace_name, existing_trace_id, existing_parent_obs
                        )
                    else:
                        # TOP-LEVEL AGENT: Create new trace
                        return await _handle_top_level_agent(
                            original_ainvoke, input_state, config, invoke_kwargs,
                            trace_name
                        )

                # Replace ainvoke with traced version
                compiled_graph.ainvoke = traced_ainvoke
                return compiled_graph
                
            except Exception as e:
                # If wrapping fails, return unwrapped compiled graph
                logger.debug(f"Failed to wrap compiled graph: {e}")
                return original_compile(*args, **kwargs)

        # Replace compile with our wrapper
        graph.compile = traced_compile

    except Exception as e:
        # If any setup fails, return the plain graph
        logger.debug(f"Failed to set up tracing for graph: {e}")
    
    return graph


async def _handle_nested_agent(
    original_ainvoke,
    input_state,
    config,
    invoke_kwargs,
    trace_name: str,
    existing_trace_id: str,
    existing_parent_obs: str,
):
    """
    Handle nested agent call (reuse existing trace).
    
    ROBUST: If tracing fails, runs graph normally.
    """
    logger.debug(f"🔗 Nested agent '{trace_name}' detected, using existing trace")

    parent_obs_id = str(uuid.uuid4())

    try:
        # Quick health check before Redis operations
        if not await _is_redis_healthy(timeout=1.0):
            logger.debug("Redis not healthy for nested agent, skipping tracing")
            return await original_ainvoke(input_state, config, **invoke_kwargs)
        
        # Create observation for this nested graph (AGENT type)
        await publish_event(
            event_type="observation_start",
            trace_id=existing_trace_id,
            observation_id=parent_obs_id,
            data={
                "name": trace_name,
                "type": "AGENT",
                "parent_observation_id": existing_parent_obs,
                "input": _safe_copy(input_state),
                "start_time": datetime.utcnow().isoformat(),
            }
        )

        # Set as current observation
        parent_token = set_current_observation(parent_obs_id)

        try:
            # Run graph with nested context
            result = await original_ainvoke(input_state, config, **invoke_kwargs)

            # End nested agent observation (best effort)
            try:
                await publish_event(
                    event_type="observation_end",
                    trace_id=existing_trace_id,
                    observation_id=parent_obs_id,
                    data={
                        "output": _safe_copy(result),
                        "level": "DEFAULT",
                        "end_time": datetime.utcnow().isoformat(),
                    }
                )
            except Exception:
                pass  # Don't fail if end event fails

            return result

        finally:
            # Restore parent observation context
            set_current_observation(existing_parent_obs, parent_token)

    except Exception as e:
        # If tracing fails, run graph without tracing
        logger.debug(f"Nested agent tracing failed: {e}, running without tracing")
        return await original_ainvoke(input_state, config, **invoke_kwargs)


async def _handle_top_level_agent(
    original_ainvoke,
    input_state,
    config,
    invoke_kwargs,
    trace_name: str,
):
    """
    Handle top-level agent call (create new trace).
    
    ROBUST: If tracing fails at any point, runs graph normally.
    """
    project_id = get_project_id()
    
    # Check if tracing is enabled for this project
    if project_id:
        try:
            # Quick health check first
            if not await _is_redis_healthy(timeout=1.0):
                logger.debug("Redis not healthy, skipping tracing")
                return await original_ainvoke(input_state, config, **invoke_kwargs)
            
            # Check tracing toggle with timeout
            tracing_enabled = await asyncio.wait_for(
                is_tracing_enabled_for_project(project_id),
                timeout=DEFAULT_TIMEOUT
            )
            if not tracing_enabled:
                logger.debug(f"⏸️ Tracing disabled for project, skipping")
                return await original_ainvoke(input_state, config, **invoke_kwargs)
            
            # Tracing is enabled - start heartbeat task
            _start_heartbeat_task(project_id)
            
        except asyncio.TimeoutError:
            logger.debug("Timeout checking tracing status, running without tracing")
            return await original_ainvoke(input_state, config, **invoke_kwargs)
        except Exception as e:
            logger.debug(f"Error checking tracing status: {e}, running without tracing")
            return await original_ainvoke(input_state, config, **invoke_kwargs)

    logger.debug(f"📍 Top-level agent '{trace_name}', creating new trace...")

    trace_id = None
    parent_obs_id = None
    parent_token = None

    try:
        user_id = input_state.get("user_id") if isinstance(input_state, dict) else None
        session_id = input_state.get("chat_id") or input_state.get("session_id") if isinstance(input_state, dict) else None

        # Extract first sentence of user message for meaningful trace name
        trace_display_name = trace_name
        if isinstance(input_state, dict):
            user_message = input_state.get("user_message") or input_state.get("message")
            if user_message and isinstance(user_message, str):
                first_sentence = user_message.split('.')[0].split('?')[0].split('!')[0]
                if len(first_sentence) > 100:
                    first_sentence = first_sentence[:97] + "..."
                trace_display_name = first_sentence.strip() or trace_name

        # Generate trace ID locally
        trace_id = str(uuid.uuid4())

        # Publish trace start event
        success = await publish_event(
            event_type="trace_start",
            trace_id=trace_id,
            data={
                "name": trace_display_name,
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        
        # If publish failed, skip tracing
        if not success:
            logger.debug("Failed to publish trace_start, running without tracing")
            return await original_ainvoke(input_state, config, **invoke_kwargs)

        # Set trace context for observations
        set_current_trace(trace_id)

        # Create parent observation for the graph
        parent_obs_id = str(uuid.uuid4())

        # Publish observation start event
        await publish_event(
            event_type="observation_start",
            trace_id=trace_id,
            observation_id=parent_obs_id,
            data={
                "name": trace_name,
                "type": "AGENT",
                "parent_observation_id": None,
                "input": _safe_copy(input_state),
                "start_time": datetime.utcnow().isoformat(),
            }
        )

        # Set as current observation
        parent_token = set_current_observation(parent_obs_id)

    except Exception as e:
        # If trace creation fails, continue without tracing
        logger.debug(f"⚠️ Failed to create trace: {e}")
        set_current_trace(None)  # Clean up any partial state
        return await original_ainvoke(input_state, config, **invoke_kwargs)

    # Run graph with trace context
    try:
        result = await original_ainvoke(input_state, config, **invoke_kwargs)

        # Publish observation end event (best effort)
        try:
            await publish_event(
                event_type="observation_end",
                trace_id=trace_id,
                observation_id=parent_obs_id,
                data={
                    "output": _safe_copy(result),
                    "level": "DEFAULT",
                    "end_time": datetime.utcnow().isoformat(),
                }
            )
        except Exception as e:
            logger.debug(f"Failed to end observation: {e}")

        return result

    except Exception as e:
        # Graph execution failed - try to log error observation
        try:
            await publish_event(
                event_type="observation_error",
                trace_id=trace_id,
                observation_id=parent_obs_id,
                data={
                    "level": "ERROR",
                    "error": str(e),
                    "end_time": datetime.utcnow().isoformat(),
                }
            )
        except:
            pass
        raise  # Re-raise the original error

    finally:
        # Clear observation and trace context
        if parent_token:
            set_current_observation(None, parent_token)
        set_current_trace(None)


def _safe_copy(data):
    """
    Safely deep copy data for tracing.
    
    Returns None if copy fails (never raises).
    """
    if data is None:
        return None
    try:
        if isinstance(data, dict):
            return copy.deepcopy(data)
        return None
    except Exception:
        return None
