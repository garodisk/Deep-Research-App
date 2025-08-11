import os
from datetime import datetime
from typing import List, Tuple

from deep_research.orchestration.pipeline import run_research
from deep_research.utils.tls import apply_certifi_env

apply_certifi_env()

import gradio as gr
from dotenv import load_dotenv


load_dotenv(override=True)

def _plan_to_rows(plan) -> List[list]:
    rows: List[list] = []
    try:
        for i, it in enumerate(plan.searches, 1):
            rows.append([i, getattr(it, "query", ""), getattr(it, "reason", "")])
    except Exception:
        pass
    return rows

def _citations_to_md(report) -> str:
    if not getattr(report, "final_citations", None):
        return ""
    lines = ["\n### Sources\n"]
    for idx, c in enumerate(report.final_citations, 1):
        title = getattr(c, "title", None) or "Source"
        url = getattr(c, "url", "")
        lines.append(f"{idx}. [{title}]({url})" if url else f"{idx}. {title}")
    return "\n".join(lines)

async def stream_research(chat_history: List[Tuple[str, str]], topic: str, progress=gr.Progress(track_tqdm=False)):
    history = list(chat_history or [])
    history.append((topic, "Starting deep research..."))
    yield history, [], "", "", "", None

    progress(0.05, desc="Planning searches…")
    history[-1] = (topic, "Planning searches…")
    yield history, [], "", "", "", None

    progress(0.12, desc="Running pipeline… (this may take a bit)")
    plan, mini_summaries, report = await run_research(topic)

    progress(0.55, desc="Formatting results…")
    plan_rows = _plan_to_rows(plan)
    history[-1] = (topic, "Searches planned. Gathering and synthesizing…")
    yield history, plan_rows, "", "", "", None

    if mini_summaries:
        parts = ["## Mini-summaries"]
        for i, s in enumerate(mini_summaries, 1):
            parts.append(f"<details><summary><b>Summary {i}</b></summary>\n\n{s}\n\n</details>")
        mini_md = "\n\n".join(parts)
    else:
        mini_md = "(No mini-summaries produced)"

    yield history, plan_rows, mini_md, "", "", None

    report_md = getattr(report, "markdown_report", "")
    sources_md = _citations_to_md(report)

    full_md = report_md + ("\n\n" + sources_md if sources_md else "")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = os.path.join(".", f"deep_research_{ts}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_md)

    history[-1] = (topic, "Done ✅")
    progress(1.0, desc="Complete")
    yield history, plan_rows, mini_md, report_md, sources_md, file_path

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔎 Deep Research (Gradio)
    Enter a topic and I'll plan searches, gather snippets, and synthesize a long-form report.
    """)

    with gr.Row():
        chatbot = gr.Chatbot(label="Research Chat", height=350, type="tuples")

    with gr.Row():
        topic = gr.Textbox(placeholder="e.g., Latest AI Agent frameworks in 2025", label="Topic", lines=1)
        go = gr.Button("Run Research", variant="primary")

    with gr.Row():
        plan_table = gr.Dataframe(headers=["#", "query", "reason"], label="Planned web searches", interactive=False)

    mini_md = gr.Markdown(label="Mini-summaries")
    report_md = gr.Markdown(label="Synthesis report (Markdown)")
    sources_md = gr.Markdown(label="Sources")

    with gr.Row():
        dl = gr.DownloadButton(label="Download Markdown", value=None)

    state = gr.State([])

    go.click(
        fn=stream_research,
        inputs=[state, topic],
        outputs=[chatbot, plan_table, mini_md, report_md, sources_md, dl],
        show_progress=True,
    ).then(lambda h: h, inputs=chatbot, outputs=state)

    gr.Examples([
        ["Latest AI Agent frameworks in 2025"],
        ["State of multimodal RAG for e-commerce"],
        ["Carbon accounting tools for utilities in 2025"],
    ], inputs=[topic])

if __name__ == "__main__":
    # Auto-pick a free port locally
    demo.launch(server_name="127.0.0.1", server_port=None, share=True)