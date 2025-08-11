import asyncio
import sys
from deep_research.orchestration.pipeline import run_research
from dotenv import load_dotenv


load_dotenv(override=True)
async def _amain(topic: str):
    plan, mini_summaries, report = await run_research(topic)
    print("\n# Report\n")
    print(report.markdown_report)

    if getattr(report, "final_citations", None):
        print("\n### Sources\n")
        for i, c in enumerate(report.final_citations, 1):
            title = c.title or c.url
            print(f"{i}. {title} — {c.url}")

def main():
    # 1) If a topic was passed via CLI args, use it
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        # 2) Otherwise, ask the user
        prompt = "Please enter the topic you want to run a deep research on:\n> "
        topic = input(prompt).strip()
        if not topic:
            # optional: fall back to a default if the user just hits Enter
            topic = "Latest AI Agent frameworks in 2025"

    asyncio.run(_amain(topic))

if __name__ == "__main__":
    main()
