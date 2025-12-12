# Contributing to AgentGear

Thanks for helping build AgentGear! This project aims to be production-ready, modular, and cloud-friendly. Please follow these guidelines to keep the codebase healthy.

## Development Setup
1. **Clone** and ensure Python 3.10+ and Node 18+ are installed.
2. **Create a virtualenv** and install Python deps (editable):
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
4. **Run backend (dev)**:
   ```bash
   uvicorn agentgear.server.app.main:app --reload
   ```
5. **Lint/test** (adjust as tooling lands):
   ```bash
   ruff check .
   pytest
   npm run lint --prefix frontend
   npm run test --prefix frontend
   ```

## Branching and Commits
- Prefer small, focused PRs.
- Write clear commit messages (imperative mood).
- Include tests for new features and bug fixes.

## Coding Standards
- Python: type hints, dataclasses/pydantic where appropriate, FastAPI best practices, minimize global state.
- Frontend: keep components small; prefer hooks; consistent TypeScript types; Tailwind for layout/theme.
- CLI: Typer with clear help text and safe defaults.
- Add concise comments only where behavior is non-obvious.

## Testing and Data
- Use SQLite for local dev; keep test fixtures small and deterministic.
- Do not commit secrets; prefer `.env` locally.

## Security
- API keys must never be logged in plaintext.
- Validate and scope tokens per project; guard cross-project access.

## Submitting Changes
1. Ensure lint/tests pass.
2. Update docs/README when behavior changes.
3. Open a PR with a short summary, testing notes, and screenshots for UI changes.

Thank you for contributing!
