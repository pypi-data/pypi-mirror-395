# AgentGear

<p align="center">
  <img src="https://raw.githubusercontent.com/debpanda/agentgear/main/docs/assets/agentgear-logo.svg" alt="# AgentGear

![AgentGear](https://img.shields.io/pypi/v/agentgear-ai.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

**AgentGear** is the all-in-one open-source platform for **LLM Observability, Prompt Engineering, and Agent Tracing**. It helps you debug, evaluate, and optimize your AI agents with a beautiful, locally hosted dashboard.

## 🚀 Quick Start

Get started in 30 seconds. No complex setup required.

### 1. Install
```bash
pip install agentgear-ai
```

### 2. Run the UI
```bash
agentgear ui
```
The dashboard will open at http://localhost:8000.

---

## ✨ Features

- **🔍 Agent Tracing**: Visualise your agent's thought process with interactive graphs.
- **📝 Prompt Registry**: Version, tag, and test your prompts.
- **🧪 Playground**: Experiment with different LLMs (OpenAI, Anthropic, Gemini, etc.) directly in the UI.
- **📊 Datasets & Evaluations**: Upload test cases (CSV/JSON) and run LLM-as-a-Judge evaluators to catch regressions.
- **📈 Metrics**: Track token usage, latency, and costs.
- **🔒 Secure**: Runs locally on your machine. Your data stays with you.

## 📚 Documentation

For full documentation on how to instrument your code, visit the **[Documentation](http://localhost:8000/guide)** page within the dashboard.

### Basic Instrumentation Example

```python
from agentgear import instrument, start_trace

# 1. Initialize
instrument(
    project_id="my-project",
    api_key="...", # Not needed for local dev
)

# 2. Decorate your functions
@trace_span(name="generate_story")
def generate_story(topic):
    # Your LLM call here...
    return "Once upon a time..."
```

## 🛠 Configuration

AgentGear works out of the box, but you can configure it via environment variables:

- `AGENTGEAR_DATABASE_URL`: Custom database path (default: `sqlite:///~/.agentgear/agentgear.db`)
- `OPENAI_API_KEY`: Required for Playground and Evaluations.

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node 18+ (with npm/pnpm/yarn) — only needed if you want to hack on the UI locally; production install uses the bundled build
- SQLite (default) or Postgres (for cloud)

### 1) Install SDK
```bash
pip install agentgear-ai
```
> Package name is `agentgear-ai`, import path remains `import agentgear`.

### 2) Initialize backend (SQLite dev)
```bash
agentgear init-db
```
> Default SQLite file lives at `~/.agentgear/agentgear.db`. Set `AGENTGEAR_DATABASE_URL` to override (absolute path recommended).

### 3) Launch API + dashboard (served from the Python package)
```bash
agentgear ui  # FastAPI + packaged React dashboard on :8000
# open http://localhost:8000
# first visit prompts you to set an admin username/password
```

### 4) Create project + token (from CLI)
```bash
agentgear create-project --name "My Project"
agentgear create-token --project <project_id>
```
Copy the token (shown once). Use it in SDK calls via `X-AgentGear-Key`.

### 5) Forgot the password?
- Set env vars, restart the server, and sign in with the override:
  - `export AGENTGEAR_ADMIN_USERNAME=admin`
  - `export AGENTGEAR_ADMIN_PASSWORD=change-me`
  - `agentgear ui`
- Clear the env vars afterward if you want to go back to the stored admin user.

---

## SDK Usage

### Configure client
```python
from agentgear import AgentGearClient

# Remote mode (FastAPI running elsewhere)
client = AgentGearClient(
    base_url="https://your-api.example.com",
    api_key="ag_live_...",
    project_id="proj_123",
    local=False,
)

# Local mode (writes directly to SQLite, no API key needed)
local_client = AgentGearClient(
    project_id="proj_123",
    local=True,
)
```

### Observe decorator
```python
from agentgear import observe

@observe(client, name="chat-complete", prompt_version_id="pv_abc")
def complete(prompt: str) -> str:
    # call your LLM here
    return "response"

complete("hi")
```
Captures args, output, latency, prompt version, and errors; logs a run.

### Trace spans
```python
from agentgear import trace

run = client.log_run(name="pipeline", input_text="user input")
with trace(client, run_id=run["id"], name="retrieve") as span:
    # retrieval work
    pass
with trace(client, run_id=run["id"], name="generate", parent_id=span.span_id):
    # generation work
    pass
```

### Prompt templating
```python
from agentgear import Prompt

prompt = Prompt(name="greeting", template="Hello {{ name }}!", version_id="pv_1")
rendered = prompt.render(name="AgentGear")
# register / version prompt
client.register_prompt(name=prompt.name, content=prompt.template, description="Greeting")
client.create_prompt_version(prompt_id="<prompt_id>", content="Hi {{ name }}!")
```

### OpenAI chat instrumentation
```python
from openai import OpenAI
from agentgear.sdk.integrations.openai import instrument_openai_chat

raw_client = OpenAI(api_key="sk-...")
client = AgentGearClient(base_url="http://localhost:8000", api_key="ag_live_...", project_id="proj_123")
instrumented = instrument_openai_chat(raw_client, agentgear=client, model="gpt-4o", prompt_version_id="pv_123")

resp = instrumented.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":"Hello"}])
```

### End-to-end example (log run + spans + prompt link)
```python
from agentgear import AgentGearClient, trace

client = AgentGearClient(
    base_url="http://localhost:8000",
    api_key="ag_live_...",          # from CLI token creation
    project_id="proj_123",
)

# Register a prompt (keeps version history)
prompt = client.register_prompt(name="retrieval-chat", content="Answer using {context}")
pv = client.create_prompt_version(prompt_id=prompt["id"], content="Answer using {context}. Be concise.")

# Log a run and nested spans
run = client.log_run(
    name="qa-flow",
    input_text="What is AgentGear?",
    prompt_version_id=pv["id"],
    token_usage={"prompt": 150, "completion": 120},
)

with trace(client, run_id=run["id"], name="retrieve") as span:
    # do retrieval...
    pass

with trace(client, run_id=run["id"], name="generate", parent_id=span.span_id) as _:
    # call model...
    pass
```

---

## Backend (FastAPI)

### Core entities
- **Project**: id, name, description, created_at
- **API Token**: id, project_id, key_hash (SHA-256), scopes, revoked, last_used_at
- **Prompt / PromptVersion**: registry + versioning
- **Run**: logged LLM call with tokens/cost/latency
- **Span**: child spans for workflows

### Auth
- Header: `X-AgentGear-Key: <token>`
- Scopes (examples): `runs.write`, `prompts.read`, `prompts.write`, `tokens.manage`
- Dashboard login: first visit prompts you to set an admin username/password.
- Password reset: set `AGENTGEAR_ADMIN_USERNAME` and `AGENTGEAR_ADMIN_PASSWORD`, restart, sign in, then clear the env vars if you want to go back to the stored admin user.
- Local mode (`AGENTGEAR_LOCAL_MODE=true`) bypasses auth for dev; keep it `false` in any shared or remote environment.

### Key endpoints
- `POST /api/projects`, `GET /api/projects`, `GET /api/projects/{id}`
- `POST /api/projects/{id}/tokens`, `GET /api/projects/{id}/tokens`, `DELETE /api/projects/{id}/tokens/{token_id}`
- `POST /api/prompts`, `GET /api/prompts`, `GET /api/prompts/{id}`, `POST /api/prompts/{id}/versions`, `GET /api/prompts/{id}/versions`
- `POST /api/runs`, `GET /api/runs`, `GET /api/runs/{id}`
- `POST /api/spans`, `GET /api/spans?run_id=`
- `GET /api/metrics/summary`, `GET /api/health`

### Configuration (env)
| Var | Default | Description |
| --- | --- | --- |
| `AGENTGEAR_DATABASE_URL` | `sqlite:///~/.agentgear/agentgear.db` | DB connection (absolute path recommended; Postgres e.g. `postgresql+psycopg://user:pass@host/db`) |
| `AGENTGEAR_API_HOST` | `0.0.0.0` | Bind host |
| `AGENTGEAR_API_PORT` | `8000` | Bind port |
| `AGENTGEAR_SECRET_KEY` | `agentgear-dev-secret` | Signing/crypto secret |
| `AGENTGEAR_ALLOW_ORIGINS` | `*` | CORS allowlist |
| `AGENTGEAR_LOCAL_MODE` | `false` | If true, bypasses auth (dev only) |
| `AGENTGEAR_ADMIN_USERNAME` | `None` | Optional: override admin login username (e.g. for reset) |
| `AGENTGEAR_ADMIN_PASSWORD` | `None` | Optional: override admin login password (e.g. for reset) |

---

## Dashboard (React + Vite + Tailwind)
- Packaged build is bundled with the PyPI wheel and served from `/` when you run `agentgear ui`.
- For local UI tweaks, use the dev server (below); production installs can skip Node entirely.
- `/projects`: list + create projects
- `/projects/:id`: overview (stats, prompts, runs, tokens)
- `/projects/:id/tokens`: create/revoke tokens (shows raw token once)
- `/runs`: list runs with latency/cost
- `/runs/:id`: run detail + spans
- `/prompts`: prompt registry
- `/prompts/:id`: versions + add version

### Run frontend locally
```bash
cd frontend
npm install
npm run dev
# set API target if not localhost:
# export VITE_AGENTGEAR_API=http://localhost:8000
```
> Production installs get the built dashboard bundled inside the Python package and served from `/` when you run `agentgear ui`.

### Common UI flows
- Sign in (or complete first-time admin setup) at `/`.
- Create a project and issue an API token from the Tokens tab (token shown once).
- Browse runs/spans with latency and cost, filter by project.
- Manage prompts and versions, and see which runs reference each prompt version.

---

## CLI (Typer)
```bash
agentgear --help
agentgear init-db
agentgear create-project --name "Demo"
agentgear create-token --project <project_id> --scopes runs.write prompts.read prompts.write tokens.manage
agentgear list-projects
agentgear demo-data
agentgear ui --host 0.0.0.0 --port 8000 --reload
```

---

## Deployment

### Postgres example
```bash
export AGENTGEAR_DATABASE_URL="postgresql+psycopg://user:pass@host:5432/agentgear"
export AGENTGEAR_LOCAL_MODE=false
agentgear init-db
agentgear ui --host 0.0.0.0 --port 8000 --reload=false
```

### Production notes
- Use Postgres for durability and concurrency.
- Keep `AGENTGEAR_SECRET_KEY` secret.
- Issue per-project tokens with least-privilege scopes.
- Put FastAPI behind HTTPS + reverse proxy (nginx, Caddy, ALB).
- Restrict CORS to trusted origins.

---

## Data Model Overview
- `projects`: id, name, description, created_at
- `api_keys`: id, project_id, key_hash, scopes (JSON), revoked, last_used_at
- `prompts`: id, project_id, name, description
- `prompt_versions`: id, prompt_id, version, content, metadata
- `runs`: id, project_id, prompt_version_id, input/output, tokens, cost, latency, error, metadata
- `spans`: id, project_id, run_id, parent_id, name, timing, metadata

---

## Testing & Dev
- Lint (Python): `ruff check .`
- Tests (Python): `pytest`
- Frontend lint: `npm run lint --prefix frontend`
- Frontend test (placeholder): `npm run test --prefix frontend`

---

## Releasing to PyPI (manual)
```bash
pip install build twine
python -m build
twine upload dist/*
```

---

## Contributing
See `CONTRIBUTING.md` for setup, standards, and review process. PRs welcome!

## License
Apache 2.0. See `LICENSE`.
