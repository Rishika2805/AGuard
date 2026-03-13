from langchain_groq import ChatGroq
from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Literal
from agents.prompting import generate_prompt
import json



class EvaluateResult(BaseModel):
    model_config = ConfigDict(extra="forbid") # to prevent llm from generating extra feilds


    relevance_score : float = Field(ge=0.0,le=1.0,description="Relevance score")
    decision : Literal["Allowed", "Rejected"]
    confidence : Literal["low", "medium", "high"]
    reason: str

    @validator("reason")
    def concise_reason(cls, v):
        if len(v.split()) > 20:
            raise ValueError("Reason must be concise (≤20 words)")
        return v


# Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # good for classification tasks
    temperature=0.0
)

# Structured Output
llm_evaluator = llm.with_structured_output(EvaluateResult)

def evaluate_content(item : dict) -> dict:
    prompt = generate_prompt(item)

    try:
        response = llm_evaluator.invoke(prompt)
        return response.model_dump()
    except Exception as e:
        return {
            "relevance_score": 0.0,
            "decision": "Rejected",
            "confidence": "low",
            "reason": "LLM evaluation failed"
        }
