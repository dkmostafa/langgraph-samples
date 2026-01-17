from simple_react_pattern.graph_state import GraphState


def should_continue(state: GraphState) -> str:


    if state.user_request_fulfilled:
        return 'end'

    if state.current_step>10:
        return "end"
    else:
        return "act_node"
