"""
Tests for LLM wrapper - automatic capture of LLM calls

These tests verify that LLM calls are automatically intercepted
and telemetry is captured (prompts, tokens, model parameters).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestLLMWrapperInterception:
    """Test LLM wrapper intercepts llm_adapter calls"""

    @pytest.mark.asyncio
    async def test_llm_call_captures_prompt_messages(self):
        """LLM wrapper captures prompt messages sent to LLM"""
        from swisper_studio_sdk.wrappers.llm_wrapper import wrap_llm_adapter
        from swisper_studio_sdk.tracing.context import get_current_observation_context
        
        # Mock llm_adapter module
        mock_adapter = MagicMock()
        mock_adapter.get_structured_output = AsyncMock(
            return_value={"intent": "test_intent"}
        )
        
        # Wrap it
        with patch.dict('sys.modules', {'swisper.backend.app.services.llm_adapter': mock_adapter}):
            wrap_llm_adapter()
            
            # Simulate LLM call
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "What's my next meeting?"}
            ]
            
            result = await mock_adapter.get_structured_output(
                messages=messages,
                model="gpt-4-turbo"
            )
            
            # Verify telemetry captured
            ctx = get_current_observation_context()
            assert ctx is not None
            assert "llm_telemetry" in ctx
            assert ctx["llm_telemetry"]["input"]["messages"] == messages

    @pytest.mark.asyncio
    async def test_llm_call_captures_model_and_parameters(self):
        """LLM wrapper captures model name and parameters"""
        from swisper_studio_sdk.wrappers.llm_wrapper import wrap_llm_adapter
        from swisper_studio_sdk.tracing.context import get_current_observation_context
        
        mock_adapter = MagicMock()
        mock_adapter.get_structured_output = AsyncMock(
            return_value={"result": "test"}
        )
        
        with patch.dict('sys.modules', {'swisper.backend.app.services.llm_adapter': mock_adapter}):
            wrap_llm_adapter()
            
            result = await mock_adapter.get_structured_output(
                messages=[{"role": "user", "content": "test"}],
                model="gpt-4-turbo",
                temperature=0.8,
                max_tokens=2000,
                top_p=0.9
            )
            
            ctx = get_current_observation_context()
            assert ctx["llm_telemetry"]["model"] == "gpt-4-turbo"
            assert ctx["llm_telemetry"]["model_parameters"]["temperature"] == 0.8
            assert ctx["llm_telemetry"]["model_parameters"]["max_tokens"] == 2000
            assert ctx["llm_telemetry"]["model_parameters"]["top_p"] == 0.9

    @pytest.mark.asyncio
    async def test_llm_call_counts_tokens(self):
        """LLM wrapper counts prompt and completion tokens"""
        from swisper_studio_sdk.wrappers.llm_wrapper import wrap_llm_adapter
        from swisper_studio_sdk.tracing.context import get_current_observation_context
        
        mock_adapter = MagicMock()
        mock_adapter.get_structured_output = AsyncMock(
            return_value={"intent": "calendar_query", "confidence": 0.95}
        )
        
        with patch.dict('sys.modules', {'swisper.backend.app.services.llm_adapter': mock_adapter}):
            wrap_llm_adapter()
            
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "What's my next meeting with Sarah?"}
            ]
            
            result = await mock_adapter.get_structured_output(
                messages=messages,
                model="gpt-4"
            )
            
            ctx = get_current_observation_context()
            assert "prompt_tokens" in ctx["llm_telemetry"]
            assert "completion_tokens" in ctx["llm_telemetry"]
            assert ctx["llm_telemetry"]["prompt_tokens"] > 0
            assert ctx["llm_telemetry"]["completion_tokens"] > 0

    @pytest.mark.asyncio
    async def test_observation_type_set_to_generation(self):
        """Observation with LLM telemetry gets type=GENERATION"""
        from swisper_studio_sdk.tracing.decorator import traced
        from swisper_studio_sdk.wrappers.llm_wrapper import wrap_llm_adapter
        
        mock_adapter = MagicMock()
        mock_adapter.get_structured_output = AsyncMock(
            return_value={"result": "test"}
        )
        
        with patch.dict('sys.modules', {'swisper.backend.app.services.llm_adapter': mock_adapter}):
            wrap_llm_adapter()
            
            @traced("llm_node")
            async def test_node(state):
                # Simulate LLM call
                result = await mock_adapter.get_structured_output(
                    messages=[{"role": "user", "content": "test"}],
                    model="gpt-4"
                )
                return state
            
            # Execute node
            state = {"test": "data"}
            await test_node(state)
            
            # Verify observation was created with type=GENERATION
            # (Would check via API in integration test)
            # For unit test, we check context
            from swisper_studio_sdk.tracing.context import get_current_observation_context
            ctx = get_current_observation_context()
            assert ctx["observation_type"] == "GENERATION"


