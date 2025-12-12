"""
@traced decorator for automatic tracing

Captures function inputs, outputs, and execution time.
Works with both sync and async functions.

v0.5.1: ROBUST FAILURE HANDLING
- All operations have timeouts
- SDK NEVER blocks Swisper, even with misconfiguration
- All exceptions caught and logged, never propagated
"""

import asyncio
import copy
import functools
import logging
import time
import uuid
from datetime import datetime
from typing import TypeVar, Callable

from .client import get_studio_client
from .context import get_current_trace, get_current_observation, set_current_observation
from .redis_publisher import publish_event, get_redis_client

logger = logging.getLogger(__name__)

# ============================================================================
# CRITICAL DESIGN PRINCIPLE:
# The SDK must NEVER block or crash Swisper, even if:
# - Redis is misconfigured
# - Redis is unreachable
# - SwisperStudio is down
# - Any timeout occurs
#
# All tracing operations fail silently.
# ============================================================================

T = TypeVar('T')


def _detect_observation_type(
    observation_name: str,
    has_llm_data: bool,
    has_tool_data: bool
) -> str:
    """
    Auto-detect observation type based on captured data and naming.

    Priority order:
    1. LLM data → GENERATION
    2. Tool data → TOOL
    3. Name contains "agent" → AGENT
    4. Default → SPAN

    Args:
        observation_name: Name of the observation/node
        has_llm_data: Whether LLM telemetry was captured (must have input or output)
        has_tool_data: Whether tool telemetry was captured

    Returns:
        Observation type string (GENERATION, TOOL, AGENT, or SPAN)
    """
    # Priority 1: LLM data
    if has_llm_data:
        logger.debug(f"Detected GENERATION type for {observation_name} (has LLM data)")
        return "GENERATION"

    # Priority 2: Tool data
    if has_tool_data:
        logger.debug(f"Detected TOOL type for {observation_name} (has tool data)")
        return "TOOL"

    # Priority 3: Agent naming pattern
    if "agent" in observation_name.lower():
        logger.debug(f"Detected AGENT type for {observation_name} (name contains 'agent')")
        return "AGENT"

    # Default
    logger.debug(f"Defaulting to SPAN type for {observation_name}")
    return "SPAN"


def traced(
    name: str | None = None,
    observation_type: str = "AUTO",  # AUTO = detect based on LLM data
    capture_reasoning: bool = True,  # Capture LLM reasoning (<think>...</think>)
    reasoning_max_length: int | None = None,  # Max reasoning chars (None = use default 50KB)
):
    """
    Auto-trace any function/node with optional reasoning capture.

    Usage:
        # Default (captures reasoning if available)
        @traced("classify_intent")
        async def classify_intent_node(state):
            return state

        # Disable reasoning for this node
        @traced("memory_node", capture_reasoning=False)
        async def memory_node(state):
            return state

        # Custom reasoning length limit
        @traced("global_planner", capture_reasoning=True, reasoning_max_length=20000)
        async def global_planner_node(state):
            return state

    Args:
        name: Observation name (defaults to function name)
        observation_type: Type of observation (SPAN, GENERATION, TOOL, AGENT, AUTO)
                         AUTO = Auto-detect based on captured LLM data
        capture_reasoning: Whether to capture LLM reasoning for this node
        reasoning_max_length: Max reasoning characters (None = use default 50KB)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        obs_name = name or func.__name__

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            # Check if Redis publisher is initialized
            redis_client = get_redis_client()
            if not redis_client:
                # Tracing not initialized, just run function
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

            # Get current trace context
            trace_id = get_current_trace()
            if not trace_id:
                # No active trace, skip tracing
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

            # Capture input (LangGraph state is a dict or TypedDict)
            # CRITICAL: Must use deep copy to avoid mutations affecting captured state
            input_data = None
            if args:
                try:
                    state = args[0]
                    # TypedDict/dict (most common for LangGraph)
                    if isinstance(state, dict):
                        input_data = copy.deepcopy(state)  # DEEP copy to isolate mutations!
                    # Pydantic models
                    elif hasattr(state, 'model_dump'):
                        input_data = state.model_dump()
                    elif hasattr(state, 'dict'):
                        input_data = state.dict()
                    # Other objects with __dict__
                    elif hasattr(state, '__dict__'):
                        input_data = copy.deepcopy(vars(state))  # DEEP copy
                except Exception:
                    # Skip if serialization fails
                    pass

            # Get parent observation (for nesting)
            parent_obs = get_current_observation()

            # FIRE-AND-FORGET: Generate observation ID locally (no waiting)
            obs_id = str(uuid.uuid4())

            # Determine initial type (can't send "AUTO" to API)
            initial_type = "SPAN" if observation_type == "AUTO" else observation_type

            # REDIS STREAMS: Publish observation start event (1-2ms, non-blocking)
            await publish_event(
                event_type="observation_start",
                trace_id=trace_id,
                observation_id=obs_id,
                data={
                    "name": obs_name,
                    "type": initial_type,
                    "parent_observation_id": parent_obs,
                    "input": input_data,
                    "start_time": datetime.utcnow().isoformat(),
                }
            )

            # Set as current observation immediately (for nested calls)
            token = set_current_observation(obs_id)

            try:
                # Execute function
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                # Capture output (LangGraph returns dict or TypedDict)
                # CRITICAL: Must use deep copy to isolate from input mutations
                output_data = None
                try:
                    # TypedDict/dict (most common for LangGraph)
                    if isinstance(result, dict):
                        output_data = copy.deepcopy(result)  # DEEP copy!
                    # Pydantic models
                    elif hasattr(result, 'model_dump'):
                        output_data = result.model_dump()
                    elif hasattr(result, 'dict'):
                        output_data = result.dict()
                    # Other objects
                    elif hasattr(result, '__dict__'):
                        output_data = copy.deepcopy(vars(result))  # DEEP copy
                except Exception:
                    pass

                # Check if LLM telemetry was captured for this observation
                llm_data = None
                has_llm_data = False
                try:
                    from ..wrappers.llm_wrapper import get_llm_telemetry, _llm_telemetry_store
                    llm_data = get_llm_telemetry(obs_id)
                    
                    # has_llm_data is True only if we have actual input or output data
                    # (not just the base structure with empty chunks)
                    has_llm_data = bool(
                        llm_data and 
                        ('input' in llm_data or 'output' in llm_data)
                    )
                    
                    # Debug: Log whether LLM data was found
                    if has_llm_data:
                        has_input = 'input' in llm_data
                        has_output = 'output' in llm_data
                        logger.debug(
                            f"✅ LLM telemetry found for {obs_name} "
                            f"(obs_id={obs_id[:8]}..., input={has_input}, output={has_output})"
                        )
                    else:
                        # Check if telemetry exists under different keys (debugging context mismatch)
                        if _llm_telemetry_store:
                            stored_keys = list(_llm_telemetry_store.keys())
                            logger.debug(
                                f"⚠️ No LLM telemetry for {obs_name} (obs_id={obs_id[:8]}...). "
                                f"Store has {len(stored_keys)} entries: {[k[:8]+'...' for k in stored_keys[:3]]}"
                            )
                        else:
                            logger.debug(f"ℹ️ No LLM telemetry for {obs_name} (no LLM calls made)")
                except Exception as e:
                    logger.debug(f"Failed to get LLM telemetry for {obs_name}: {e}")

                # Merge LLM data into output if available
                final_output = output_data or {}
                if llm_data:
                    # Add LLM prompt/response data
                    if 'input' in llm_data and llm_data['input'].get('messages'):
                        final_output['_llm_messages'] = llm_data['input']['messages']

                    if 'output' in llm_data:
                        final_output['_llm_result'] = llm_data['output'].get('result')

                        # Add model name for cost calculation
                        if llm_data['output'].get('model'):
                            final_output['_llm_model'] = llm_data['output']['model']

                        # Add reasoning if enabled and available
                        if capture_reasoning and llm_data['output'].get('reasoning'):
                            # Import reasoning function here to apply node-specific max length
                            from ..wrappers.llm_wrapper import _get_accumulated_reasoning
                            reasoning_text = _get_accumulated_reasoning(obs_id, reasoning_max_length)
                            if reasoning_text:
                                final_output['_llm_reasoning'] = reasoning_text

                        final_output['_llm_tokens'] = {
                            'total': llm_data['output'].get('total_tokens'),
                            'prompt': llm_data['output'].get('prompt_tokens'),
                            'completion': llm_data['output'].get('completion_tokens'),
                        }

                # AUTO-DETECT observation type if set to "AUTO"
                final_type = observation_type

                if observation_type == "AUTO":
                    final_type = _detect_observation_type(obs_name, has_llm_data, False)

                # FLEXIBLE TOOL EXTRACTION (v0.5.0 Enhancement):
                # Extract tools from ANY observation that has _tools_executed
                # No longer requires node to be named "tool_execution"
                #
                # Supports TWO patterns:
                # Pattern 1: Separate tool_execution node (productivity_agent, doc_agent, wealth_agent)
                # Pattern 2: Tools in agent observation (research_agent)
                #
                # v0.5.1: All tool extraction wrapped in try-except (never fails)

                try:
                    # Debug: Check conditions
                    has_tools_in_output = (final_output and '_tools_executed' in final_output and len(final_output.get('_tools_executed', [])) > 0)

                    # Check ownership to prevent duplicate extraction (v0.5.0 anti-duplication)
                    created_by = final_output.get('_tools_executed_by') if final_output else None
                    is_owner = (created_by is None or created_by == obs_name)

                    should_extract_tools = (
                        (obs_name == "tool_execution" and is_owner)
                        or (has_tools_in_output and is_owner)
                    )

                    # Debug logging
                    if has_tools_in_output:
                        if is_owner:
                            logger.debug(f"Found _tools_executed in {obs_name}: {len(final_output.get('_tools_executed', []))} tools")
                        else:
                            logger.debug(f"Skipping _tools_executed in {obs_name} (owned by: {created_by})")

                    if should_extract_tools and final_output:
                        try:
                            from .tool_observer import create_tool_observations

                            # Universal tool extraction with timeout
                            tool_count = await asyncio.wait_for(
                                create_tool_observations(
                                    trace_id=trace_id,
                                    parent_observation_id=obs_id,
                                    output=final_output
                                ),
                                timeout=5.0  # 5s timeout for tool extraction
                            )

                            if tool_count > 0:
                                logger.debug(f"Extracted {tool_count} tools from {obs_name}")

                        except asyncio.TimeoutError:
                            logger.debug(f"Timeout extracting tools from {obs_name}")
                        except Exception as e:
                            logger.debug(f"Failed to extract tools from {obs_name}: {e}")
                except Exception as e:
                    # Never fail on tool extraction
                    logger.debug(f"Tool extraction check failed: {e}")

                # REDIS STREAMS: Publish observation end event (1-2ms, non-blocking)
                await publish_event(
                    event_type="observation_end",
                    trace_id=trace_id,
                    observation_id=obs_id,
                    data={
                        "output": final_output,
                        "level": "DEFAULT",
                        "type": final_type,  # Final detected type
                        "end_time": datetime.utcnow().isoformat(),
                    }
                )

                # Cleanup telemetry to prevent memory leaks
                try:
                    from ..wrappers.llm_wrapper import cleanup_observation
                    cleanup_observation(obs_id)
                except:
                    pass

                return result

            except Exception as e:
                # REDIS STREAMS: Publish observation error event
                await publish_event(
                    event_type="observation_error",
                    trace_id=trace_id,
                    observation_id=obs_id,
                    data={
                        "level": "ERROR",
                        "error": str(e),
                        "status_message": str(e),
                        "end_time": datetime.utcnow().isoformat(),
                    }
                )
                raise

            finally:
                # Reset observation context
                set_current_observation(parent_obs, token)

        # Return appropriate wrapper
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            # For sync functions, wrap in async
            @functools.wraps(func)
            async def sync_wrapper(*args, **kwargs) -> T:
                return await async_wrapper(*args, **kwargs)
            return sync_wrapper

    return decorator

