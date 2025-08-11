import asyncio
from typing import List, Tuple
from agents import Runner, trace

from deep_research.models import WebSearchPlan, WebSearchItem, ReportData
from deep_research.agents.planner_agent import planner_agent
from deep_research.agents.search_agent import search_agent
from deep_research.agents.writer_agent import writer_agent
from deep_research.utils.logging import info, step, doing, BOLD, DIM, RESET

async def plan_searches(query: str) -> WebSearchPlan:
    result = await Runner.run(planner_agent, f"Query: {query}")
    plan: WebSearchPlan = result.final_output
    info("Planned search phrases:")
    for i, it in enumerate(plan.searches, 1):
        print(f"  {i}. {BOLD}{it.query}{RESET} {DIM}— {it.reason}{RESET}")
    return plan

async def search_one(item: WebSearchItem) -> str:
    doing(f"Searching: {item.query}")
    input_msg = f"Search term: {item.query}\nReason: {item.reason}"
    result = await Runner.run(search_agent, input_msg, max_turns=4)
    step(f"Done: {item.query}")
    return result.final_output

async def perform_searches(plan: WebSearchPlan) -> List[str]:
    tasks = [asyncio.create_task(search_one(it)) for it in plan.searches]
    return await asyncio.gather(*tasks)

def build_writer_input(original_query: str, mini_summaries: List[str]) -> str:
    blocks: List[str] = []
    blocks.append(f"Original query:\n{original_query}\n")
    blocks.append("=== MINI-SUMMARIES START ===")
    for i, s in enumerate(mini_summaries, 1):
        blocks.append(f"\n--- Summary {i} ---\n{s}\n")
    blocks.append("=== MINI-SUMMARIES END ===\n")
    return "\n".join(blocks)

async def write_report(original_query: str, mini_summaries: List[str]) -> ReportData:
    payload = build_writer_input(original_query, mini_summaries)
    result = await Runner.run(writer_agent, payload, max_turns=4)
    return result.final_output

async def run_research(query: str):
    with trace("Deep Research (DDG)"):
        print("Planning...")
        plan = await plan_searches(query)
        print("Searching...")
        mini_summaries = await perform_searches(plan)
        print("Synthesizing...")
        report = await write_report(query, mini_summaries)
        return plan, mini_summaries, report