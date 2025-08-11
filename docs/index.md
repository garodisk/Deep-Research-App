<!-- Personal hero -->
<div align="center" style="margin: 0 0 1.25rem 0;">
  <h1 style="margin-bottom: .25rem;">👋 Hi, I’m <span style="white-space:nowrap;">Saket Garodia</span></h1>
  <p style="max-width: 720px;">
    I’m passionate about building AI apps, agentic workflows, and everything AI — from search & synthesis
    pipelines to production-ready LLM tooling.
  </p>
  <p>
    <a class="btn" href="https://www.linkedin.com/in/saket-garodia/" target="_blank" rel="noopener">Connect on LinkedIn</a>
    <a class="btn" href="https://github.com/garodisk/Deep-Research-App" target="_blank" rel="noopener">View this project</a>
  </p>
</div>

---

## About me
I love shipping real AI products: agentic systems, LLMs and AI apps.


## Overview - Deep Research (DDG‑Powered Agentic Pipeline)

A small but complete **agentic research pipeline** that:

- illustrates how thinking models work (eg. o3, deep research etc)
- plans focused web searches,
- gathers high‑signal snippets via **DuckDuckGo** (ddgs),
- synthesizes a long‑form **Markdown report** with inline citations,
- (optionally) emails the report via **SendGrid**,
- and ships with a clean **Gradio UI**.

---

## ✨ Features

- **PlannerAgent** → generates 3 targeted search phrases with reasons
- **Search agent** → calls `ddg_search` once per phrase, writes mini‑summaries + Sources
- **WriterAgent** → produces a structured report (exec summary, outline, body, follow‑ups, citations)
- **Email agent (optional)** → sends HTML email via SendGrid
- **Gradio app** → streaming progress, mini‑summaries, report view, and Markdown download

---

## 🧱 Project structure

```
deep-research/
├─ pyproject.toml
├─ requirements.txt
├─ .env.example
├─ README.md
├─ scripts/
│  ├─ run_research.py          # CLI entry: run the pipeline from terminal
│  └─ send_email_test.py       # Example: run pipeline + email report
└─ deep_research/
   ├─ __init__.py              # Package API (re‑exports common objects)
   ├─ config.py                # Constants (e.g., HOW_MANY_SEARCHES)
   ├─ models.py                # Pydantic models (WebSearchPlan, ReportData, ...)
   ├─ utils/
   │  ├─ __init__.py
   │  ├─ logging.py            # pretty console logging helpers
   │  └─ tls.py                # certifi CA env helper (fixes TLS in some envs)
   ├─ tools/
   │  ├─ __init__.py
   │  └─ ddg_tool.py           # DuckDuckGo search tool (ddgs)
   ├─ agents/
   │  ├─ __init__.py
   │  ├─ planner_agent.py
   │  ├─ search_agent.py
   │  ├─ writer_agent.py
   │  └─ email_agent.py
   ├─ orchestration/
   │  ├─ __init__.py
   │  └─ pipeline.py           # plan → search → synthesize orchestration
   └─ ui/
      ├─ __init__.py
      └─ gradio_app.py         # Gradio Blocks app
```

---

## ⚙️ Requirements

- Python **3.10+**
- Internet access for searches and (optionally) SendGrid

Install deps:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# also install your custom `agents` SDK if it isn't on PyPI
```

Copy the env template and fill values:

```bash
cp .env.example .env
```

`.env` values:

- `SENDGRID_API_KEY` – required only if you use the email step
- `EMAIL_FROM` – a **verified** sender (Single Sender or domain‑authenticated)
- `EMAIL_TO` – your recipient address
- 'OPENAI_API_KEY' - 'sk-...'

> Behind corporate proxies/Windows, TLS may fail. See **Troubleshooting → TLS/CA**.

---

## 🚀 Quickstart

Run the pipeline from the command line:

```bash
python -m scripts.run_research "Latest AI Agent frameworks in 2025"
# or run without args and you’ll be prompted to enter a topic interactively
python -m scripts.run_research
```

Launch the Gradio app:

```bash
python -m deep_research.ui.gradio_app
```

Then open the printed local URL. Type a topic → **Run Research**.

Send the report by email (example script):

```bash
python -m scripts.send_email_test
```

---

## 🧠 How it works

1. **PlannerAgent** builds a `WebSearchPlan` (3 queries + reasons).
2. **Search agent** runs each query with the `ddg_search` tool (DuckDuckGo via ddgs) and produces mini‑summaries + sources.
3. **WriterAgent** synthesizes a long Markdown report with inline `[n]` citations and an ordered `final_citations` list.
4. **Gradio** streams progress and writes a timestamped `.md` for download.
5. **Email agent (optional)** sends a nicely formatted HTML email.

**Concurrency**: all searches run in parallel with `asyncio` for speed.

**Typed outputs**: Pydantic models (`WebSearchPlan`, `ReportData`) keep boundaries clean and predictable.

---

## 📦 Packages & modules (what each does)

- ``: shared data contracts (Pydantic) used across agents and orchestration.
- ``: `ddg_search` wraps ddgs to return `{title,url,snippet}` dicts.
- ``: preconfigured agents (planner, search, writer, email). Search agent is forced to call the tool exactly once.
- ``: glue code: `plan_searches` → `perform_searches` → `write_report` → `run_research`.
- ``: UI wiring; async generator yields partial updates to the interface.
- ``: sets `SSL_CERT_FILE` to `certifi` CA bundle if needed.

**About **``** files**: they mark directories as Python packages and *optionally* re‑export a clean public API so you can write:

```python
from deep_research import run_research, ReportData
from deep_research.agents import planner_agent
```

Instead of longer nested imports.

---

## ✉️ Emailing the report (SendGrid)

1. Verify `EMAIL_FROM` in SendGrid (Single Sender or domain authentication).
2. Set `SENDGRID_API_KEY`, `EMAIL_FROM`, `EMAIL_TO` in `.env`.
3. Run the email example:

```bash
python -m scripts.send_email_test
```

If you get **202 Accepted** but no mail, check SendGrid **Email Activity** and **Suppressions** (bounces/blocks), or Gmail’s Spam/Promotions.

---

## 🧰 Troubleshooting

**TLS/CA on Windows/corp proxy**

- If HTTPS fails with `CERTIFICATE_VERIFY_FAILED`, ensure a CA bundle is set:

```bash
python -c "import certifi, os; print(certifi.where())"
# then set SSL_CERT_FILE to that path
```

The Gradio app calls `apply_certifi_env()` automatically.

**Port already in use**

- Change `demo.launch(..., server_port=None)` or run:

```python
import gradio as gr; gr.close_all()
```

**SendGrid 403 Forbidden**

- `EMAIL_FROM` must be a **verified** sender; ensure API key has **Mail Send** permission.

**DuckDuckGo tool broke**

- `ddgs` is a scraping wrapper; if DDG changes, update `ddgs` or pin a working version.

---

## 🔧 Dev tips

- Switch Gradio Chatbot to `type="messages"` later if desired; right now `type="tuples"` matches our data.
- Add concurrency throttling with a semaphore if you see rate limits.
- Persist reports to a database or S3 by swapping the file write in the UI.

---

## 📜 License

Choose a license (MIT/Apache‑2.0) and add it here.

