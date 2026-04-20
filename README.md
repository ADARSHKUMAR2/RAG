# Python Udemy - learning workspace

Personal sandbox for Python and AI course exercises: small scripts, RAG demos, queue-based async processing, LangGraph experiments, memory-enabled assistants, and voice agents. Dependencies are pinned in the root `requirements.txt`.

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
| [`rag_queue/`](rag_queue/) | Queue-based RAG API: FastAPI enqueues prompts, RQ worker processes jobs, Redis/Valkey is used as queue backend. |
| [`langraph_learn/`](langraph_learn/) | LangGraph basics: typed state, nodes/edges, simple chat graph, and a MongoDB checkpointer example. |
| [`mem_agent/`](mem_agent/) | Mem0-based memory assistant using Qdrant + Neo4j for recall and relationship extraction. |
| [`voice_agent/`](voice_agent/) | Speech-to-text + LLM + text-to-speech loops, including a tool-calling voice assistant. |
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

## Queue-based RAG API (`rag_queue/`)

This folder runs the same retrieval + Gemini answering flow behind a queue:

- `server.py`: FastAPI app with:
  - `POST /chat` -> enqueues a job and returns a `job_id`
  - `GET /job_status?job_id=...` -> returns queued/running/completed/failed
- `queues/worker.py`: RQ worker task (`process_query`) that:
  - retrieves similar chunks from Qdrant (`learning_rag`)
  - calls Gemini (`gemini-2.5-flash`) with context + page metadata
  - stores output as job result
- `client/rq_client.py`: Redis connection + shared RQ queue object
- `docker-compose.yml`: local Valkey service on port `6379`

### Prerequisites

- Qdrant running on `http://localhost:6333` (from `rag_learn/docker-compose.yml`).
- Valkey/Redis running on `localhost:6379` (from `rag_queue/docker-compose.yml`).
- `GOOGLE_API_KEY` set in `rag_queue/.env` (or exported in shell).

### Run

From repo root:

```bash
# terminal 1
cd rag_queue
docker compose up -d

# terminal 2
cd rag_queue
rq worker --with-scheduler

# terminal 3
cd rag_queue
python main.py
```

### Test with curl

```bash
# enqueue
curl -X POST "http://localhost:8000/chat?query=Summarize%20page%201"

# check status
curl "http://localhost:8000/job_status?job_id=<job_id>"
```

The second call returns the generated answer in `result` once the worker finishes.

---

## Weather agent (`Weather_Agent/`)

**`weather_agent.py`** — simple REPL that sends prompts to Gemini (`gemini-3-flash-preview`) using the same OpenAI-compatible base URL as `rag_learn/chat.py`.

- **Env:** `GOOGLE_API_KEY` in `.env` next to the script or in the working directory.

**`agent.py`** — multi-step agent with JSON-structured turns: planning, tool calls, and final output. Tools include `get_weather` (via [wttr.in](https://github.com/chubin/wttr.in)) and `run_cmd` (executes shell commands in the `Weather_Agent/` folder).

- **Env:** `GITHUB_TOKEN` for `https://models.inference.ai.azure.com` (GitHub Models).
- **Warning:** `run_cmd` can run arbitrary shell commands; only use in a trusted environment.

---

## LangGraph experiments (`langraph_learn/`)

This folder contains small graph-first experiments:

- `chat.py`: basic `StateGraph` flow with two nodes (`chatbot` -> `sampleNode`) and terminal execution.
- `chat_copy.py`: graph execution with MongoDB checkpointing via `MongoDBSaver`.
- `docker-compose.yml`: local MongoDB service used by the checkpointer example.

### Run

```bash
cd langraph_learn
python chat.py
```

For checkpointing flow:

```bash
cd langraph_learn
docker compose up -d
python chat_copy.py
```

### Environment

- `GITHUB_TOKEN` (or another provider token based on your chosen model/provider setup).
- Any keys referenced by your selected model/provider configuration.

---

## Memory agent (`mem_agent/`)

`mem_agent/mem.py` implements a memory loop with `mem0`:

- retrieves related memories from Qdrant
- enriches prompts with recalled context
- generates responses with Gemini
- stores each new interaction back into memory
- uses Neo4j as graph store for relationship-aware memory

`mem_agent/test_graph.py` is a focused test that checks graph extraction/write behavior on a sample prompt.

### Services required

- Qdrant on `localhost:6333` (see `mem_agent/docker-compose.yml`).
- Neo4j reachable via `NEO4J_URI`.

### Run

```bash
cd mem_agent
docker compose up -d   # starts Qdrant
python mem.py
```

### Environment

- `GOOGLE_API_KEY`
- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `GITHUB_TOKEN` (used by `test_graph.py`)

---

## Voice agents (`voice_agent/`)

This folder has two voice-first scripts:

- `main.py`: microphone input -> Google STT -> LLM response -> Edge TTS playback.
- `cursor.py`: tool-calling voice assistant with structured steps (`PLAN`, `TOOL`, `OUTPUT`) plus TTS playback.

### Run

```bash
cd voice_agent
python main.py
```

or:

```bash
cd voice_agent
python cursor.py
```

### Environment

- `GITHUB_TOKEN` for GitHub Models endpoint (`https://models.inference.ai.azure.com`).

### Notes

- Requires microphone/audio device access.
- Uses `speech_recognition` (Google STT), `edge-tts`, and `pygame` for playback.
- `cursor.py` includes `run_cmd`; treat it as high-trust local execution only.

---

## AI course snippets (`AI_course/`)

Examples such as a minimal FastAPI app (`fast_api.py`). Extra packages (for example `fastapi`, `uvicorn`, `ollama`) may be needed beyond the root `requirements.txt` if you run those files—install as needed for each script.

---

## License and notes

This is a personal learning repository. Third-party services (Google AI, Qdrant, GitHub Models, wttr.in) have their own terms and rate limits.

If you add new exercises, prefer a short folder name and a one-line comment or docstring at the top of each script describing how to run it and which env vars it expects.

If credentials were accidentally committed in any local `.env`, rotate them immediately and replace with placeholders before sharing the repository.
