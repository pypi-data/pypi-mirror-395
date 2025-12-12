# agent-ledger-sdk

Python SDK for [Agent Ledger](https://agent-ledger.thabo.xyz). Instrument your agents, stream session data, and enforce budget guardrails with a simple HTTP client.

## Installation

```bash
pip install agent-ledger-sdk
# or
uv add agent-ledger-sdk
```

## Quick start

```python
from agent_ledger_sdk import AgentLedgerClient, BudgetGuardrailError

ledger = AgentLedgerClient(api_key="alk_abc123")

session_id = ledger.start_session("support-bot")
try:
    ledger.log_llm_call(
        session_id,
        {
            "step_index": 0,
            "model": "gpt-4.1",
            "provider": "openai",
            "prompt": "Draft a welcome email",
            "response": "Hello ...",
            "tokens_in": 120,
            "tokens_out": 96,
            "latency_ms": 2100,
        },
    )
    ledger.end_session(session_id, "success")
except BudgetGuardrailError as exc:
    print("Budget exceeded", exc.details)
    ledger.end_session(session_id, "error", error_message="Budget hit")
```

## API overview

| Method | Description |
| --- | --- |
| `AgentLedgerClient(api_key, base_url=None, timeout=10.0)` | Creates a reusable HTTP client. `base_url` falls back to `AGENT_LEDGER_BASE_URL`, otherwise the hosted production endpoint. |
| `start_session(agent_name)` | Begins a session and returns its ID. |
| `end_session(session_id, status, error_message=None)` | Completes a session. |
| `log_events(session_id, events)` | Low-level helper that posts arbitrary event payloads. |
| `log_llm_call`, `log_tool_call`, `log_tool_result` | Typed shortcuts that add the `type` field for you. |

### Budget guardrails

When Agent Ledger blocks spending for an agent, the SDK raises `BudgetGuardrailError`. Inspect the `.details` attribute to see the remaining budget and attempted spend so you can pause execution gracefully.

### Thread safety & async

`AgentLedgerClient` wraps a single `httpx.Client`. Reuse the instance across calls and call `close()` when shutting down, or use it as a context manager. For async workloads, you can build a thin wrapper around `httpx.AsyncClient`; contributions welcome!

## Development

```bash
cd packages/sdk-py
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
pytest
```

## License

MIT
