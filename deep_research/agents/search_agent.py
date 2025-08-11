from agents import Agent, ModelSettings
from deep_research.tools.ddg_tool import ddg_search
from deep_research.utils.tls import apply_certifi_env

apply_certifi_env()

import gradio as gr

SEARCH_INSTRUCTIONS = (
    "You are a research assistant. Given a search term, call `ddg_search` exactly once to fetch results, "
    "then produce an elaborate 4-5 paragraph summary (>=1000 words). Use only titles and snippets; do not browse further.\n\n"
    "After the summary, add a 'Sources' section listing 2–4 relevant items as:\n"
    "[1] Title — URL\n[2] Title — URL\n"
)

search_agent = Agent(
    name="Search agent (DuckDuckGo)",
    instructions=SEARCH_INSTRUCTIONS,
    tools=[ddg_search],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)