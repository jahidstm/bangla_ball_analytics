import json
from groq import Groq
from app.agents.state import AgentState, PostVariant
from app.core.config import get_settings

settings = get_settings()

COPYWRITER_SYSTEM_PROMPT = """You are an expert Bengali sports journalist and Facebook content creator.
Your job is to write engaging, viral-worthy Facebook posts in Bengali based on the Analyst's tactical data.

You must write 3 different variations of the post:
1. "Tactical": Focuses deeply on formations, stats, and tactical nuances.
2. "Emotional": Focuses on the passion, the heroics, and the feelings of the fans.
3. "Engaging": A short, punchy post ending with a question to drive comments.

RESPOND ONLY WITH A VALID JSON ARRAY OF OBJECTS. No markdown formatting, no backticks.
Format:
[
  {"style": "Tactical", "content": "আপনার বাংলা পোস্ট..."},
  {"style": "Emotional", "content": "আপনার বাংলা পোস্ট..."},
  {"style": "Engaging", "content": "আপনার বাংলা পোস্ট..."}
]
}
"""

def generate_post_node(state: AgentState) -> AgentState:
    print("--- NODE: COPYWRITER (GROQ FALLBACK) ---")

    client = Groq(api_key=settings.GROQ_API_KEY)

    topic = state.get("topic", "")
    analysis_result = json.dumps(state.get("analysis_result", {}), ensure_ascii=False, indent=2)
    style_context = state.get("style_context", "")

    prompt = f"""{COPYWRITER_SYSTEM_PROMPT}

Style & Tone Guidelines (RAG Context):
{style_context}

Analyst's Data:
{analysis_result}

Topic: {topic}

Write the 3 Facebook post variants in Bengali now:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": COPYWRITER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1024,
        )

        content = response.choices[0].message.content.strip()

        parsed_data = json.loads(content)
        parsed_variants = []
        if isinstance(parsed_data, list):
            parsed_variants = parsed_data
        elif isinstance(parsed_data, dict):
            parsed_variants = parsed_data.get("posts", [])
            if not parsed_variants:
                for v in parsed_data.values():
                    if isinstance(v, list):
                        parsed_variants = v
                        break

        posts = [PostVariant(**v) for v in parsed_variants]

        return {
            "bangla_posts": posts,
            "current_step": "copywriter",
            "error": None
        }

    except Exception as e:
        print(f"Copywriter Error: {e}")
        return {
            "error": f"Copywriter failed: {str(e)}",
            "current_step": "copywriter"
        }
