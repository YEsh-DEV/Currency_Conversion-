# Copilot / AI Agent Instructions — Currency_conversion

Purpose: Give AI coding agents the exact, actionable knowledge needed to be productive in this repo — whether it's empty, scaffolded, or partially implemented.

Quick Start

- If the repo is empty, scaffold an MVP under `backend/` and `frontend/` rather than proposing broad design changes.
- Preferred stacks: **Python + FastAPI** (recommended) or **Node + Express**. Use `requirements.txt` / `package.json` when present.
- Typical commands (PowerShell):

```powershell
# Python path (example)
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
uvicorn backend.app:app --reload --port 8000
pytest -q
```

Big-picture architecture to look for

- Backend API (chat/convert endpoints) — likely under `backend/` or `server/`.
- Tool wrappers (rate providers) — expected under `backend/tools/` (e.g., `get_rate.py`, `providers.py`).
- Agent/controller that formats prompts, validates JSON, and orchestrates tool calls — search for `agent.py`, `controller.py`, or `llm_agent/`.
- Frontend (optional) — `frontend/` or `web/` with a simple chat UI.

Project-specific patterns to follow

- Structured function-calling: LLM outputs should be validated against a schema (Pydantic / TypeScript types). Look for `schemas.py`, `models.py`, or `src/types.ts`.
- Tool signatures commonly used: `GetRate(base, quote, date?)`, `ConvertAmount(amount, base, quote, rate)`, `ParseIntent(text)`. If you change a signature, update the agent prompts and schema simultaneously.
- Cache rates with TTL (Redis or in-memory). If no cache exists, add a simple in-memory TTL cache before adding Redis.

Integration & external dependencies

- Currency rate APIs (Fixer, exchangerate.host, ECB) — wrappers must surface `rate`, `source`, `timestamp`.
- LLM provider (OpenAI/Anthropic/etc.) — prefer provider SDKs that support function-calling or strict JSON outputs.
- Secrets: expect `.env` or `config/`; never commit keys. Add `.env.example` if missing.

What agents should do first (small, safe changes)

- If repo empty: scaffold minimal `backend/app.py`, `backend/tools/get_rate.py`, `backend/schemas.py`, `requirements.txt`, and `README.md`.
- If backend exists: add/verify `backend/schemas.py` to validate LLM JSON outputs before tool execution.
- Add CI-friendly tests: `tests/test_parser.py` and `tests/test_converter.py` with mocked provider responses.

# Copilot / AI Agent Instructions — Currency_conversion

Purpose: Give AI coding agents the exact, actionable knowledge needed to be productive in this repo — whether it's empty, scaffolded, or partially implemented. This file now includes a step-by-step backend process, a TODO checklist for implementation, and explicit guidance about ports and Docker.

Quick Start

- If the repo is empty, scaffold a minimal MVP under `backend/` and `frontend/` and keep changes focused and incremental.
- Preferred stacks: **Python + FastAPI** (recommended) or **Node + Express**. Use `requirements.txt` / `package.json` when present.
- Typical commands (PowerShell):

```powershell
# Create venv, install deps, run dev server (Python/FastAPI example)
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
uvicorn backend.app:app --reload --port 8001
pytest -q
```

Why `8001` above: the host already runs another service on port `8000` and Docker images may expose `8000`. See "Ports & Docker" section below before binding to `8000`.

Big-picture architecture to look for

- Backend API (chat/convert endpoints) — likely under `backend/` or `server/`.
- Tool wrappers (rate providers) — expected under `backend/tools/` (e.g., `get_rate.py`, `providers.py`) and must return `{ rate, source, timestamp }`.
- Agent/controller that formats prompts, validates JSON, and orchestrates tool calls — search for `agent.py`, `controller.py`, or `llm_agent/`.
- Frontend (optional) — `frontend/` or `web/` with a simple chat UI; user will implement frontend separately.

Back-end process (step-by-step) — follow this before coding

1. Project setup and ports
	- Confirm which ports are already in use on the host. If another service uses `8000`, do NOT bind the new FastAPI service to host port `8000` simultaneously.
	- Recommended: run FastAPI on a different host port (e.g., `8001`) during development. If using Docker, you can keep the container exposing `8000` internally and map it to a different host port: `-p 8001:8000`.
	- If you must use `8000`, stop or move the other service, or run services in separate VMs/containers with reverse proxy routing (NGINX) to different upstreams.

2. Environment & secrets
	- Add `.env.example` with placeholders for keys: `RATE_API_KEY=`, `LLM_API_KEY=`, `REDIS_URL=`.
	- Never commit real keys. Use environment variables in Docker and CI.

3. Schemas & validation
	- Add `backend/schemas.py` (Pydantic) or `src/types.ts` to define tool-call shapes: `GetRate`, `ConvertAmount`, `ParseIntent`.
	- Always validate LLM outputs against these models before executing tools.

4. Tool wrappers
	- Implement `backend/tools/get_rate.py` which calls provider(s) and returns `{rate, source, timestamp, ttl_seconds}`.
	- Provide a clear error code shape for upstream handling: `{code, message}`.

5. Caching
	- Start with an in-memory TTL cache for rates. Add Redis only if necessary for persistence or multi-instance deployments.

6. Agent/controller
	- Implement `backend/agent.py` that formats system prompts and few-shot examples, calls the LLM (function-calling if available), validates JSON, and orchestrates `GetRate` / `ConvertAmount` calls.
	- If clarification is needed, the agent should ask a clarifying question instead of guessing.

7. Tests
	- Add `tests/test_parser.py` (intent & amount extraction), `tests/test_converter.py` (math correctness), and mocks for provider responses.

8. Docker & local run
	- Add `Dockerfile` for the backend. Container can `EXPOSE 8000` internally.
	- Map container port to a free host port when running locally: `docker run -p 8001:8000 ...`.

9. CI & linting
	- Mirror local commands in `.github/workflows/ci.yml`. Use `pytest` and `flake8`/`ruff` as found in repo.

10. Observability
	- Add basic logging, error traces, and metrics for LLM call counts and rate-provider errors.

Ports & Docker (explicit guidance)

- Two services cannot bind the same host port simultaneously. If your host already runs a service on `8000`, either:
  - Run FastAPI on another host port (e.g., `8001`) during development, or
  - Use Docker port mapping to keep container internal port `8000` but map to host `8001` (`-p 8001:8000`), or
  - Use a reverse proxy (NGINX) and route different paths to different upstream services.
- It's safe for the backend container to `EXPOSE 8000` internally even if the host maps it to another port.

Project-specific patterns to follow

- Structured function-calling: LLM outputs must match Pydantic / TypeScript schemas. If you update schemas, update the few-shot examples and agent prompt.
- Tool signatures: use `GetRate(base, quote, date?)`, `ConvertAmount(amount, base, quote, rate)`, `ParseIntent(text)`.
- Small PRs: change schema + agent prompt + tests together.

TODO: Backend implementation checklist (for the next coding phase)

- [ ] Create `backend/` layout and `requirements.txt` (or `package.json`) and `README.md`.
- [ ] Add `.env.example` with placeholder keys.
- [ ] Implement `backend/schemas.py` (Pydantic models for tool calls).
- [ ] Implement `backend/tools/get_rate.py` with provider wrappers and error codes.
- [ ] Implement `backend/utils/cache.py` (simple in-memory TTL) and optional `backend/cache_redis.py`.
- [ ] Implement `backend/agent.py` (prompt formatting, LLM invocation, JSON validation, orchestration).
- [ ] Add `tests/test_parser.py`, `tests/test_converter.py` and CI configuration.
- [ ] Add `Dockerfile` and `docker-compose.yml` with example port mapping (`8001:8000`).

Clarifying questions (answer these before coding)

- Which stack do you prefer for backend: **Python + FastAPI** (recommended) or **Node + Express**? (I will default to Python if you don't choose.)
- Is there an existing rate-provider account we should use, or should we start with free providers (exchangerate.host / ECB)?
- For local development, do you prefer the backend to listen on host `8001`, or would you rather stop the existing `8000` service and reuse `8000`?

Editing rules & safety (reminder)

- Validate any LLM-generated JSON with the project's schema before executing tools.
- Keep PRs small: update schema + agent prompt + tests in the same change.
- Never include real API keys in commits; prefer `.env.example` placeholders.

If you want, I can now:
- A) Convert this TODO into actual scaffold files (`backend/app.py`, `backend/tools/get_rate.py`, `backend/schemas.py`, `requirements.txt`) using Python + FastAPI, or
- B) Keep refining this instruction doc for Node + Express instead, or
- C) Wait for your answers to the clarifying questions above before creating code scaffolding.

Please tell me which option (A/B/C) you want and answer the clarifying questions so I can proceed without blocking.

---

Backend-ready: pre-coding checklist (what I will ensure before writing any code)

- Confirm stack and ports: default to **Python + FastAPI** and host port **8001** mapped to container port **8000** (`-p 8001:8000`) because you already run a service on host `8000`.
- Create `.env.example` and document required env vars: `RATE_API_KEY`, `LLM_API_KEY`, `REDIS_URL`, `HOST_PORT=8001`, `CONTAINER_PORT=8000`.
- Create strict schemas (`backend/schemas.py`) and a repository file with example prompts: `backend/agent_prompts.md`.
- Add server-side validation hooks that reject any LLM JSON that does not match Pydantic schemas and return a clear retry path (ask LLM to reformat or ask the user for clarification).
- Provide a mocked LLM client for tests (`tests/mocks/mock_llm.py`) and test harnesses that assert LLM outputs are validated and rejected when invalid.

Anti-hallucination practices (enforced before tool execution)

- Use function-calling or instruct the LLM to output a single JSON object; never trust freeform text for tool invocation.
- Configure low randomness for production/test calls: `temperature=0` and `max_tokens` limited to expected size for function outputs.
- Validate every field of the LLM response against Pydantic schemas. If validation fails, log the raw output (to `logs/llm_raw.log`), increment a metric and ask the model to retry with stricter instruction or fall back to a local regex parser.
- Keep few-shot examples minimal and focused; store them in `backend/agent_prompts.md` so changes are versioned with schema changes.

Minimal example (conceptual) — Pydantic shapes and system prompt

- Pydantic models (example names): `GetRateParams(base: str, quote: str, date: Optional[date])`, `GetRateResult(rate: float, source: str, timestamp: datetime)`.
- System prompt (short):

	"You are a Currency Conversion Agent. When you want to perform an operation, return only a single JSON object that exactly matches one of the available function schemas (`GetRate`, `ConvertAmount`, `Clarify`). If you need more information, return `{\"clarify\": true, \"question\": \"...\"}`. Do not output any other text."

LLM testing & mocking strategy

- Add `tests/test_agent_flow.py` that uses `tests/mocks/mock_llm.py` to return deterministic JSON responses. This ensures the controller, validation, and tool-call flow works without invoking a real LLM during CI.
- Tests should cover: valid tool call, invalid JSON (validation rejects), clarify-question flow, provider error flow, caching behavior.

Error code conventions (examples)

- `RATE_NOT_FOUND` — no rate available for requested date/pair.
- `PROVIDER_ERROR` — upstream API returned 5xx or malformed data.
- `INVALID_PAYLOAD` — LLM produced invalid JSON.

Start-coding checklist (what will be created before first coding sprint)

- `backend/` scaffold: `app.py`, `routes.py`, `tools/get_rate.py`, `agent.py`, `schemas.py`, `utils/cache.py`.
- `.env.example` and `README.md` with explicit dev run commands (use host port `8001`).
- `Dockerfile` exposing internal `8000` and `docker-compose.yml` mapping `8001:8000` for dev.
- Tests and mock LLM client in `tests/` and CI workflow that uses mocks for LLM and provider responses.

Confirmations I need from you before I start scaffolding code

- Confirm backend stack: `Python + FastAPI` (yes/no).
- Confirm host port choice: use `8001` mapped to container `8000` (yes/no), or do you want me to assume you'll free up host `8000`?
- Do you have a preferred rate-provider account/key to add to `.env.example`, or should I default to free provider `exchangerate.host` for scaffolding and tests?

When you confirm those three items I will begin scaffolding the backend (option A) in the next step, one small change at a time, and run tests locally to verify the flow works with mocked LLM/provider calls.