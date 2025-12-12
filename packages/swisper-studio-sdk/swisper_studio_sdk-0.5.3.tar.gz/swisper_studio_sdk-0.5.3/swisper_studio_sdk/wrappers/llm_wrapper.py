"""
LLM Wrapper - Automatic capture of LLM calls

Intercepts Swisper's llm_adapter.get_structured_output() to capture prompts, 
responses, tokens, and model parameters.

v0.3.0: Now implemented based on actual Swisper code analysis.
"""

import logging
from typing import Optional
from ..tracing.context import get_current_observation

logger = logging.getLogger(__name__)

# Global state to track if wrapper is active
_llm_wrapper_active = False


def wrap_llm_adapter() -> None:
    """
    Wrap Swisper's TokenTrackingLLMAdapter to capture LLM telemetry.
    
    Based on analysis of Helvetiq codebase:
    - Path: backend.app.api.services.llm_adapter.token_tracking_llm_adapter
    - Method: get_structured_output(messages, schema, agent_type, ...)
    - Returns: StructuredOutputResult with result, token_usage, prompt_tokens, completion_tokens
    
    Called from: initialize_tracing()
    """
    global _llm_wrapper_active
    
    if _llm_wrapper_active:
        return  # Already wrapped
    
    try:
        # Import Swisper's LLM adapter
        from app.api.services.llm_adapter.token_tracking_llm_adapter import TokenTrackingLLMAdapter
        
        # Save original method
        original_get_structured_output = TokenTrackingLLMAdapter.get_structured_output
        
        # Create wrapper for get_structured_output
        async def wrapped_get_structured_output(self, messages, schema, agent_type=None, 
                                              on_reasoning_chunk=None, llm_reasoning_language=None, 
                                              metadata=None):
            """
            Wrapped get_structured_output that captures LLM telemetry.
            
            Captures:
            - Messages (prompts sent to LLM)
            - Reasoning chunks (<think>...</think>)
            - Result (LLM response)
            - Tokens (prompt + completion)
            - Agent type (for model identification)
            """
            obs_id = get_current_observation()
            
            if obs_id:
                logger.debug(f"LLM call intercepted for obs_id={obs_id[:8]}...")
                
                # Try to get actual model name from Swisper's config
                model_name = None
                try:
                    # TokenTrackingLLMAdapter wraps the actual adapter
                    # Access wrapped_adapter to get model config
                    if hasattr(self, 'wrapped_adapter') and hasattr(self.wrapped_adapter, '_get_model_config_for_agent_type'):
                        model_config = self.wrapped_adapter._get_model_config_for_agent_type(agent_type)
                        model_name = model_config.get('model') if model_config else None
                except Exception as e:
                    logger.debug(f"Could not get model name: {e}")
                
                # Store prompts + model info - PASS obs_id EXPLICITLY to avoid context issues
                _store_llm_input(obs_id, {
                    "messages": messages,
                    "agent_type": agent_type,
                    "model": model_name,  # Actual model name for cost calculation
                    "schema_name": schema.__name__ if schema else None,
                })
                
                # Intercept reasoning chunks if callback provided
                original_callback = on_reasoning_chunk
                
                if original_callback:
                    async def safe_reasoning_interceptor(chunk: str):
                        """
                        Intercept reasoning chunks for SDK capture.
                        
                        Safely accumulates reasoning while passing through to
                        original callback. Never propagates errors to LLM call.
                        """
                        try:
                            # Accumulate for SDK
                            _accumulate_reasoning(obs_id, chunk)
                        except Exception as e:
                            # NEVER break user's LLM call!
                            logger.debug(f"SDK reasoning capture failed: {e}")
                        
                        try:
                            # Pass through to original callback
                            await original_callback(chunk)
                        except Exception as e:
                            # Log but don't propagate
                            logger.debug(f"Original reasoning callback failed: {e}")
                    
                    # Replace callback with safe interceptor
                    on_reasoning_chunk = safe_reasoning_interceptor
            
            # Call original method (with intercepted callback)
            result = await original_get_structured_output(
                self, messages, schema, agent_type, 
                on_reasoning_chunk, llm_reasoning_language, metadata
            )
            
            # Store output data AFTER LLM call - PASS obs_id EXPLICITLY
            if obs_id:
                # Get accumulated reasoning (if any)
                reasoning_text = _get_accumulated_reasoning(obs_id)
                
                # Get model name from input data (stored earlier)
                model_name = None
                if obs_id in _llm_telemetry_store and 'input' in _llm_telemetry_store[obs_id]:
                    model_name = _llm_telemetry_store[obs_id]['input'].get('model')
                
                _store_llm_output(obs_id, {
                    "result": result.result.model_dump() if hasattr(result.result, 'model_dump') else str(result.result),
                    "reasoning": reasoning_text,  # Include reasoning!
                    "model": model_name,  # Model name for cost calculation
                    "total_tokens": result.token_usage,
                    "prompt_tokens": result.prompt_tokens,
                    "completion_tokens": result.completion_tokens,
                })
                logger.debug(f"LLM call completed for obs_id={obs_id[:8]}..., tokens={result.token_usage}")
            
            return result
        
        # Save original streaming method
        original_stream = TokenTrackingLLMAdapter.stream_message_from_LLM
        
        # Create wrapper for stream_message_from_LLM
        async def wrapped_stream_message_from_LLM(self, messages, agent_type=None, metadata=None):
            """
            Wrapped streaming that captures prompts and final aggregated response.
            
            Captures:
            - Messages (prompts)
            - Streaming response chunks (accumulated)
            - Tokens (from final chunk)
            
            Zero latency - streaming passes through immediately.
            """
            obs_id = get_current_observation()
            
            if obs_id:
                logger.debug(f"Streaming LLM call intercepted for obs_id={obs_id[:8]}...")
                
                # Try to get model name
                model_name = None
                try:
                    # Access wrapped_adapter to get model config
                    if hasattr(self, 'wrapped_adapter') and hasattr(self.wrapped_adapter, '_get_model_config_for_agent_type'):
                        model_config = self.wrapped_adapter._get_model_config_for_agent_type(agent_type)
                        model_name = model_config.get('model') if model_config else None
                except Exception as e:
                    logger.debug(f"Could not get model name: {e}")
                
                # Store prompts - PASS obs_id EXPLICITLY
                _store_llm_input(obs_id, {
                    "messages": messages,
                    "agent_type": agent_type,
                    "model": model_name,
                })
            
            # Accumulate response chunks and tokens
            accumulated_tokens = {
                'total_tokens': 0,
                'prompt_tokens': 0,
                'completion_tokens': 0
            }
            
            # Stream through (zero delay!)
            try:
                async for chunk in original_stream(self, messages, agent_type, metadata):
                    # Accumulate response content
                    if obs_id and isinstance(chunk, dict):
                        if 'content' in chunk:
                            _accumulate_response(obs_id, chunk['content'])
                        
                        # Capture token info (usually in final chunks)
                        # Swisper's TokenTrackingLLMAdapter passes through usage from chunks
                        if 'usage' in chunk:
                            usage = chunk['usage']
                            if 'total_tokens' in usage:
                                accumulated_tokens['total_tokens'] = usage.get('total_tokens', 0)
                            if 'prompt_tokens' in usage:
                                accumulated_tokens['prompt_tokens'] = usage.get('prompt_tokens', 0)
                            if 'completion_tokens' in usage:
                                accumulated_tokens['completion_tokens'] = usage.get('completion_tokens', 0)
                    
                    yield chunk  # ← Pass through immediately (zero latency)
                
                # After streaming completes - store final data - PASS obs_id EXPLICITLY
                if obs_id:
                    final_response = _get_accumulated_response(obs_id)
                    
                    # Get model name from input
                    model_name = None
                    if obs_id in _llm_telemetry_store and 'input' in _llm_telemetry_store[obs_id]:
                        model_name = _llm_telemetry_store[obs_id]['input'].get('model')
                    
                    # Only store tokens if we actually got them (don't store 0 as None)
                    token_data = {}
                    if accumulated_tokens['total_tokens'] > 0:
                        token_data['total_tokens'] = accumulated_tokens['total_tokens']
                        token_data['prompt_tokens'] = accumulated_tokens['prompt_tokens']
                        token_data['completion_tokens'] = accumulated_tokens['completion_tokens']
                    else:
                        # No tokens captured from streaming - log warning
                        logger.debug(f"No token usage captured from streaming (agent_type={agent_type})")
                        # Store None explicitly so we know streaming was attempted
                        token_data['total_tokens'] = None
                        token_data['prompt_tokens'] = None
                        token_data['completion_tokens'] = None
                    
                    _store_llm_output(obs_id, {
                        "result": final_response,  # Full streamed response
                        "reasoning": None,  # Streaming usually doesn't have <think> tags
                        "model": model_name,  # Model name for cost calculation
                        **token_data
                    })
                    logger.debug(f"Streaming LLM call completed for obs_id={obs_id[:8]}...")
                    
            except Exception as e:
                # Let error propagate but log for debugging
                logger.debug(f"Error during streaming: {e}")
                raise
        
        # Replace both methods
        TokenTrackingLLMAdapter.get_structured_output = wrapped_get_structured_output
        TokenTrackingLLMAdapter.stream_message_from_LLM = wrapped_stream_message_from_LLM
        _llm_wrapper_active = True
        
        logger.info("✅ LLM adapter wrapped for prompt capture (structured + streaming)")
        
    except ImportError as e:
        # Swisper structure different or not running in Swisper context
        logger.debug(f"LLM adapter not available for wrapping: {e}")
        pass
    except Exception as e:
        logger.warning(f"Failed to wrap LLM adapter: {e}")
        pass


# Global storage for LLM telemetry (temporary until observation update)
_llm_telemetry_store = {}

# Default reasoning configuration
_default_max_reasoning_length = 50000  # 50 KB default


def set_default_reasoning_config(max_length: int = 50000) -> None:
    """Set global default for reasoning capture"""
    global _default_max_reasoning_length
    _default_max_reasoning_length = max_length


def _store_llm_input(obs_id: str, data: dict) -> None:
    """
    Store LLM input data for a specific observation.
    
    IMPORTANT: obs_id must be passed explicitly to avoid context propagation issues
    in async code with LangGraph orchestration. Do NOT call get_current_observation()
    here - the caller has the authoritative obs_id.
    
    Args:
        obs_id: Observation ID (must be passed from caller, not fetched from context)
        data: Input data dict (messages, agent_type, model, etc.)
    """
    if not obs_id:
        logger.debug("_store_llm_input called with None obs_id, skipping")
        return
    
    if obs_id not in _llm_telemetry_store:
        _llm_telemetry_store[obs_id] = {
            'reasoning_chunks': [],  # For accumulating reasoning
            'response_chunks': [],   # For accumulating streaming responses
        }
    _llm_telemetry_store[obs_id]['input'] = data
    logger.debug(f"Stored LLM input for obs_id={obs_id[:8]}...")


def _store_llm_output(obs_id: str, data: dict) -> None:
    """
    Store LLM output data for a specific observation.
    
    IMPORTANT: obs_id must be passed explicitly to avoid context propagation issues
    in async code with LangGraph orchestration. Do NOT call get_current_observation()
    here - the caller has the authoritative obs_id.
    
    Args:
        obs_id: Observation ID (must be passed from caller, not fetched from context)
        data: Output data dict (result, tokens, reasoning, etc.)
    """
    if not obs_id:
        logger.debug("_store_llm_output called with None obs_id, skipping")
        return
    
    if obs_id not in _llm_telemetry_store:
        _llm_telemetry_store[obs_id] = {
            'reasoning_chunks': [],
            'response_chunks': [],
        }
    _llm_telemetry_store[obs_id]['output'] = data
    logger.debug(f"Stored LLM output for obs_id={obs_id[:8]}...")


def _accumulate_reasoning(obs_id: str, chunk: str) -> None:
    """Accumulate reasoning chunk for an observation"""
    if obs_id in _llm_telemetry_store:
        _llm_telemetry_store[obs_id]['reasoning_chunks'].append(chunk)
    else:
        # Observation might have already ended - ignore late chunks
        logger.debug(f"Ignoring late reasoning chunk for ended observation {obs_id}")


def _get_accumulated_reasoning(obs_id: str, max_length: int = None) -> Optional[str]:
    """
    Get accumulated reasoning text with optional truncation.
    
    Args:
        obs_id: Observation ID
        max_length: Maximum characters (default: 50000)
    
    Returns:
        Full or truncated reasoning text, or None if no reasoning captured
    """
    if obs_id not in _llm_telemetry_store:
        return None
    
    chunks = _llm_telemetry_store[obs_id].get('reasoning_chunks', [])
    if not chunks:
        return None
    
    full_text = ''.join(chunks)
    
    # Apply truncation if needed
    max_len = max_length or _default_max_reasoning_length
    if len(full_text) > max_len:
        return (
            full_text[:max_len] +
            f"\n\n... [Truncated. Full length: {len(full_text):,} characters]"
        )
    
    return full_text


def _accumulate_response(obs_id: str, chunk: str) -> None:
    """Accumulate streaming response chunk"""
    if obs_id in _llm_telemetry_store:
        _llm_telemetry_store[obs_id]['response_chunks'].append(chunk)


def _get_accumulated_response(obs_id: str) -> Optional[str]:
    """Get accumulated streaming response text"""
    if obs_id not in _llm_telemetry_store:
        return None
    
    chunks = _llm_telemetry_store[obs_id].get('response_chunks', [])
    return ''.join(chunks) if chunks else None


def get_llm_telemetry(obs_id: str) -> Optional[dict]:
    """Get stored LLM telemetry for an observation"""
    return _llm_telemetry_store.get(obs_id)


def cleanup_observation(obs_id: str) -> None:
    """
    Cleanup LLM telemetry for an observation (prevent memory leaks).
    
    Call this after observation is sent to SwisperStudio.
    """
    if obs_id in _llm_telemetry_store:
        del _llm_telemetry_store[obs_id]
        logger.debug(f"Cleaned up telemetry for observation {obs_id}")


