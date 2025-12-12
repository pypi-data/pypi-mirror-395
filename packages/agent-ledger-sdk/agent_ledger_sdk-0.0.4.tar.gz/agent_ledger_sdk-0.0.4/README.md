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
import os
import time

from agent_ledger_sdk import AgentLedgerClient, BudgetGuardrailError
from openai import OpenAI

ledger = AgentLedgerClient(api_key=os.environ["LEDGER_API_KEY"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

session_id = ledger.start_session("support-bot")
try:
    started = time.perf_counter()
    completion = openai_client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": "Draft a concise welcome email for a premium banking customer.",
            }
        ],
        temperature=0.3,
    )
    latency_ms = int((time.perf_counter() - started) * 1000)
    answer = completion.output[0].content[0].text
    usage = completion.usage

    ledger.log_llm_call(
        session_id,
        {
            "step_index": 0,
            "provider": "openai",
            "model": completion.model,
            "prompt": "Draft a concise welcome email for a premium banking customer.",
            "response": answer,
            "tokens_in": usage.input_tokens,
            "tokens_out": usage.output_tokens,
            "latency_ms": latency_ms,
        },
    )
    ledger.end_session(session_id, "success")
except BudgetGuardrailError as exc:
    print("Budget exceeded", exc.details)
    ledger.end_session(session_id, "error", error_message="Budget hit")
finally:
    ledger.close()
```

> ℹ️ Bring your own OpenAI (or other) API keys. The SDK never proxies LLM calls—you run them directly with your provider’s Python client and log the relevant metadata into Agent Ledger.

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
