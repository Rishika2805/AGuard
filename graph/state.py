# graph/state.py

from typing import TypedDict, List, Dict, Any


class AGuardState(TypedDict, total=False):
    items : List[Dict[str, Any]]

    preprocessed_items : List[Dict[str, Any]]

    stored_items : List[Dict[str, Any]]

    hard_rules_decision: List[Dict[str, Any]]

    passed_items: List[Dict[str, Any]]

    llm_decisions : Dict[str, Dict[str, Any]]

    llm_gate_items: List[Dict[str, Any]]

    final_decision : List[Dict[str, Any]]

    notify_items : List[Dict[str, Any]]

    archive_items : List[Dict[str, Any]]
