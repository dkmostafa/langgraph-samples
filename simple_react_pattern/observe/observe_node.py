from simple_react_pattern.graph_state import GraphState


def observe_node(state: GraphState) -> GraphState:

    tool_to_call = state.next_tool_to_use
    if tool_to_call is None or state.last_tool_result is None:
        return state

    context_key = tool_to_call.tool_returned_value
    state.context[context_key] = state.last_tool_result

    state.last_tool_result = None
    state.next_tool_to_use = None

    return state
