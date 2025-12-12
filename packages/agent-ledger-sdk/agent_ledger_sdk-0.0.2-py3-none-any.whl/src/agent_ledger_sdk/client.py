from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Literal, Mapping, MutableMapping, Optional

import httpx

PROD_BASE_URL = "https://agent-ledger-api.azurewebsites.net"

SessionStatus = Literal["success", "error"]


@dataclass(slots=True)
class BudgetGuardrailDetails:
    agent_name: str
    daily_limit_usd: float
    spent_today_usd: float
    attempted_cost_usd: float
    projected_cost_usd: float
    remaining_budget_usd: float


class AgentLedgerError(RuntimeError):
    """Base exception for SDK failures."""


class BudgetGuardrailError(AgentLedgerError):
    """Raised when Agent Ledger blocks an event because of budget guardrails."""

    def __init__(self, message: str, details: BudgetGuardrailDetails) -> None:
        super().__init__(message)
        self.details = details


class AgentLedgerClient:
    """Synchronous HTTP client for the Agent Ledger API."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = 10.0,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self._api_key = api_key
        self._base_url = _resolve_base_url(base_url)
        self._timeout = timeout
        self._client = httpx.Client(transport=transport, timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "AgentLedgerClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        self.close()

    def start_session(self, agent_name: str) -> str:
        response = self._request("POST", "/v1/sessions", json={"agentName": agent_name})
        data = response.json()
        session_id = data.get("id")
        if not isinstance(session_id, str):
            raise AgentLedgerError("Agent Ledger did not return a session id")
        return session_id

    def end_session(
        self,
        session_id: str,
        status: SessionStatus,
        *,
        error_message: Optional[str] = None,
    ) -> None:
        payload: Dict[str, Any] = {"status": status, "errorMessage": error_message}
        self._request("POST", f"/v1/sessions/{session_id}/end", json=payload)

    def log_events(self, session_id: str, events: Iterable[Mapping[str, Any]]) -> None:
        serialized_events = [dict(event) for event in events]
        payload = {"sessionId": session_id, "events": serialized_events}
        self._request("POST", "/v1/events", json=payload)

    def log_llm_call(self, session_id: str, event: Mapping[str, Any]) -> None:
        enriched = dict(event)
        enriched.setdefault("type", "llm_call")
        self.log_events(session_id, [enriched])

    def log_tool_call(self, session_id: str, event: Mapping[str, Any]) -> None:
        enriched = dict(event)
        enriched.setdefault("type", "tool_call")
        self.log_events(session_id, [enriched])

    def log_tool_result(self, session_id: str, event: Mapping[str, Any]) -> None:
        enriched = dict(event)
        enriched.setdefault("type", "tool_result")
        self.log_events(session_id, [enriched])

    def _request(self, method: str, path: str, *, json: Optional[MutableMapping[str, Any]] = None) -> httpx.Response:
        url = f"{self._base_url}{path}"
        headers = {
            "x-api-key": self._api_key,
        }
        response = self._client.request(method, url, json=json, headers=headers)
        if response.status_code == 429:
            details = _parse_guardrail_details(response)
            if details:
                raise BudgetGuardrailError(details.message, details.details)
        if response.is_error:
            message = _extract_error_message(response)
            raise AgentLedgerError(message)
        return response


def _resolve_base_url(explicit: Optional[str]) -> str:
    import os

    if explicit:
        return explicit.rstrip("/")

    env_base = os.environ.get("AGENT_LEDGER_BASE_URL")
    if env_base:
        return env_base.rstrip("/")

    return PROD_BASE_URL


@dataclass(slots=True)
class _GuardrailExtraction:
    message: str
    details: BudgetGuardrailDetails


def _parse_guardrail_details(response: httpx.Response) -> Optional[_GuardrailExtraction]:
    try:
        payload = response.json()
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    details = payload.get("details")
    if not isinstance(details, Mapping):
        return None
    try:
        parsed = BudgetGuardrailDetails(
            agent_name=str(details.get("agentName")),
            daily_limit_usd=float(details.get("dailyLimitUsd", 0)),
            spent_today_usd=float(details.get("spentTodayUsd", 0)),
            attempted_cost_usd=float(details.get("attemptedCostUsd", 0)),
            projected_cost_usd=float(details.get("projectedCostUsd", 0)),
            remaining_budget_usd=float(details.get("remainingBudgetUsd", 0)),
        )
    except Exception:
        return None
    message = str(payload.get("error", "Budget limit exceeded"))
    return _GuardrailExtraction(message=message, details=parsed)


def _extract_error_message(response: httpx.Response) -> str:
    try:
        payload = response.json()
        if isinstance(payload, Mapping) and "error" in payload:
            return str(payload["error"])
    except Exception:
        pass
    if response.text:
        return response.text
    return f"Request failed with status {response.status_code}"
