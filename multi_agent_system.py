import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Load environment variables from .env file automatically
load_dotenv()

# Import LangChain models and prompt tools
# Note: Ensure you have `langchain-google-genai` and `langgraph` installed:
# pip install langchain-google-genai langgraph langchain-core
from langchain_core.messages import HumanMessage, SystemMessage

# ------------------------------------------------------------------------------
# 1. LLM SETUP
# ------------------------------------------------------------------------------
# Initialize the language model.
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(
    model="qwen2.5:0.5b",
    temperature=0.7
)
# ------------------------------------------------------------------------------
# 2. STATE DEFINITION
# ------------------------------------------------------------------------------
# The shared state dictionary passed around the agents. Langgraph merges the 
# returned dictionary from each node into this global state.
class AgentState(TypedDict):
    user_request: str
    destinations: str
    itinerary: str
    final_plan: str

# ------------------------------------------------------------------------------
# 3. AGENT DEFINITIONS (NODES)
# ------------------------------------------------------------------------------

# Agent 1: Destination Expert
# Suggests places to visit based on user constraints.
def destination_expert(state: AgentState) -> dict:
    print("✈️  [Agent 1: Destination Expert] Researching best spots...")
    user_request = state["user_request"]
    
    messages = [
        SystemMessage(content="You are a seasoned travel expert. Given a user's travel request, suggest 3 amazing destinations/spots. Keep it concise."),
        HumanMessage(content=user_request)
    ]
    
    response = llm.invoke(messages)
    return {"destinations": response.content}

# Agent 2: Itinerary Planner
# Creates a daily schedule.
def itinerary_planner(state: AgentState) -> dict:
    print("📅 [Agent 2: Itinerary Planner] Building day-to-day schedule...")
    destinations = state["destinations"]
    user_request = state["user_request"]
    
    messages = [
        SystemMessage(content="You are an expert trip planner. Create a high-level daily itinerary based on the initial request and suggested spots."),
        HumanMessage(content=f"User Request: {user_request}\nSuggested Spots: {destinations}")
    ]
    
    response = llm.invoke(messages)
    return {"itinerary": response.content}

# Agent 3: Budget & Tips Analyzer
# Calculates rough costs and adds helpful tips.
def budget_analyzer(state: AgentState) -> dict:
    print("💰 [Agent 3: Budget Analyzer] Estimating costs and finalizing tips...")
    itinerary = state["itinerary"]
    
    messages = [
        SystemMessage(content="You are a budget travel advisor. Review the itinerary and provide a rough cost estimate and 3 practical travel tips. Merge the itinerary and your notes into one final clean output."),
        HumanMessage(content=f"Itinerary:\n{itinerary}")
    ]
    
    response = llm.invoke(messages)
    return {"final_plan": response.content}

# ------------------------------------------------------------------------------
# 4. LANGGRAPH WORKFLOW CONSTRUCTION
# ------------------------------------------------------------------------------
def build_graph():
    # Initialize a state graph pointing to our TypedDict
    workflow = StateGraph(AgentState)
    
    # Add nodes (our agents)
    workflow.add_node("destination_expert", destination_expert)
    workflow.add_node("itinerary_planner", itinerary_planner)
    workflow.add_node("budget_analyzer", budget_analyzer)
    
    # Define edges (how data flows conditional routing could go here but we use linear flow for simplicity)
    workflow.set_entry_point("destination_expert")
    workflow.add_edge("destination_expert", "itinerary_planner")
    workflow.add_edge("itinerary_planner", "budget_analyzer")
    workflow.add_edge("budget_analyzer", END)
    
    # Compile into an executable LangChain Runnable
    return workflow.compile()

# ------------------------------------------------------------------------------
# 5. MAIN FUNCTION & CLI EXECUTION
# ------------------------------------------------------------------------------
def main():
    print("=" * 60)
    print(" 🌍 Welcome to the AI Travel Planner Multi-Agent System! 🌍")
    print("=" * 60)
    
    # Accept dynamic user input
    user_input = input("\nTell us about your dream trip (e.g., 'A 3-day relaxing beach trip in Spain'):\n> ")
    
    if not user_input.strip():
        print("Input cannot be empty. See you next time!")
        return

    # Build the system
    app = build_graph()
    
    # Initial state seeding
    initial_state = AgentState(
        user_request=user_input.strip(),
        destinations="",
        itinerary="",
        final_plan=""
    )
    
    print("\n--- Starting Agent Execution Workflow ---\n")
    
    # Execute the graph
    final_output = app.invoke(initial_state)
    
    # Display results
    print("\n" + "=" * 60)
    print(" 🎉 YOUR FINAL TRAVEL PLAN 🎉")
    print("=" * 60)
    print(final_output["final_plan"])
    print("=" * 60)

if __name__ == "__main__":
    main()
