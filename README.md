# Cedar & Crumb Bakery — Agent-Powered Business Assistant

EECE 503P/798S: Agentic Systems — Assignment C3 (Introduction to Agents)

A chatbot that represents **Cedar & Crumb Bakery**, a fictional artisan bakery. It answers questions
from the business profile, routes each message to the right handling path, collects leads, and logs
customer feedback and unanswered questions through tool calls. It runs on Gemini through the
OpenAI-compatible API and is served with Gradio.

## Project structure

```
business_bot/
├── me/
│   ├── about_business.pdf       # Business profile (PDF)
│   └── business_summary.txt     # Short summary (TXT)
├── scripts/
│   └── make_about_pdf.py        # Generates about_business.pdf
├── business_agent.ipynb         # Main chatbot code
├── .env.example                 # Template for .env (API key)
└── requirements.txt             # Libraries used
```

## Setup

1. Create and activate a virtual environment, then install the requirements:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and put your Gemini API key in it
   (free at https://aistudio.google.com/apikey). `.env` is gitignored.

3. Open `business_agent.ipynb`, select the `.venv` kernel, and run all cells.

**Models.** The defaults run on a free Gemini key: `gemini-3.5-flash-lite` for the agent and
`gemini-3.1-flash-lite` for the router. They are different models on purpose, so each has its own
free-tier per-minute limit. If a per-minute limit is hit, the notebook waits and retries. With a paid key
you can set `GEMINI_MODEL=gemini-3.5-flash` in `.env` for stronger answers.

## Features

_To be completed as the steps are built._

- [x] Business identity (PDF + summary). Regenerate the PDF with `python scripts/make_about_pdf.py`
- [x] Persona and instructions, clearly separated (notebook sections 3.1 and 3.2), assembled into `system_prompt`
- [x] Router: general question / lead collection / feedback (notebook section 6). An LLM classifier
  with a keyword fallback; each route sets its own guidance, tools and `tool_choice`
- [x] Tools: `record_customer_interest`, `record_feedback`, documented MCP-style (notebook section 5).
  Every call is printed and appended to `logs/leads.jsonl` or `logs/feedback.jsonl` (gitignored)
- [x] Agent loop with chat history (short-term memory) and tool calling (notebook section 7), plus a
  guardrail in code: a lead is only saved with an email the customer actually typed
- [ ] Gradio ChatInterface
- [ ] Bonus: reflection step with logged draft and revised replies

## Demo video

_Link to be added._
