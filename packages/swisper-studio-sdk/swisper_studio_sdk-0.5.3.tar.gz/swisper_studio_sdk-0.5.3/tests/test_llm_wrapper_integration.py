"""
Tests for LLM wrapper integration

These tests verify that LLM adapter wrapping works correctly
and captures prompts, responses, and tokens.

Issue #2 from Swisper integration feedback.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch


class TestLLMWrapperIntegration:
    """Verify LLM wrapper captures telemetry correctly"""

    @pytest.mark.asyncio
    async def test_llm_wrapper_captures_messages(self):
        """
        LLM wrapper should capture messages sent to LLM.
        
        When get_structured_output() is called, wrapper should:
        1. Capture messages array
        2. Call original method
        3. Return result unchanged
        4. Store messages for observation
        """
        from swisper_studio_sdk.wrappers.llm_wrapper import wrap_llm_adapter, get_llm_telemetry
        from swisper_studio_sdk.tracing.context import set_current_observation
        
        # Mock Swisper's LLM adapter
        with patch('app.api.services.llm_adapter.token_tracking_llm_adapter.TokenTrackingLLMAdapter') as MockAdapter:
            # Setup mock
            mock_result = MagicMock()
            mock_result.result = MagicMock()
            mock_result.result.model_dump = lambda: {"intent": "test"}
            mock_result.token_usage = 100
            mock_result.prompt_tokens = 60
            mock_result.completion_tokens = 40
            
            MockAdapter.get_structured_output = AsyncMock(return_value=mock_result)
            
            # Wrap the adapter
            wrap_llm_adapter()
            
            # Set observation context
            obs_id = "test-obs-123"
            set_current_observation(obs_id)
            
            # Simulate LLM call
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Test message"}
            ]
            
            # This should capture telemetry
            # (In real scenario, this would be called by Swisper code)
            
            # Verify telemetry was stored
            telemetry = get_llm_telemetry(obs_id)
            
            # Should have captured messages
            assert telemetry is not None, "LLM telemetry not captured!"
            assert 'input' in telemetry
            assert telemetry['input']['messages'] == messages

    @pytest.mark.asyncio
    async def test_llm_wrapper_captures_tokens(self):
        """LLM wrapper should capture token counts"""
        from swisper_studio_sdk.wrappers.llm_wrapper import get_llm_telemetry
        
        # Mock test similar to above
        # Verify token counts captured
        pass  # TODO: Implement full mock

    @pytest.mark.asyncio
    async def test_llm_wrapper_does_not_interfere_with_result(self):
        """
        LLM wrapper should not change the result.
        Observability should be transparent.
        """
        # Verify result from wrapped call == result from original call
        pass  # TODO: Implement

    @pytest.mark.asyncio
    async def test_llm_wrapper_graceful_if_not_in_swisper(self):
        """
        LLM wrapper should fail gracefully if not in Swisper context.
        SDK should work in any environment.
        """
        from swisper_studio_sdk.wrappers.llm_wrapper import wrap_llm_adapter
        
        # Calling wrap_llm_adapter() outside Swisper should not crash
        try:
            wrap_llm_adapter()
            # Should not raise, just log and continue
        except ImportError:
            pass  # Expected if not in Swisper
        except Exception as e:
            pytest.fail(f"Should fail gracefully, but raised: {e}")

