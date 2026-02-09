from pydantic import BaseModel, Field

class ContentSummary(BaseModel):
    summary: str = Field(
        description="2–3 line clear summary in simple words"
    )


SUMMARY_SYSTEM_PROMPT = """
You are a summarization agent for notifications.

Your task:
- Read the given content
- Extract only the most important information
- Write a short, clear summary that can be read in under 5 seconds

Rules:
- Use simple, direct language
- Maximum 2–3 short sentences
- Focus on WHAT happened and WHY it matters
- Do not include opinions, speculation, or extra details
- Do not repeat the input text
- Do not add emojis, formatting, or headings
- If the content is unclear or low-value, still summarize but keep it very neutral
- Output must strictly match the required structured format

"""

def build_summary_prompt(item: dict) -> str:
    return f"""
Content:
{item.get("content")}

Summarize this so it can be sent as a notification.
"""


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

summarizer = llm.with_structured_output(ContentSummary)

def generate_summary(item: dict) -> str:

    prompt = build_summary_prompt(item)

    summary = summarizer.invoke(prompt)

    return summary.summary
