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

    notify_items = state.get("notify_items", [])
    archive_items = state.get("archive_items", [])

    if notify_items or archive_items:
        return "notify"

    return "end"
