# Python Udemy — learning workspace

Personal sandbox for Python and AI course exercises: small scripts, a RAG demo over PDFs, API snippets, and simple agents. Dependencies are pinned in the root `requirements.txt`.

## Requirements

- **Python** 3.12+ recommended (matches the bundled `venv` layout in this repo).
- **Docker** (optional, for the RAG vector database).

## Setup

From the repository root:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` files next to the scripts that need secrets (see each section below). Never commit real API keys.

## Repository layout

| Path | What it is |
|------|------------|
| [`rag_learn/`](rag_learn/) | End-to-end RAG: chunk `sample.pdf`, embed with Gemini, store in Qdrant, answer questions with context + page hints. |
| [`Weather_Agent/`](Weather_Agent/) | Minimal Gemini chat CLI and a separate tool-using agent (weather + shell) backed by GitHub Models inference. |
| [`AI_course/`](AI_course/) | FastAPI and related small examples (e.g. Ollama client usage). |
| [`00_/`](00_/) | Short standalone Python exercises. |

---

## RAG demo (`rag_learn/`)

**Stack:** LangChain, [Qdrant](https://qdrant.tech/), Google Gemini embeddings (`models/gemini-embedding-001`), and the Gemini chat API via an OpenAI-compatible client (`generativelanguage.googleapis.com`).

**Environment** — in `rag_learn/.env` (or export in your shell):

- `GOOGLE_API_KEY` — [Google AI Studio](https://aistudio.google.com/apikey) API key (used for embeddings and chat).

**1. Start Qdrant**

From `rag_learn/`:

```bash
docker compose up -d
```

This exposes Qdrant at `http://localhost:6333`.

**2. Index the PDF**

```bash
cd rag_learn
python index.py
```

This loads `sample.pdf`, splits it into chunks, and upserts them into the `learning_rag` collection.

**3. Chat against the index**

```bash
python chat.py
```

You will be prompted for a question; the script retrieves similar chunks, builds a system prompt with page metadata, and prints the model reply.

To use a different PDF, change `pdf_path` in `index.py` and re-run indexing.

---

## Weather agent (`Weather_Agent/`)

**`weather_agent.py`** — simple REPL that sends prompts to Gemini (`gemini-3-flash-preview`) using the same OpenAI-compatible base URL as `rag_learn/chat.py`.

- **Env:** `GOOGLE_API_KEY` in `.env` next to the script or in the working directory.

**`agent.py`** — multi-step agent with JSON-structured turns: planning, tool calls, and final output. Tools include `get_weather` (via [wttr.in](https://github.com/chubin/wttr.in)) and `run_cmd` (executes shell commands in the `Weather_Agent/` folder).

- **Env:** `GITHUB_TOKEN` for `https://models.inference.ai.azure.com` (GitHub Models).
- **Warning:** `run_cmd` can run arbitrary shell commands; only use in a trusted environment.

---

## AI course snippets (`AI_course/`)

Examples such as a minimal FastAPI app (`fast_api.py`). Extra packages (for example `fastapi`, `uvicorn`, `ollama`) may be needed beyond the root `requirements.txt` if you run those files—install as needed for each script.

---

## License and notes

This is a personal learning repository. Third-party services (Google AI, Qdrant, GitHub Models, wttr.in) have their own terms and rate limits.

If you add new exercises, prefer a short folder name and a one-line comment or docstring at the top of each script describing how to run it and which env vars it expects.
