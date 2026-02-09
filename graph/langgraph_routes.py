# graph/langgraph_routes.py

def route_after_hard_rules(state):
    """
    Decide next step after hard rules
    """

    if not state.get('passed_items'):
        return 'end'
    return 'vector'

def route_after_llm(state):
    """
    Decide next step after LLM Decision Node
    """

    llm_decision = state.get('llm_decisions', {})

    if not llm_decision:
        return 'end'
    return 'decision'

def route_after_decision(state):
    """
    Decide next step after decision
    """

    if not state.get('notify_items'):
        return 'end'
    if not state.get('archive_items'):
        return 'end'
    return 'notify'
