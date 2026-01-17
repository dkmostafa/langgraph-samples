from typing import Iterable

from langchain_core.tools import StructuredTool

from simple_react_pattern.graph_state import GraphState
from simple_react_pattern.reason.reason_states import ToolToCall


def act_node(state: GraphState, tools: list[StructuredTool]) -> GraphState:
    tool_to_call = state.next_tool_to_use
    if tool_to_call is None:
        return state  # nothing to do

    tool_to_call_args = tool_to_call.arguments
    tool_to_use = _get_tool_if_exists(tool_to_call, tools)

    if tool_to_use is None:
        state.context["_last_tool_error"] = f"No tool found for {tool_to_call.tool_name}"
        state.last_tool_result = None
        state.next_tool_to_use = None
        return state

    result = tool_to_use.invoke(tool_to_call_args)

    state.last_tool_result = result

    return state


def _get_tool_if_exists(
    tool_to_call: ToolToCall | None,
    tools: Iterable[StructuredTool],
) -> StructuredTool | None:
    if not tool_to_call or not hasattr(tool_to_call, "tool_name"):
        return None

    for tool in tools:
        if tool.name == tool_to_call.tool_name:
            return tool

    return None