from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

class PostVariant(BaseModel):
    style: str = Field(description="The style of the post, e.g., Tactical, Emotional, or Engaging")
    content: str = Field(description="The actual content of the post written in Bengali")

class AgentState(TypedDict):
    topic: str
    raw_data: dict               # Mock বা Real API যেখান থেকেই আসুক
    analysis_result: dict        # Groq (Analyst) এর JSON আউটপুট
    style_context: str           # ChromaDB (RAG) থেকে রিট্রিভ করা স্টাইল স্যাম্পল
    bangla_posts: List[PostVariant] # Gemini-এর আউটপুট (Structured for frontend)
    current_step: str
    error: Optional[str]         # গ্রাফ ফেইল করলে ট্র্যাক করার জন্য
