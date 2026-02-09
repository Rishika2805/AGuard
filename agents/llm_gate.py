from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, validator
from typing import Literal
from agents.cot_prompting import generate_prompt
import json



class EvaluateResult(BaseModel):
    relevance_score : float = Field(ge=0.0,le=1.0,description="Relevance score")
    decision : Literal["Allowed", "Rejected"]
    confidence : Literal["low", "medium", "high"]
    reason: str

    @validator("reason")
    def concise_reason(cls, v):
        if len(v.split()) > 20:
            raise ValueError("Reason must be concise (≤20 words)")
        return v

    # @validator("decision")
    # def decision_validator(cls, v,values):
    #     score = values.get("relevance_score",0)
    #
    #     if v == "Allowed" and score <= 0.4:
    #         raise ValueError("Allowed content must have relevance_score > 0.2")
    #     return v


llm = ChatOpenAI(
    model = "gpt-4o",
    temperature=0.0
)

llm_evaluator = llm.with_structured_output(EvaluateResult)

def evaluate_content(item : dict) -> dict:
    prompt = generate_prompt(item)

    response = llm_evaluator.invoke(prompt)

    return response.model_dump()
