# Demo Video Script

A scene-by-scene plan for the submission video (about 6 to 7 minutes). It shows every item on the
assignment's submission checklist. The chat messages below were dry-run through the full agent, but the
model's wording changes a little from run to run.

## Before recording

1. Make sure `.env` contains your Gemini API key.
2. Optional: empty the `logs/` folder so the log files only contain what happens in the video.
3. Open `business_agent.ipynb`, select the `.venv` kernel and click **Run All**. Running every cell takes
   2 to 5 minutes (about 60 model calls, with short automatic waits if a free-tier per-minute limit is
   hit). When it finishes, the chat is running at http://127.0.0.1:7860.
4. Open http://127.0.0.1:7860 in a browser tab, and keep the notebook and the `logs/` folder in other tabs.

## Scene 1: The project (about 45 s)

- Show the GitHub repository: `me/about_business.pdf`, `me/business_summary.txt`, `business_agent.ipynb`,
  `requirements.txt`, `.env.example`.
- Open `about_business.pdf` for a few seconds: services, menu prices, team, value proposition.
- Show `.gitignore` containing `.env`, and point out that `.env` (the API key) is not in the repository.
  `.env.example` is the template.

## Scene 2: Notebook walkthrough (about 2 min)

| Section | What to point out |
|---|---|
| 3.1 PERSONA / 3.2 INSTRUCTIONS | Two separate, clearly labeled blocks: who Nour is vs. the 10 rules she must follow |
| 4 System prompt | Persona + instructions + summary + PDF assembled into `system_prompt` |
| 5.2 Tool definitions | MCP-style schemas: `name`, `description`, `inputSchema`, `outputSchema` |
| 6.5 Router test | 13 messages, LLM router vs. keyword fallback, with a reason for each decision |
| 6.6 / 6.7 | The fallback when the LLM router fails, and how routing forces `record_feedback` |
| 7.3 Conversation 1 | A lead collected over several messages; the guardrail if the model guesses an email |
| 8.2 Reflection tests | Bad drafts caught and revised; the original draft and revised reply shown side by side |

## Scene 3: Live chat in Gradio (about 3 min)

Type these in **one conversation**. After each reply, expand the collapsed **Router**, **Tool** and
**Reflection** notes above it.

| # | Type this | What to point out |
|---|---|---|
| 1 | `Hi! What's your signature pastry?` | Router: `general`. The answer comes from the PDF (knefeh croissant, $4.50). Reflection: `ok` |
| 2 | `Do you sell gift cards?` | Router: `feedback`. Tool `record_feedback` → `recorded`: an unanswered question is logged, and Nour doesn't guess |
| 3 | `I'd like to order a birthday cake for about 12 people next Saturday, chocolate hazelnut please.` | Router: `lead`. Nour quotes the 8-inch cake (from $65), the 72-hour notice and the deposit, then asks for name and email |
| 4 | `I'm Lina Saab.` | Still `lead`. Nour asks for the email. If the model tries to guess one, the Tool note shows `error` from the guardrail |
| 5 | `lina.bakes@example.com` | Tool `record_customer_interest` → `recorded`. Expand it to show the name, email and order note |
| 6 | `The coffee was cold this morning, a bit disappointing.` | Router: `feedback`. Logged; Nour apologises without promising compensation (rule 3) |
| 7 | `Can you help me with my calculus homework?` | Router: `general`. Politely declined, no tool call (rule 8) |
| 8 | `Is the pistachio pain suisse ok for someone with a nut allergy?` | Allergen information, and no promise that it is safe (rule 7) |

If a **Reflection** note says `revised`, expand it: it lists the issues and the original draft. If no
reply gets revised during the live chat, point back to section 8.2, where the revisions are shown.

## Scene 4: The logs (about 45 s)

Open the three files in `logs/`:

- `leads.jsonl`: Lina's lead with name, email and order note.
- `feedback.jsonl`: the gift-card question and the cold-coffee complaint.
- `reflections.jsonl`: one entry per reply with `verdict`, `issues`, `draft` and `final`. Show a
  `revised` entry where the draft and final reply differ.

## Scene 5: Wrap-up (about 20 s)

Recap: a fictional business with a PDF and summary, separate persona and instructions, a router with three
paths, two logging tools with MCP-style schemas, chat history, a Gradio interface, and the reflection bonus
with logged draft and revised replies.
