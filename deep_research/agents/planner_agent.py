from agents import Agent
from deep_research.config import HOW_MANY_SEARCHES
from deep_research.models import WebSearchPlan, WebSearchItem

INSTRUCTIONS = (
    "You are a helpful research assistant. Given a query, propose web searches "
    f"to answer it best. Output {HOW_MANY_SEARCHES} focused queries with reasons."
)

planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)