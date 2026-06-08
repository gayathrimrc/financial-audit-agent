from langgraph.graph import StateGraph, END
from .schema import AuditState
from .nodes import generate_sql_node, execute_query_node, analyze_results_node

def route_engine(state: AuditState) -> str:
    """Evaluates if the agent needs to re-try SQL writing or move to analysis."""
    if state.get("error_log"):
        return "fix_sql"
    return "analyze"

# Construct the Graph Workflow
workflow = StateGraph(AuditState)

# Define Nodes
workflow.add_node("write_sql", generate_sql_node)
workflow.add_node("run_sql", execute_query_node)
workflow.add_node("analyze_results", analyze_results_node)

# Map Edges
workflow.set_entry_point("write_sql")
workflow.add_edge("write_sql", "run_sql")

# Add conditional routing based on execution success
workflow.add_conditional_edges(
    "run_sql",
    route_engine,
    {
        "fix_sql": "write_sql",
        "analyze": "analyze_results"
    }
)

workflow.add_edge("analyze_results", END)

# Compile Application Graph
agent_app = workflow.compile()

if __name__ == "__main__":
    # Test execution block
    initial_input = {
        "user_prompt": "Find all accounts in Q1 that had a transaction amount above 10,000 and flag their merchant categories."
    }
    
    print("🚀 Initializing Autonomous Financial Audit Agent...")
    output = agent_app.invoke(initial_input)
    
    print("\n📋 Final Audit Output:")
    print(output["final_report"].model_dump_json(indent=2))
