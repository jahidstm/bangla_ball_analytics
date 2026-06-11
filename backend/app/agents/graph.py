from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.analyst import analyze_data_node
from app.agents.rag import retrieve_style_node
from app.agents.copywriter import generate_post_node
from app.services.mock_data import MOCK_PLAYERS, MOCK_TEAMS  # Using mock data for now

def fetch_data_node(state: AgentState) -> AgentState:
    print("--- NODE: FETCH DATA ---")
    # If raw_data isn't provided via API, fetch mock data based on topic
    raw_data = state.get("raw_data")
    if not raw_data:
        topic_lower = state.get("topic", "").lower()
        # Player matching
        if "messi" in topic_lower:
            raw_data = MOCK_PLAYERS["messi"]
        elif "ronaldo" in topic_lower:
            raw_data = MOCK_PLAYERS["ronaldo"]
        elif "mbappe" in topic_lower or "mbapp" in topic_lower:
            raw_data = MOCK_PLAYERS["mbappe"]
        # Team matching
        elif "real madrid" in topic_lower or "real" in topic_lower:
            raw_data = MOCK_TEAMS["real_madrid"]
        elif "argentina" in topic_lower:
            raw_data = MOCK_TEAMS["argentina"]
        elif "brazil" in topic_lower or "brasil" in topic_lower:
            raw_data = MOCK_TEAMS["brazil"]
        else:
            # Generic fallback — Groq can still analyze any topic creatively
            raw_data = {
                "topic": state.get("topic", ""),
                "event": "General football tactical analysis request",
                "note": "No specific player/team data found. Analyst should provide general tactical insights based on the topic."
            }
            
    return {
        "raw_data": raw_data,
        "current_step": "fetch_data",
        "error": None
    }

def check_analyst_result(state: AgentState) -> str:
    print("--- CONDITIONAL EDGE: CHECK ANALYST RESULT ---")
    if state.get("error"):
        print("-> FAILED: Retrying Analyst or End")
        # In a real self-healing graph we might loop back to analyst (with a retry count in state)
        # For simplicity, we end if it fails.
        return "end"
    print("-> PASSED: Proceed to RAG")
    return "rag"

# Build the LangGraph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("fetch_data", fetch_data_node)
workflow.add_node("analyst", analyze_data_node)
workflow.add_node("rag_retrieval", retrieve_style_node)
workflow.add_node("copywriter", generate_post_node)

# Add Edges
workflow.set_entry_point("fetch_data")
workflow.add_edge("fetch_data", "analyst")

# Conditional Edge after Analyst
workflow.add_conditional_edges(
    "analyst",
    check_analyst_result,
    {
        "rag": "rag_retrieval",
        "end": END
    }
)

workflow.add_edge("rag_retrieval", "copywriter")
workflow.add_edge("copywriter", END)

# Compile the Graph
app_graph = workflow.compile()
