from graph.logger import logger
from graph.safe_node import safe_node
from graph.state import AGuardState

from database.db import get_connection
from agents.fetch_data import collect_all_data
from agents.preprocessor import preprocessor
from database.repos.content_repo import insert_content
from agents.hard_rules import apply_hard_rules
from database.repos.decision_repo import log_decision
from agents.similarity import get_similarity_scores
from agents.llm_gate import evaluate_content
from memory.vector_repo import upsert_content_embedding
from agents.decision import make_decision
from agents.summary_llm import generate_summary
from notification.dispatcher import dispatch_notification


@safe_node
def fetch_node(state : AGuardState):
    items = collect_all_data(15)
    logger.info(f"Fetched {len(items)} items")
    return {'items': items}

@safe_node
def preprocessor_node(state : AGuardState):
    processed = [preprocessor(item) for item in state['items']]
    logger.info(f"Preprocessed {len(processed)} items")
    return {'preprocessed_items': processed}

@safe_node
def store_node(state : AGuardState):
    stored = []

    conn = get_connection()
    cursor = conn.cursor()
    try:
        for item in state['preprocessed_items']:
            if insert_content(item,cursor):
                stored.append(item)
        conn.commit()
        logger.info(f"Stored {len(stored)} items")
        return {'stored_items': stored}
    except Exception as e:
        logger.info(f"Failed to store item {e}")
        raise ValueError("Failed to store item")
    finally:
        cursor.close()
        conn.close()


@safe_node
def hard_rules_node(state : AGuardState):
    decisions = []
    passed = []

    for item in state['stored_items']:
        decision = apply_hard_rules(item)
        log_decision(decision)
        decisions.append(decision)

        if decision['decision'] == "PASS_TO_LLM":
            passed.append(item)

    logger.info(
        f"Hard rules: {len(passed)} passed / {len(decisions) - len(passed)} dropped"
    )

    return {
        "hard_rules_decision" : decisions,
        "passed_items" : passed
    }

@safe_node
def vector_node(state : AGuardState):
    inserted = 0

    for item in state["passed_items"]:
        upsert_content_embedding(item)
        inserted += 1
        get_similarity_scores(item)

    logger.info(f"Vectorized {inserted} items")


@safe_node
def llm_node(state : AGuardState):
    results = {}

    for item in state["passed_items"]:
        results[item["id"]] = evaluate_content(item)

    llm_passed_items = []
    for cid, decisions in  results.items():
        if decisions['decision'] == "Allowed":
            for item in state["passed_items"]:
                if item["id"] == cid:
                    llm_passed_items.append(item)
                    item["llm_score"] = decisions["relevance_score"]
                    item["reason"] = decisions["reason"]
                    item["confidence"] = decisions["confidence"]

    logger.info(f"LLM passed {len(llm_passed_items)} items")

    return {'llm_gate_items': llm_passed_items, "llm_decisions": results}

'''
hard_rule_score
similarity_score
llm_score
content_id
llm_reason
'''
@safe_node
def decision_node(state : AGuardState):
    decisions = []
    notified_items = []
    archived_items = []
    for item in state["llm_gate_items"]:
        # Calculate avg of top 2 similarity score

        inputs = {
            "content_id": item["id"],
            "similarity_score": item["similarity_score"],
            "llm_reason": item["reason"],
            "hard_rule_score": item["hard_rule_score"],
            "llm_score": item["llm_score"]
            }

        response = make_decision(inputs)
        item["final_score"] = response["final_score"]
        item['decision'] = response["decision"]
        if response["decision"] == "Notify":
            notified_items.append(item)
            item['summary'] = generate_summary(item)
        elif response["decision"] == "Archive":
            archived_items.append(item)
            item['summary'] = generate_summary(item)

        print(
            f"DECISION | {item['id']} | "
            f"rule={item['hard_rule_score']:.2f} | "
            f"vector={item['similarity_score']:.2f} | "
            f"llm={item['llm_score']:.2f} | "
            f"final={item['final_score']:.2f} | "
            f"{item['decision']}"
        )

    logger.info(f"Notify {len(notified_items)} items and archive {len(archived_items)} items")


    return {"notify_items": notified_items, "archive_items": archived_items}

@safe_node
def notification_node(state: AGuardState):
    """
    LangGraph notification node.
    This expresses INTENT, not delivery implementation.
    """

    notify_items = state.get("notify_items", [])
    archive_items = state.get("archive_items", [])
    print("🚀 Entered notification_node")
    print("notify_items:", len(state.get("notify_items", [])))
    print("archive_items:", len(state.get("archive_items", [])))

    if not notify_items and not archive_items:
        print("ℹ️ No items to notify")
        return {}
    for item in notify_items:
        dispatch_notification(item)

    for item in archive_items:
        dispatch_notification(item)
    return state










