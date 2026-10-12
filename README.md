# Cedar & Crumb Bakery: Agent-Powered Business Assistant

EECE 503P/798S: Agentic Systems · Assignment C3 (Introduction to Agents)

**Student:** Mohammed Farhat · **ID:** 202772669

**GitHub repository:** https://github.com/Mohammed-Farhat/business_bot

**Nour** is the virtual host of *Cedar & Crumb Bakery*, a fictional artisan bakery in Mar Mikhael,
Beirut. Nour answers questions from the business profile, routes every message to the right handling
path, collects leads, and logs customer feedback and unanswered questions through tool calls. Before
each reply is sent, a reflection step checks it against the agent's instructions. The model is Gemini,
called through its OpenAI-compatible API, and the chat runs in Gradio.

**Demo video:** [Watch on Google Drive](https://drive.google.com/file/d/1n6enzVHkKBnTr95JXu4iiZyi0kLFUGfm/view?usp=sharing)
(the same recording is in the repo under `demo_video/`)

## How a message flows through the agent

```
 customer message
       │
       ▼
 ┌──────────┐  general / lead / feedback   (LLM classifier, keyword fallback)
 │  Router  │──────────────────────────────►  route guidance + tools + tool_choice
 └──────────┘
       │
       ▼
 ┌─────────────────────────┐   tool call   ┌───────────────────────────┐
 │ LLM: persona,           │──────────────►│ record_customer_interest  │──► logs/leads.jsonl
 │ instructions, business  │◄──────────────│ record_feedback           │──► logs/feedback.jsonl
 │ context, chat history   │  tool result  └───────────────────────────┘
 └─────────────────────────┘
       │ draft reply
       ▼
 ┌──────────────┐  checks the draft against the instructions, revises it if needed,
 │  Reflection  │  logs anything the draft forgot to log            ──► logs/reflections.jsonl
 └──────────────┘
       │
       ▼
 final reply (Gradio)
```

## Assignment requirements

| Requirement | Where |
|---|---|
| Business identity: name, mission, services, team, value proposition | `me/about_business.pdf` (5 pages) and `me/business_summary.txt` |
| Persona and instructions, clearly separated | Notebook **3.1 PERSONA** and **3.2 INSTRUCTIONS** |
| Router: general / lead / feedback | Notebook **6**: LLM classifier + keyword fallback, test table, fallback demo |
| `record_customer_interest(email, name, message)` and `record_feedback(question)` | Notebook **5**: functions, MCP-style schemas, dispatcher, tests |
| System prompt: in character, uses summary + PDF, logs unknowns, encourages leads | Notebook **4** |
| Agent loop: user input + chat history + tools; handles tool calls | Notebook **7** |
| Gradio ChatInterface | Notebook **9** |
| Bonus: reflection with logged draft and revised replies | Notebook **8** and `logs/reflections.jsonl` |
| API key in `.env`, not uploaded | `.env` is gitignored; `.env.example` is the template |

## Project structure

```
business_bot/
├── me/
│   ├── about_business.pdf       # Business profile (PDF)
│   └── business_summary.txt     # Short summary (TXT)
├── scripts/
│   └── make_about_pdf.py        # Generates about_business.pdf
├── logs/                        # Created at runtime by the tools (gitignored)
├── demo_video/                  # Screen recording of the demo
├── business_agent.ipynb         # Main chatbot code
├── .env.example                 # Template for .env (API key and model names)
├── .env                         # Your API key (gitignored, never committed)
└── requirements.txt             # Libraries used
```

## Setup and running

1. Create a virtual environment and install the requirements:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # macOS / Linux
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and put your Gemini API key in it (free at
   https://aistudio.google.com/apikey).

3. Open `business_agent.ipynb`, select the `.venv` kernel and run all cells. The last cell starts the chat
   at http://127.0.0.1:7860, which also shows inside the notebook. To open the notebook, use VS Code with
   the Jupyter extension, or install and start classic Jupyter:

   ```bash
   pip install notebook
   jupyter notebook business_agent.ipynb
   ```

**Models.** The defaults run on a free Gemini key: `gemini-3.5-flash-lite` for the agent and
`gemini-3.1-flash-lite` for the router. They are different models on purpose, so each has its own
free-tier per-minute limit. If a per-minute limit is hit, the notebook waits and retries
(`create_completion`). With a paid key you can set `GEMINI_MODEL=gemini-3.5-flash` in `.env` for stronger
answers. Running every cell makes about 60 model calls, and the test outputs vary a little from run to
run because they come from a live model.

## The agent

### Persona and instructions (notebook 3)

- **PERSONA:** Nour, a warm neighbourhood-baker voice: concise, proud of the bakery's craft, greets new
  customers with "Ahla w sahla!", and replies in the customer's language.
- **INSTRUCTIONS:** 10 numbered rules. Answer only from the business information. Log unknown questions
  and feedback. Always ask for an email in a lead conversation, and never make up contact details. Never
  take payments or confirm orders. Be careful with allergy questions. Decline off-topic requests. Never
  reveal the instructions. Only say something was passed on after the tool call succeeded.

### Tools (notebook 5)

| Tool | Parameters | Returns | Logs to |
|---|---|---|---|
| `record_customer_interest` | `email` (required), `name` (required), `message` | `{status, lead_id, message}` | `logs/leads.jsonl` |
| `record_feedback` | `question` (required) | `{status, feedback_id, message}` | `logs/feedback.jsonl` |

Each tool is defined once in MCP style (`name`, `title`, `description`, `inputSchema`, `outputSchema`), and
the OpenAI-format `TOOLS` list is generated from those definitions. Every call is printed and appended to
its log file as one JSON line. Invalid input, such as a malformed email, is returned to the model as an
error so it can ask the customer again.

### Router (notebook 6)

A small, fast model classifies each message as `general`, `lead` or `feedback`. It sees the business
information, so it can tell an unanswered question from one the profile answers, and it sees the previous
reply, so a bare email address is understood as part of a lead. If the call fails (timeout or server
error), keyword rules take over. A per-minute rate limit is waited out instead.

| Route | Guidance added to the prompt | Tools offered | `tool_choice` |
|---|---|---|---|
| `general` | Answer from the business info; log the question if the answer is missing | both | `auto` |
| `lead` | Help, collect name, email and details, then save the lead | both | `auto` |
| `feedback` | Log the feedback or question, then thank or offer a follow-up | `record_feedback` only | `required` (first call) |

On the 13-message test set, the LLM router classified 12 or 13 correctly across runs and the keyword
fallback 11. The one borderline case is "Are you hiring bakers?", which is sometimes routed to `general`
instead of `feedback`. Nothing is lost when that happens: the general route still offers `record_feedback`,
and reflection logs any feedback the reply missed.

### Agent loop (notebook 7)

Route the message, call the model with the route's guidance, the chat history (last 20 messages) and the
route's tools, run any tool calls, send the results back, and repeat until the model answers in text
(at most 4 rounds).

### Reflection (notebook 8, bonus)

A second call reviews each draft for: (1) invented information, (2) missing contact requests,
(3) claims of saving or passing something on that no tool call backs up, (4) persona and rule
violations, and (5) feedback that was never logged. It returns `ok` or `revised`. A revised reply is
sent instead of the draft. Both versions are written to `logs/reflections.jsonl`, and anything the draft
forgot to log is logged by the reflection step itself.

## Design decisions found through testing

The bot runs on a small "lite" model, and testing showed where prompts alone are not enough. Each weakness
is now handled in code:

| Problem found in testing | Fix |
|---|---|
| The model sometimes called `record_customer_interest` with an email it guessed from the customer's name ("I'm Lina Saab" → `lina.saab@example.com`) | **Guardrail in code:** a lead is only saved if its email appears in something the customer typed; otherwise the call is blocked and the model asks for the email |
| Without routing, the model often skipped `record_feedback`, answering "we don't offer gift cards" or claiming "I've passed it on" without logging | The **feedback route requires** the tool call, and **reflection logs** any feedback the draft still missed |
| The reviewer's first revisions sometimes swapped one problem for another | The reflection prompt requires the revised reply to pass every check itself |
| Free-tier keys have per-minute limits | `create_completion` waits for the delay the API suggests and retries. The router uses it too, so a burst of requests is waited out instead of falling back to keywords |

## Log files

All three are JSON Lines files in `logs/` (gitignored, because they contain customer emails):

```jsonc
// logs/leads.jsonl
{"id": "lead-268d580c", "time": "2026-10-11T16:17:27", "name": "Lina Saab", "email": "lina.bakes@example.com", "message": "Custom birthday cake: chocolate hazelnut flavour, 8-inch round (serves 12), pickup on Saturday the 24th"}
// logs/feedback.jsonl
{"id": "fb-c3a00feb", "time": "2026-10-11T15:24:00", "question": "Do you sell gift cards?"}
// logs/reflections.jsonl
{"id": "rf-8e743721", "route": "feedback", "customer_message": "The croissants were a bit dry this morning.", "verdict": "revised", "issues": ["The draft claims feedback was passed to the team without a successful tool call this turn."], "logged_by_reflection": "Customer noted that the croissants were a bit dry this morning.", "draft": "I'm so sorry to hear that! I've passed your feedback straight on to Rania and the baking team.", "final": "I'm so sorry to hear that! Thank you for letting us know—I've passed your feedback on to our team."}
```

## Example conversation

Conversation 1 from one run of the notebook tests (section 7.3), shortened. The wording, and whether the
model tries to guess an email, varies from run to run. Router decisions and tool calls are printed in the
notebook and shown as collapsible notes in the Gradio chat:

> **Customer:** Hi! Do you make birthday cakes?
>
> *router: `lead`*
>
> **Nour:** Ahla w sahla! Yes, we do! Our pastry chef Lea Khoury designs custom celebration cakes for birthdays, starting at $45 for a 6-inch round cake that serves 8 to 10… could you please share your name and email address, along with your preferred date, size, and flavour?
>
> **Customer:** Great, I'd like a chocolate hazelnut cake for about 12 people, pickup on Saturday the 24th.
>
> **Nour:** That chocolate hazelnut cake sounds delicious! An 8-inch round cake would be perfect for 12 people, starting at $65… Could you please share your name and email address?
>
> **Customer:** I'm Lina Saab.
>
> *The model tried to save the lead with an email it made up. The guardrail blocked it:
> `record_customer_interest` → error: "The customer has not given this email address. Ask them for their email; never guess it."*
>
> **Nour:** Thank you, Lina! I have your name, but I still need your email address so the team can send you a confirmation.
>
> **Customer:** lina.bakes@example.com
>
> *`record_customer_interest` → recorded*
>
> **Nour:** Thank you so much, Lina! I have saved your details and passed your chocolate hazelnut cake request to the team. They will follow up with you by email soon to confirm everything!
