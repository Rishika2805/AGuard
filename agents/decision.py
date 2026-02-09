from pydantic import BaseModel, Field
from typing import Literal


class FinalDecision(BaseModel):
    content_id: str

    decision : Literal["Notify", "Ignore", "Archive"]

    final_score: float = Field(ge=0.0,le=1.0)

    reason : str

    confidence : Literal['low','medium','high']


def make_decision(inputs: dict) -> dict:
    rule_score = inputs["hard_rule_score"]
    similarity_score = inputs["similarity_score"]
    llm_score = inputs["llm_score"]

    # 🔑 rebalance weights (LLM rescues)
    final_score = round(
        0.25 * rule_score +
        0.25 * similarity_score +
        0.50 * llm_score,
        3
    )

    # ---------- DECISION BANDS ----------
    if final_score >= 0.5:
        decision = "Notify"
        confidence = "high"
    elif final_score >= 0.35:
        decision = "Archive"   # 🔥 MORE ARCHIVE, LESS IGNORE
        confidence = "medium"
    else:
        decision = "Ignore"
        confidence = "low"

    return dict(
        content_id=inputs["content_id"],
        decision=decision,
        final_score=final_score,
        reason=inputs.get("llm_reason", "Aggregated decision"),
        confidence=confidence,
    )
