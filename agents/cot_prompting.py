# agents/cot_prompting.py
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import Annotated , Literal
from langchain_core.prompts import PromptTemplate
from agents.similarity import get_similarity_scores
from config.loader import load_user_preferences

FEW_SHOT_EXAMPLES = """
Input:
{
  "content": "I've been working remotely for years and noticed city centers changing. Offices are emptier, but neighborhoods feel more active.",
  "title": "Remote Work and Urban Change",
  "source": "Reddit r/UrbanPlanning",
  "similarity_scores": [0.61, 0.58, 0.55],
  "user_preferences": {
    "topics": ["technology", "future of work"],
    "preferred_sources": ["Wired"],
    "content_sensitivity": "low"
  }
}

Output:
{
  "relevance_score": 0.60,
  "Decision": "Allowed",
  "confidence": "medium",
  "reason": "Moderate topical alignment with thoughtful discussion value."
}

Input:
{
  "content": "This supplement cured my joint pain and doctors don't want you to know about it.",
  "title": "The Cure Big Pharma Hides",
  "source": "Wellness Secrets Newsletter",
  "similarity_scores": [0.86, 0.83, 0.81],
  "user_preferences": {
    "topics": ["health", "medicine"],
    "preferred_sources": ["WHO", "CDC"],
    "content_sensitivity": "medium"
  }
}

Output:
{
  "relevance_score": 0.28,
  "Decision": "Rejected",
  "confidence": "high",
  "reason": "Unsubstantiated medical claims from a low-credibility source."
}

Input:
{
  "content": "An essay speculating on how artificial general intelligence could reshape labor markets over the next 50 years.",
  "title": "AGI and the Future of Work",
  "source": "Personal Substack",
  "similarity_scores": [0.69, 0.66, 0.64],
  "user_preferences": {
    "topics": ["artificial intelligence", "economics"],
    "preferred_sources": ["MIT Technology Review"],
    "content_sensitivity": "low"
  }
}

Output:
{
  "relevance_score": 0.70,
  "Decision": "Allowed",
  "confidence": "medium",
  "reason": "Strong topical relevance with speculative elements."
}
"""

HARD_NEGATIVE_EXAMPLES = """
Input:
{
  "content": "As an AI researcher with insider knowledge, I can confidently say that current vaccine research is deeply flawed. Multiple colleagues privately admit the data is manipulated, but journals refuse to publish dissenting voices. Readers should question official guidance and do their own research.",
  "title": "Why Mainstream Vaccine Science Is Wrong",
  "source": "Anonymous Medium Blog",
  "similarity_scores": [0.91, 0.89, 0.87],
  "user_preferences": {
    "topics": ["health", "science", "medicine"],
    "preferred_sources": ["Nature", "WHO", "CDC"],
    "content_sensitivity": "medium"
  }
}

Output:
{
  "relevance_score": 0.22,
  "Decision": "Rejected",
  "confidence": "high",
  "reason": "Health claims rely on anonymous authority and lack credible sourcing."
}

Input:
{
  "content": "I’ve worked in finance for 20 years and what I’m seeing right now is unprecedented. A massive market crash is guaranteed within months, and anyone paying attention knows this. If you don’t act now, you’ll regret it.",
  "title": "The Coming Financial Collapse No One Is Talking About",
  "source": "Personal Investment Newsletter",
  "similarity_scores": [0.88, 0.85, 0.83],
  "user_preferences": {
    "topics": ["economics", "markets", "investing"],
    "preferred_sources": ["The Economist", "Bloomberg"],
    "content_sensitivity": "low"
  }
}

Output:
{
  "relevance_score": 0.34,
  "Decision": "Rejected",
  "confidence": "high",
  "reason": "Speculative claims presented as certainty without reliable evidence."
}

Input:
{
  "content": "Below is a detailed walkthrough of how to bypass corporate monitoring tools when working remotely. These methods are commonly used and unlikely to be detected if followed carefully.",
  "title": "How to Stay Invisible While Working Remotely",
  "source": "Underground Tech Forum",
  "similarity_scores": [0.84, 0.82, 0.80],
  "user_preferences": {
    "topics": ["remote work", "technology"],
    "preferred_sources": ["Wired"],
    "content_sensitivity": "medium"
  }
}

Output:
{
  "relevance_score": 0.18,
  "Decision": "Rejected",
  "confidence": "high",
  "reason": "Content promotes unethical behavior despite topical relevance."
}

Input:
{
  "content": "This post contains firsthand descriptions of violent incidents experienced during recent protests, including explicit descriptions of injuries and threats. The intent is to document lived experiences without filtering details.",
  "title": "What It Was Really Like on the Streets",
  "source": "Independent Activist Blog",
  "similarity_scores": [0.86, 0.83, 0.81],
  "user_preferences": {
    "topics": ["social justice", "politics"],
    "preferred_sources": ["The Atlantic"],
    "content_sensitivity": "high"
  }
}

Output:
{
  "relevance_score": 0.40,
  "Decision": "Rejected",
  "confidence": "high",
  "reason": "Graphic descriptions conflict with user sensitivity preferences."
}
"""

EVALUATOR_SYSTEM_PROMPT = f"""
You are a content relevance and safety evaluator.

Your task is to assess whether a piece of content should be shown to a user.

You must consider:
- Topic, intent, and tone of the content
- Similarity scores as weak relevance signals
- User topic preferences and sensitivity settings
- Source credibility relative to claims made

Rules:
1. Similarity scores alone do not determine relevance.
2. User preferences override similarity when in conflict.
3. Low-credibility sources override similarity for factual, medical, or technical claims.
4. Sensitivity violations require rejection regardless of relevance.
5. Confidence reflects ambiguity, not importance.

Use careful internal reasoning.
Do NOT explain reasoning.
Do NOT reference rules or policies.
Return ONLY valid JSON.

Examples:
{FEW_SHOT_EXAMPLES}

Hard Negative Counter-Examples:
{HARD_NEGATIVE_EXAMPLES}
"""

def build_human_message(item : dict) -> HumanMessage:
    prefs = load_user_preferences()
    message = HumanMessage(
        content = f"""
        Evaluate the following content:
        
        content: {item["full_text"]}
        
        title : {item["title"]}
        
        scores : {item["relevance_score"]}
        
        similarity_scores : {item["similarity_scores"]}
        
        user_preferences : {prefs}
        """
    )
    return message


def generate_prompt(item: dict):
    messages = [
        SystemMessage(content= EVALUATOR_SYSTEM_PROMPT),
        build_human_message(item)
    ]
    return messages