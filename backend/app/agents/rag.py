import os
from app.agents.state import AgentState
from app.core.config import get_settings

settings = get_settings()

# A sample high-quality Bangla Sports writing style reference (Pavilion/Sports Analyst BD style)
MOCK_STYLE_CONTEXT = """
Style Reference (Tactical & Emotional Bangla):
"মাঠে যখন তিনি নামেন, তখন পুরো গ্যালারি নিস্তব্ধ হয়ে যায়! বল পায়ে তার প্রতিটি মুভমেন্ট যেন এক একটা শিল্পের ছোঁয়া। ট্যাকটিক্যালি দেখলে, আজকের ম্যাচে সে মূলত 'ফলস নাইন' হিসেবে খেলেছে, ডিফেন্ডারদের লাইন ব্রেক করে বারবার হাফ-স্পেসে ঢুকে পড়েছে। তার এই প্রেসিং এবং ভিশনই আজকে ম্যাচের পার্থক্য গড়ে দিয়েছে।"

Instruction for Copywriter:
- Use sophisticated but easy to read Bengali (প্রমিত বাংলা).
- Use football terminologies naturally (e.g., হাফ-স্পেস, প্রেসিং, ফলস নাইন, কাউন্টার অ্যাটাক).
- Mix emotion with tactical depth.
"""

def retrieve_style_node(state: AgentState) -> AgentState:
    print("--- NODE: RAG RETRIEVAL ---")
    
    # In Phase 4, we will fetch this from ChromaDB based on state["topic"]
    # For now, we inject a highly effective base style to fix the 'Generic Voice' blind spot.
    retrieved_style = MOCK_STYLE_CONTEXT
    
    return {
        "style_context": retrieved_style,
        "current_step": "rag_retrieval",
        "error": None
    }
