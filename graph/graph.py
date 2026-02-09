from langgraph.graph import StateGraph, END

from graph.state import AGuardState
from graph.nodes import (
    fetch_node,
    preprocessor_node,
    store_node,
    hard_rules_node,
    vector_node,
    llm_node,
    decision_node
)
from graph.langgraph_routes import route_after_hard_rules, route_after_llm, route_after_decision


def build_graph():
    graph = StateGraph(AGuardState)

    # add nodes

    graph.add_node("fetch_and_parse", fetch_node)
    graph.add_node("preprocessor", preprocessor_node)
    graph.add_node("store", store_node)
    graph.add_node("hard_rules", hard_rules_node)
    graph.add_node("vector", vector_node)
    graph.add_node("llm", llm_node)
    graph.add_node("decision", decision_node)

    # linear edges
    graph.set_entry_point("fetch_and_parse")
    graph.add_edge("fetch_and_parse", "preprocessor")
    graph.add_edge("preprocessor", "store")
    graph.add_edge('store', "hard_rules")

    # Branch after hard rules
    graph.add_conditional_edges(
        "hard_rules",
        route_after_hard_rules,
        {
            "vector" : "vector",
            "end" : END
        }
    )

    graph.add_edge("vector", "llm")

    # Branch after llm_node
    graph.add_conditional_edges(
        "llm",
        route_after_llm,
        {
            "decision" : "decision",
            "end" : END
        }
    )

    # Branch after decision_node

    graph.add_conditional_edges(
        "decision",
        route_after_decision,
        {
            "notify" : END,
            "end" : END
        }
    )

    return graph.compile()