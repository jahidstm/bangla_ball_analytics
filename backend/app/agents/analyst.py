import json
from groq import Groq
from app.agents.state import AgentState
from app.core.config import get_settings

settings = get_settings()

# System prompt for the Data Analyst
ANALYST_PROMPT = """You are a world-class football tactical data analyst.
Your job is to analyze raw football data and extract the most interesting tactical insights, key player stats, and momentum shifts.

You must ALWAYS respond with ONLY valid JSON in the following format. Do not add any markdown formatting, backticks, or explanatory text. Just the raw JSON object.
{
  "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
  "tactical_analysis": "A brief paragraph explaining the tactics.",
  "standout_players": [{"name": "Player Name", "reason": "Why they stood out"}]
}
"""

def analyze_data_node(state: AgentState) -> AgentState:
    print("--- NODE: ANALYST (GROQ) ---")

    client = Groq(api_key=settings.GROQ_API_KEY)

    try:
        raw_data_str = json.dumps(state.get("raw_data", {}), indent=2)
        topic = state.get("topic", "General Analysis")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": ANALYST_PROMPT},
                {"role": "user", "content": f"Topic: {topic}\n\nRaw Data:\n{raw_data_str}"}
            ],
            temperature=0.2,
            max_tokens=1024,
        )

        content = response.choices[0].message.content.strip()
        # Remove markdown code blocks if model adds them despite instructions
        if content.startswith("```json"):
            content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
        elif content.startswith("```"):
            content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        parsed_result = json.loads(content)

        return {
            "analysis_result": parsed_result,
            "current_step": "analyst",
            "error": None
        }

    except Exception as e:
        print(f"Analyst Error: {e}")
        return {
            "error": f"Analyst failed: {str(e)}",
            "current_step": "analyst"
        }
