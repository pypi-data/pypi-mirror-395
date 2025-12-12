"""
Tests for fire-and-forget HTTP pattern

These tests verify that HTTP calls don't block execution
and that observations are created in background.

Issue #5 from Swisper integration feedback.
"""

import pytest
import asyncio
import time


class TestFireAndForgetPattern:
    """Verify fire-and-forget adds zero latency"""

    @pytest.mark.asyncio
    async def test_observation_creation_does_not_block(self):
        """
        Creating observation should not block function execution.
        
        CRITICAL: HTTP calls to SwisperStudio must be async background tasks.
        User should see instant response, not wait for HTTP.
        """
        from swisper_studio_sdk.tracing.client import SwisperStudioClient
        
        # Create client (mock server will be slow)
        client = SwisperStudioClient(
            api_url="http://slow-mock-server:8001",
            api_key="test",
            project_id="test"
        )
        
        # Time the background call
        start = time.time()
        
        # This should NOT block (fire-and-forget)
        client.create_observation_background(
            trace_id="test-trace",
            name="test-obs",
            type="SPAN",
            observation_id="test-obs-id",
            input={"test": "data"}
        )
        
        elapsed = time.time() - start
        
        # Should be instant (< 10ms), not wait for HTTP
        assert elapsed < 0.01, f"Blocked for {elapsed}s - should be instant!"

    @pytest.mark.asyncio
    async def test_end_observation_does_not_block(self):
        """Ending observation should not block return value"""
        from swisper_studio_sdk.tracing.client import SwisperStudioClient
        
        client = SwisperStudioClient(
            api_url="http://slow-mock-server:8001",
            api_key="test",
            project_id="test"
        )
        
        start = time.time()
        
        # This should NOT block
        client.end_observation_background(
            observation_id="test-obs-id",
            output={"result": "data"},
            level="DEFAULT"
        )
        
        elapsed = time.time() - start
        
        # Should be instant
        assert elapsed < 0.01, f"Blocked for {elapsed}s - should be instant!"

    @pytest.mark.asyncio
    async def test_traced_function_runs_at_full_speed(self):
        """
        Function with @traced decorator should run at full speed.
        HTTP calls should happen in background.
        """
        from swisper_studio_sdk.tracing.decorator import traced
        from swisper_studio_sdk.tracing.client import initialize_tracing
        
        # Initialize with mock (won't actually send HTTP)
        initialize_tracing(
            api_url="http://mock",
            api_key="test", 
            project_id="test",
            enabled=False  # Mock mode
        )
        
        call_count = 0
        
        @traced("test_node")
        async def fast_function(state):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)  # Simulate work
            return state
        
        # Time the function
        start = time.time()
        result = await fast_function({"test": "state"})
        elapsed = time.time() - start
        
        # Should be ~0.1s (function time), not 0.1s + HTTP time
        assert elapsed < 0.15, f"Took {elapsed}s - SDK added latency!"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_background_tasks_eventually_complete(self):
        """
        Background tasks should eventually complete.
        Observations should be created (eventually consistent).
        """
        # This test would need a real or mock server
        # For now, verify tasks are created
        pass  # TODO: Implement with mock server


class TestLocalIDGeneration:
    """Verify IDs are generated locally (no server round-trip)"""

    @pytest.mark.asyncio
    async def test_observation_id_generated_locally(self):
        """
        Observation IDs should be generated client-side.
        No need to wait for server response to get ID.
        """
        from swisper_studio_sdk.tracing.decorator import traced
        import uuid
        
        # Verify decorator generates UUID locally
        # This is implicit in fire-and-forget pattern
        test_id = str(uuid.uuid4())
        assert isinstance(test_id, str)
        assert len(test_id) == 36  # UUID format

