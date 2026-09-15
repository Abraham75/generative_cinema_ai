# Generative Cinema AI

Generative Cinema AI is a runnable screenplay-intelligence foundation. It turns Fountain or plain text into scene-specific, source-grounded suggestions for framing, lighting/color, lens, camera movement, and texture through an offline deterministic engine.

## Current capability

- Strict Pydantic schemas for the current local analysis request/result
- Fountain scene detection with source offsets and plain-text fallback
- Deterministic recommendations that vary with cited screenplay evidence
- Interface-level provider portability for future third-party adapters
- FastAPI health and synchronous analysis endpoints
- JSON CLI, tests, Dockerfile, and CI

This is a **foundation, not a production enterprise platform**. It does not implement authentication, authorization, persistence, database tenant isolation, file upload, a UI, paid API adapters, storyboards, video, collaboration, billing, verified deletion, SSO/SCIM, production monitoring, or compliance certification. `tenant_id` and `project_id` are trace fields only; they do not provide security isolation.

## Quick start

Python 3.11 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
generative-cinema sample_script.fountain
```

Start the local-only API. Keep the explicit loopback bind:

```bash
uvicorn generative_cinema_ai.api:app --host 127.0.0.1 --reload
```

Open `http://127.0.0.1:8000/docs`, or submit:

```bash
curl -X POST http://127.0.0.1:8000/v1/analysis \
  -H 'Content-Type: application/json' \
  -d '{"tenant_id":"00000000-0000-0000-0000-000000000001","project_id":"00000000-0000-0000-0000-000000000002","screenplay_text":"INT. VAULT - NIGHT\nA guard shouts. Mara sprints.","input_format":"fountain"}'
```

The unauthenticated prototype rejects non-loopback clients by default. Outside `APP_ENV=development`, startup also fails unless `ALLOW_NETWORK_API=true` is explicitly set for controlled testing. That override does not add authentication or tenant isolation and must not be used to expose confidential material.

Request bodies are capped at 525,000 bytes by default, and validation responses omit submitted values so screenplay text is not echoed. A production gateway would still require its own smaller-or-equal body limit and body-free logging/telemetry policy.

## Structure

- `src/generative_cinema_ai/models.py` — versioned domain/API contracts
- `src/generative_cinema_ai/parser.py` — deterministic parsing and provenance
- `src/generative_cinema_ai/providers.py` — provider protocol and offline baseline
- `src/generative_cinema_ai/service.py` — transport-independent orchestration
- `src/generative_cinema_ai/api.py` — HTTP transport
- `src/generative_cinema_ai/cli.py` — local CLI
- `tests/` — unit, API, and executable deterministic evaluation checks
- `docs/architecture.md` — staged target architecture
- `docs/current-state-audit.md` — original repository audit

The legacy root modules remain temporarily for historical reference. New code should use the packaged API; the old hard-coded functions are unsupported.

## Limits and roadmap

The parser recognizes headings beginning with `INT.`, `EXT.`, `INT./EXT.`, or `EXT./INT.`. It is not a full Fountain implementation. Explicit `plain_text` mode always returns one scene; `fountain` applies the heading subset and preserves a title/preamble as an explicitly marked scene; `auto` uses headings when found. Exact source text, including trailing whitespace, remains represented. Only supplied text is accepted in Wave 1; secure PDF/DOCX/FDX uploads are future work.

Recommendations are rule-based baselines. Confidence is a workflow signal, not an objective artistic score. Every recommendation includes source evidence and requires human creative judgment.

The **Approved Working Interpretation** is to stage capabilities as: screenplay intelligence and editable shot plans, then storyboards, then video. These are capability phases, not maturity labels. Prototype, MVP, beta, and production maturity require separate evidence and release gates.

Next work includes identity and authorization, PostgreSQL row-level security, secure storage, asynchronous jobs, a policy-controlled LLM adapter, review UI, production exports, human evaluation, collaboration, and media providers. Enterprise/studio controls remain conceptual until implemented and verified. Legal review is required for copyright, privacy, provider contracts, and licensing.
