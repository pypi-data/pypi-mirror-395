"""
Tool observation creator - UNIVERSAL tool extraction from ANY agent format

Creates separate TOOL observations for each tool call within tool_execution.
Uses pattern-based detection to work with ANY agent format (scalable!).

Supports:
- productivity_agent format: tool_results
- research_agent format: tool_execution_results_history  
- Future agents: Auto-detects tool-like structures
- Custom format: _tools_executed (recommended standard)

Design: Zero decorator changes for new agents - just works!
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ToolCall:
    """Normalized tool call structure (works across all agent formats)"""
    name: str
    parameters: Dict[str, Any]
    result: Any
    error: Any
    status: str  # "success" or "failure"
    batch_key: str = ""


def extract_tools_from_output(output: Dict[str, Any]) -> List[ToolCall]:
    """
    UNIVERSAL tool extractor - works for ANY agent format.
    
    Auto-detects tools by pattern matching. No agent-specific code needed!
    New agents automatically work if they follow common patterns.
    
    Priority Order (v0.5.0 Tool Format Standardization):
    1. _tools_executed (NEW STANDARD - recommended for all agents)
    2. tool_results (productivity_agent - backwards compat)
    3. tool_execution_results_history (research_agent - backwards compat)
    4. Generic fallback (duck typing)
    
    Args:
        output: Observation output dict (any agent)
    
    Returns:
        List of normalized ToolCall objects
    """
    tools = []
    
    # Priority 1: _tools_executed (STANDARD FORMAT - v0.5.0)
    if '_tools_executed' in output:
        tools.extend(_extract_from_tools_executed(output['_tools_executed']))
        logger.debug(f"Extracted {len(tools)} tools from STANDARD format (_tools_executed)")
        return tools  # Stop here if found (highest priority)
    
    # Priority 2: tool_results (productivity_agent format - backwards compat)
    if 'tool_results' in output and isinstance(output['tool_results'], dict):
        tools.extend(_extract_from_tool_results(output['tool_results']))
        logger.debug(f"Extracted {len(tools)} tools from tool_results format (backwards compat)")
        return tools  # Stop here if found
    
    # Priority 3: tool_execution_results_history (research_agent format - backwards compat)
    if 'tool_execution_results_history' in output:
        history = output['tool_execution_results_history']
        tools.extend(_extract_from_execution_history(history))
        logger.debug(f"Extracted {len(tools)} tools from execution_history format (backwards compat)")
        return tools  # Stop here if found
    
    # Priority 4: Generic fallback (scan for tool-like structures)
    for key, value in output.items():
        if 'tool' in key.lower() and isinstance(value, (list, dict)):
            found = _extract_from_generic_structure(value)
            if found:
                tools.extend(found)
                logger.debug(f"Extracted {len(found)} tools from generic pattern: {key}")
    
    return tools


def _extract_from_tool_results(tool_results: dict) -> List[ToolCall]:
    """Extract from productivity_agent format"""
    tools = []
    for batch_key, batch_data in tool_results.items():
        if isinstance(batch_data, dict) and 'results' in batch_data:
            for tool_key, tool_data in batch_data['results'].items():
                tool_name = tool_data.get('tool_name', tool_key.split('_')[0])
                tools.append(ToolCall(
                    name=tool_name,
                    parameters=parse_tool_parameters(tool_key, tool_data),
                    result=tool_data.get('result'),
                    error=tool_data.get('error'),
                    status='failure' if tool_data.get('error') else 'success',
                    batch_key=batch_key
                ))
    return tools


def _extract_from_execution_history(history: Any) -> List[ToolCall]:
    """Extract from research_agent format"""
    tools = []
    
    if not isinstance(history, list):
        return tools
    
    for execution in history:
        if isinstance(execution, dict):
            # Check for results key
            if 'results' in execution:
                results = execution['results']
                batch_key = execution.get('batch_key', 'research')
                
                # Results could be dict or list
                if isinstance(results, dict):
                    for tool_key, tool_data in results.items():
                        tool_name = tool_data.get('tool_name', tool_key.split('_')[0])
                        tools.append(ToolCall(
                            name=tool_name,
                            parameters=tool_data.get('parameters', {}),
                            result=tool_data.get('result'),
                            error=tool_data.get('error'),
                            status=tool_data.get('status', 'success'),
                            batch_key=batch_key
                        ))
                elif isinstance(results, list):
                    for tool_data in results:
                        if isinstance(tool_data, dict):
                            tools.append(ToolCall(
                                name=tool_data.get('tool_name', 'unknown'),
                                parameters=tool_data.get('parameters', {}),
                                result=tool_data.get('result'),
                                error=tool_data.get('error'),
                                status=tool_data.get('status', 'success'),
                                batch_key=batch_key
                            ))
    
    return tools


def _extract_from_tools_executed(tools_data: Any) -> List[ToolCall]:
    """
    Extract from standard format (_tools_executed).
    
    STANDARD FORMAT (v0.5.0):
    [
      {
        "tool_name": str (required),
        "parameters": dict (required, can be empty),
        "result": Any (required, can be None),
        "error": None | dict (required),
        "status": "success" | "failure" (required),
        "batch_key": str (optional),
        "timestamp": str (optional),
        "duration_ms": int (optional),
        "metadata": dict (optional)
      }
    ]
    
    Validation: LENIENT (use defaults for missing required fields)
    """
    tools = []
    
    if not isinstance(tools_data, list):
        logger.warning(f"_tools_executed is not a list: {type(tools_data).__name__}")
        return tools
    
    for idx, tool in enumerate(tools_data):
        if not isinstance(tool, dict):
            logger.warning(f"_tools_executed[{idx}] is not a dict: {type(tool).__name__}")
            continue
        
        # Validate required field: tool_name
        tool_name = tool.get('name') or tool.get('tool_name')
        if not tool_name:
            logger.warning(f"_tools_executed[{idx}] missing tool_name, skipping")
            continue
        
        # Extract with defaults (lenient validation)
        tools.append(ToolCall(
            name=tool_name,
            parameters=tool.get('parameters', {}),
            result=tool.get('result'),
            error=tool.get('error'),
            status=tool.get('status', 'success'),  # Default to success
            batch_key=tool.get('batch_key', '')
        ))
    
    return tools


def _extract_from_generic_structure(data: Any) -> List[ToolCall]:
    """Fallback: Extract from any tool-like structure (duck typing)"""
    tools = []
    
    # List of dicts with tool-like keys
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                # Has tool_name or name? Probably a tool!
                if 'tool_name' in item or 'name' in item:
                    tools.append(ToolCall(
                        name=item.get('tool_name', item.get('name', 'unknown')),
                        parameters=item.get('parameters', item.get('params', {})),
                        result=item.get('result', item.get('output')),
                        error=item.get('error'),
                        status=item.get('status', 'success' if not item.get('error') else 'failure'),
                        batch_key=item.get('batch_key', '')
                    ))
    
    # Nested dict structure
    elif isinstance(data, dict):
        # Check if values are tool-like
        for value in data.values():
            if isinstance(value, (list, dict)):
                tools.extend(_extract_from_generic_structure(value))
    
    return tools


async def create_tool_observations(
    trace_id: str,
    parent_observation_id: str,
    output: Dict[str, Any]
) -> int:
    """
    Create individual TOOL observations from output (ANY format).
    
    UNIVERSAL: Works for productivity_agent, research_agent, and future agents!
    Auto-detects tool calls using pattern matching.
    
    Args:
        trace_id: Trace ID
        parent_observation_id: tool_execution observation ID (parent)
        output: Full observation output (we'll extract tools from it)
    
    Returns:
        Number of tool observations created
    """
    from .redis_publisher import publish_event
    
    # Extract tools using universal detector
    tools = extract_tools_from_output(output)
    
    if not tools:
        logger.debug("No tools found in output (node may not have executed tools)")
        return 0
    
    # Create observations for each tool
    tool_count = 0
    for tool in tools:
        try:
            tool_obs_id = str(uuid.uuid4())
            
            # Create observation start
            await publish_event(
                event_type="observation_start",
                trace_id=trace_id,
                observation_id=tool_obs_id,
                data={
                    "name": tool.name,
                    "type": "TOOL",
                    "parent_observation_id": parent_observation_id,
                    "input": {
                        "tool_name": tool.name,
                        "parameters": tool.parameters,
                        "batch_key": tool.batch_key,
                    },
                    "start_time": datetime.utcnow().isoformat(),
                }
            )
            
            # Create observation end (tool already executed)
            await publish_event(
                event_type="observation_end",
                trace_id=trace_id,
                observation_id=tool_obs_id,
                data={
                    "output": {
                        "status": tool.status,
                        "result": tool.result,
                        "error": tool.error,
                    },
                    "level": "ERROR" if tool.status == "failure" else "DEFAULT",
                    "end_time": datetime.utcnow().isoformat(),
                }
            )
            
            tool_count += 1
            logger.debug(f"Created TOOL observation: {tool.name} (status: {tool.status})")
        
        except Exception as e:
            logger.warning(f"Failed to create observation for tool {tool.name}: {e}")
            # Continue with other tools
    
    if tool_count > 0:
        logger.info(f"Created {tool_count} TOOL observations")
    
    return tool_count


def parse_tool_parameters(tool_key: str, tool_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse tool parameters from tool key and/or tool data.
    
    Tool keys encode parameters: toolname_param1_value1_param2_value2
    Example: office365_search_emails_folder_inbox_filter_receivedDateTime...
    
    Args:
        tool_key: Encoded tool key
        tool_data: Tool data dict (may contain explicit parameters)
    
    Returns:
        Parameters dict
    """
    params = {}
    
    # Check if tool_data has explicit parameters
    if 'parameters' in tool_data and isinstance(tool_data['parameters'], dict):
        params = tool_data['parameters'].copy()
    
    # Try to parse from tool_key (encoded parameters)
    try:
        parts = tool_key.split('_')
        
        # Skip tool name parts (first 1-3 parts depending on tool)
        # Look for key-value pairs in remaining parts
        start_idx = 2  # After tool name
        
        for i in range(start_idx, len(parts), 2):
            if i + 1 < len(parts):
                key = parts[i]
                value = parts[i + 1]
                
                # Only add if looks like a parameter (not part of tool name)
                if key and value and len(key) > 1:
                    # Decode common encodings
                    value = value.replace('ge', '>=').replace('lt', '<').replace('eq', '==')
                    params[key] = value
    
    except Exception as e:
        logger.debug(f"Could not parse parameters from key: {e}")
    
    return params

