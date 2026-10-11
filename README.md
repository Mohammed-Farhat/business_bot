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

## Features

_To be completed as the steps are built._

- [x] Business identity (PDF + summary). Regenerate the PDF with `python scripts/make_about_pdf.py`
- [x] Persona and instructions, clearly separated (notebook sections 3.1 and 3.2), assembled into `system_prompt`
- [ ] Router: general question / lead collection / feedback
- [ ] Tools: `record_customer_interest`, `record_feedback`
- [ ] Agent loop with chat history and tool calling
- [ ] Gradio ChatInterface
- [ ] Bonus: reflection step with logged draft and revised replies

## Demo video

_Link to be added._
