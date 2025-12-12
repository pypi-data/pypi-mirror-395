"""
Tests for observation type detection

Verifies that observation types are correctly inferred from captured data.
"""

import pytest


class TestObservationTypeDetection:
    """Test automatic type detection"""

    def test_agent_nodes_get_agent_type(self):
        """Nodes with 'agent' in name get AGENT type"""
        from swisper_studio_sdk.tracing.decorator import _detect_observation_type
        
        # Test various agent naming patterns
        assert _detect_observation_type("productivity_agent", False, False) == "AGENT"
        assert _detect_observation_type("research_agent", False, False) == "AGENT"
        assert _detect_observation_type("my_agent_node", False, False) == "AGENT"
        assert _detect_observation_type("agent_handler", False, False) == "AGENT"

    def test_llm_data_gets_generation_type(self):
        """Nodes with LLM telemetry get GENERATION type"""
        from swisper_studio_sdk.tracing.decorator import _detect_observation_type
        
        # has_llm_data=True → GENERATION
        assert _detect_observation_type("intent_classification", True, False) == "GENERATION"
        assert _detect_observation_type("any_node_name", True, False) == "GENERATION"

    def test_tool_data_gets_tool_type(self):
        """Nodes with tool telemetry get TOOL type"""
        from swisper_studio_sdk.tracing.decorator import _detect_observation_type
        
        # has_tool_data=True → TOOL
        assert _detect_observation_type("get_calendar", False, True) == "TOOL"
        assert _detect_observation_type("any_node_name", False, True) == "TOOL"

    def test_default_nodes_get_span_type(self):
        """Nodes with no special data get SPAN type"""
        from swisper_studio_sdk.tracing.decorator import _detect_observation_type
        
        # No special indicators → SPAN
        assert _detect_observation_type("memory_node", False, False) == "SPAN"
        assert _detect_observation_type("planner", False, False) == "SPAN"
        assert _detect_observation_type("ui_node", False, False) == "SPAN"

    def test_llm_takes_precedence_over_agent_name(self):
        """LLM data takes precedence over agent naming"""
        from swisper_studio_sdk.tracing.decorator import _detect_observation_type
        
        # Even if name has "agent", LLM data → GENERATION
        assert _detect_observation_type("my_agent", True, False) == "GENERATION"


