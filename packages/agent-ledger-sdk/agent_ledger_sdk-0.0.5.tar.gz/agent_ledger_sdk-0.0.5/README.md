# agent-ledger-sdk

Official Python SDK for [Agent Ledger](https://agent-ledger.thabo.xyz). Instrument your AI agents with session telemetry, capture every LLM/tool call, and enforce budget guardrails with a single synchronous HTTP client.

## Table of contents

1. [Features](#features)
2. [Installation](#installation)
3. [Requirements](#requirements)
4. [Quick start](#quick-start)
5. [Session lifecycle](#session-lifecycle)
6. [Event schema](#event-schema)
7. [API reference](#api-reference)
8. [Error handling](#error-handling)
9. [Configuration & environments](#configuration--environments)
10. [Advanced usage](#advanced-usage)
11. [Testing & troubleshooting](#testing--troubleshooting)
12. [Development](#development)
13. [License](#license)

## Features

- Zero-dependency interface beyond `httpx`, so you stay in control of transports, retries, and proxies.
- Typed dataclasses (`BudgetGuardrailDetails`) for precise guardrail reporting.
- Context-manager friendly client that mirrors the Agent Ledger API surface (`/v1/sessions`, `/v1/events`).
- Works anywhere CPython 3.9+ can run (serverless functions, notebooks, background workers).

## Installation

```bash
pip install agent-ledger-sdk
# or with uv
uv add agent-ledger-sdk
```

## Requirements

- Python 3.9 or newer.
- An Agent Ledger API key created in the dashboard.
- Network access to `https://agent-ledger-api.azurewebsites.net`.

## Quick start

```python
import os
import time

from agent_ledger_sdk import AgentLedgerClient, BudgetGuardrailError
from openai import OpenAI

ledger = AgentLedgerClient(api_key=os.environ["AGENT_LEDGER_API_KEY"])
llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

session_id = ledger.start_session("support-bot")
try:
    started = time.perf_counter()
    completion = llm.responses.create(
        model="gpt-4o-mini",
        input=[{"role": "user", "content": "Draft a welcome email."}],
        temperature=0.2,
    )
    latency_ms = int((time.perf_counter() - started) * 1000)
    content = completion.output[0].content[0].text

    ledger.log_llm_call(
        session_id,
        {
            "stepIndex": 0,
            "provider": "openai",
            "model": completion.model,
            "prompt": "Draft a welcome email.",
            "response": content,
            "tokensIn": completion.usage.input_tokens,
            "tokensOut": completion.usage.output_tokens,
            "latencyMs": latency_ms,
        },
    )

    ledger.end_session(session_id, "success")
except BudgetGuardrailError as exc:
    ledger.end_session(session_id, "error", error_message="Budget exceeded")
    print("Budget exceeded", exc.details)
    raise
except Exception:
    ledger.end_session(session_id, "error", error_message="Unhandled failure")
    raise
finally:
    ledger.close()
```

> ℹ️ The SDK never proxies your LLM/tool calls. You run them directly and forward the metadata (prompt, response, tokens, latency) to Agent Ledger for analytics, guardrails, and diffing.

## Session lifecycle

1. **Start** a session as soon as the workflow begins: `ledger.start_session("agent-name")`.
2. **Log events** every time you:
   - call an LLM (`log_llm_call`).
   - invoke a tool (`log_tool_call`).
   - get a tool response (`log_tool_result`).
   - emit a custom diagnostic (`log_events`).
3. **End** the session with `ledger.end_session(...)` so the dashboard can show the outcome next to cost metrics.

Keep the session ID in scope (store it on the request context, job payload, or tracing span) so every downstream component can append telemetry.

## Event schema

The Agent Ledger API expects camelCase keys. The Python SDK forwards your dictionaries as-is, so be sure to match the schema exactly.

| Event | Required keys | Optional keys | Notes |
| --- | --- | --- | --- |
| LLM call | `stepIndex`, `model`, `provider`, `prompt`, `response`, `tokensIn`, `tokensOut`, `latencyMs` | — | Use `log_llm_call`. Agent Ledger prices the call automatically using provider/model/tokens. |
| Tool call | `stepIndex`, `toolName`, `toolInput` | — | Use `log_tool_call` right before invoking the tool. |
| Tool result | `stepIndex`, `toolName`, `toolOutput`, `latencyMs` | — | Use `log_tool_result` after receiving the output. |
| Custom | `type`, `stepIndex`, plus any attributes you want | Anything | Send via `log_events` for domain-specific signals.

Conventions:

- `stepIndex` is a monotonically increasing integer, making prompt/tool diffs straightforward.
- Keep payloads under ~64 KB per event for the best UI experience.
- Numbers should remain numeric (avoid serializing to strings) so the backend can aggregate costs.

## API reference

### `AgentLedgerClient(api_key, *, timeout=10.0, transport=None)`

| Parameter | Type | Description |
| --- | --- | --- |
| `api_key` | `str` (required) | Workspace API key. Raises `ValueError` if empty. |
| `timeout` | `float` | Passed to the underlying `httpx.Client`. |
| `transport` | `httpx.BaseTransport | None` | Inject custom transports (proxies, testing stubs, etc.). |

The client can be used as a context manager:

```python
from agent_ledger_sdk import AgentLedgerClient

with AgentLedgerClient(api_key="sk-...", timeout=5) as ledger:
    session_id = ledger.start_session("batch-writer")
    ledger.end_session(session_id, "success")
```

### `start_session(agent_name: str) -> str`

Creates a session row and returns its UUID.

### `end_session(session_id: str, status: Literal["success", "error"], *, error_message: Optional[str] = None) -> None`

Marks a session as finished. When `status == "error"`, include an `error_message` so the dashboard can surface it.

### `log_events(session_id: str, events: Iterable[Mapping[str, Any]]) -> None`

Low-level ingestion helper. Accepts any iterable, clones each event into a list, and POSTs them to `/v1/events`. Each event must include a `type` field.

### `log_llm_call` / `log_tool_call` / `log_tool_result`

Thin wrappers that add the correct `type` and delegate to `log_events`. Use them to keep your instrumentation consistent.

## Error handling

- `BudgetGuardrailError` — raised when the API returns HTTP 429 with guardrail metadata. The `details` attribute includes:

  ```python
  BudgetGuardrailDetails(
      agent_name="support-bot",
      daily_limit_usd=20.0,
      spent_today_usd=18.4,
      attempted_cost_usd=0.9,
      projected_cost_usd=19.3,
      remaining_budget_usd=0.7,
  )
  ```

  Use it to short-circuit further tool/LLM calls or trigger human intervention.

- `AgentLedgerError` — raised for any other non-success HTTP response (network failures, 4xx/5xx). Contains the server-provided `error` field when available.

## Configuration & environments

- Provide `AGENT_LEDGER_API_KEY` (or load it from your secrets manager) and the SDK targets the hosted API automatically.
- Default endpoint → `https://agent-ledger-api.azurewebsites.net`.

For local experimentation, leave the SDK untouched and proxy traffic through tools like [pytest-httpserver](https://pytest-httpserver.readthedocs.io/) or MSW if you need to inspect requests.

## Advanced usage

- **Custom HTTP transport**: inject an `httpx.HTTPTransport` or `httpx_socks.SyncProxyTransport` to route traffic through proxies or service meshes.
- **Retries**: wrap SDK calls with your preferred retry decorator (e.g., `tenacity`) if you need resilience around transient network errors.
- **Thread safety**: `httpx.Client` is threadsafe; reuse a single `AgentLedgerClient` across worker threads or WSGI/ASGI processes.
- **Async workflows**: if you need `asyncio` support today, instantiate the SDK inside an executor, or adapt it by swapping `httpx.Client` for `httpx.AsyncClient` (PRs welcome!).

## Testing & troubleshooting

- In tests, intercept HTTP calls via `transport` injections or libraries such as pytest-httpserver/MSW so you can assert payloads.
- If the dashboard shows no events, double-check that your event dictionaries use camelCase keys.
- HTTP 401/403 errors mean the API key is missing or revoked—create a new key in the dashboard and update your secrets manager.
- Guardrail errors (HTTP 429) are expected when daily spend is exhausted; catch `BudgetGuardrailError` to degrade gracefully.

## Development

```bash
cd packages/sdk-py
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
pytest
```

## License

MIT
