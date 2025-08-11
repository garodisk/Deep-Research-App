import asyncio
import os
from markdown_it import MarkdownIt
from deep_research.agents.email_agent import email_agent
from deep_research.orchestration.pipeline import run_research
from agents import Runner
from dotenv import load_dotenv


load_dotenv(override=True)

async def _amain(topic: str):
    _, _, report = await run_research(topic)
    md = MarkdownIt()
    subject = f"Deep Research – {topic}"
    html_body = f"<h2>{subject}</h2><hr>" + md.render(report.markdown_report)

    res = await Runner.run(
        email_agent,
        f"""Send this as an HTML email using your tool.\nsubject: {subject}\nhtml_body:\n<<<HTML\n{html_body}\nHTML"""
    )
    print(res.final_output)

if __name__ == "__main__":
    asyncio.run(_amain("Latest AI Agent frameworks in 2025"))