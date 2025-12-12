"""
Tests for state capture deep copy fix

These tests verify that state mutations after capture
don't affect the captured input/output data.

Issue #3 from Swisper integration feedback.
"""

import pytest
import asyncio


class TestDeepCopyStateMutations:
    """Verify state is deep copied, not shallow copied"""

    @pytest.mark.asyncio
    async def test_state_mutation_after_input_capture_does_not_affect_input(self):
        """
        CRITICAL: State mutations after input capture should not change captured input.
        
        Bug: SDK uses dict(state) which creates shallow copy.
        When state is mutated during node execution, input_data also changes.
        This breaks state diff view.
        """
        from swisper_studio_sdk.tracing.decorator import traced
        from swisper_studio_sdk.tracing.client import initialize_tracing
        
        # Initialize tracing (will need mock)
        initialize_tracing(
            api_url="http://mock",
            api_key="test",
            project_id="test",
            enabled=False  # Use mock for unit test
        )
        
        # Create state with nested dict
        test_state = {
            "message": "test",
            "nested": {"value": "original"},
            "list": [1, 2, 3]
        }
        
        captured_input = None
        captured_output = None
        
        @traced("test_node")
        async def mutating_node(state):
            nonlocal captured_input, captured_output
            
            # Simulate SDK capturing input (this is what SDK does internally)
            # Bug: Uses dict() which is shallow copy
            captured_input = dict(state)  # Current SDK behavior
            
            # Node mutates state (normal LangGraph behavior)
            state["message"] = "modified"
            state["nested"]["value"] = "changed"  # Nested mutation!
            state["list"].append(4)
            state["new_field"] = "added"
            
            # Simulate SDK capturing output
            captured_output = dict(state)
            
            return state
        
        # Execute
        result = await mutating_node(test_state)
        
        # EXPECTED BEHAVIOR (with deep copy):
        # captured_input should show original values
        # captured_output should show modified values
        
        # ACTUAL BEHAVIOR (with shallow copy):
        # Both show modified values (BUG!)
        
        # This test should FAIL with current SDK
        assert captured_input["message"] == "test"  # Should be "test", not "modified"
        assert captured_input["nested"]["value"] == "original"  # Should be "original", not "changed"
        assert captured_input["list"] == [1, 2, 3]  # Should be [1,2,3], not [1,2,3,4]
        assert "new_field" not in captured_input  # Should not exist in input

    @pytest.mark.asyncio
    async def test_nested_dict_mutation_isolated(self):
        """Nested dict changes should not affect captured input"""
        import copy
        
        state = {"data": {"count": 0, "items": []}}
        
        # Shallow copy (WRONG - current SDK)
        shallow = dict(state)
        
        # Mutate original
        state["data"]["count"] = 10
        state["data"]["items"].append("item1")
        
        # This will FAIL because shallow copy shares nested objects
        assert shallow["data"]["count"] == 0  # FAILS - shows 10
        assert shallow["data"]["items"] == []  # FAILS - shows ["item1"]
        
    @pytest.mark.asyncio
    async def test_deep_copy_isolates_mutations(self):
        """Deep copy should properly isolate state"""
        import copy
        
        state = {"data": {"count": 0, "items": []}}
        
        # Deep copy (CORRECT - what we need)
        deep = copy.deepcopy(state)
        
        # Mutate original
        state["data"]["count"] = 10
        state["data"]["items"].append("item1")
        
        # This should PASS
        assert deep["data"]["count"] == 0  # PASSES - isolated
        assert deep["data"]["items"] == []  # PASSES - isolated

