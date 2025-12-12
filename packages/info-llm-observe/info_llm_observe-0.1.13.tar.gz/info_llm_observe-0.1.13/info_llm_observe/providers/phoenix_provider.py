import os
import uuid
import requests
from typing import Dict, Any, Optional, List

from info_llm_observe.providers.base import ObservabilityProvider


class PhoenixProvider(ObservabilityProvider):
    """
    Phoenix Observability Provider for info-llm-observe wrapper.
    Uses the correct ingestion API:

        POST /v1/spans
        {
            "project_id": "...",
            "spans": [ ... ]
        }
    """

    def __init__(self, project_name: str, base_url: Optional[str] = None, timeout: int = 10):
        # Project name supplied by wrapper register()
        self.project_name = project_name

        # Prefer environment override from GitHub Actions
        self.base_url = (base_url or os.getenv("PHOENIX_BASE_URL", "")).rstrip("/")
        if not self.base_url:
            raise RuntimeError("PHOENIX_BASE_URL must be set in environment or passed to provider")

        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}

    # ---------------------------------------------
    # Low-level HTTP helpers
    # ---------------------------------------------
    def _post(self, path: str, json_payload: Dict[str, Any]):
        url = f"{self.base_url}{path}"
        resp = requests.post(url, json=json_payload, headers=self.headers, timeout=self.timeout)

        if resp.status_code >= 400:
            raise RuntimeError(
                f"Phoenix POST {url} failed: {resp.status_code} {resp.text}"
            )

        return resp.json() if resp.text else {}

    def _get(self, path: str):
        url = f"{self.base_url}{path}"
        resp = requests.get(url, headers=self.headers, timeout=self.timeout)

        if resp.status_code >= 400:
            raise RuntimeError(
                f"Phoenix GET {url} failed: {resp.status_code} {resp.text}"
            )

        return resp.json()

    # ---------------------------------------------
    # Project resolution
    # ---------------------------------------------
    def ensure_project(self) -> str:
        """
        Phoenix "project_id" is simply the project name.
        Phoenix API does NOT require creating the project via API.
        UI automatically manages project namespace.
        """
        return self.project_name

    # ---------------------------------------------
    # SPAN INGESTION (CORRECT ENDPOINT)
    # ---------------------------------------------
    def send_span(self, span: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send span to Phoenix backend using correct ingestion API.
        """

        request_body = {
            "project_id": self.project_name,  # REQUIRED
            "spans": [span],                 # MUST be array
        }

        return self._post("/v1/spans", request_body)

    # ---------------------------------------------
    # Higher-level convenience: send trace
    # ---------------------------------------------
    def send_trace(self, payload: Dict[str, Any]):
        """
        Convert LLM trace into Phoenix "span" format.
        """

        span = {
            "span_id": str(uuid.uuid4()),
            "trace_id": payload.get("trace_id", str(uuid.uuid4())),
            "name": payload.get("operation", "unknown-operation"),
            "start_time": payload.get("start_time", "2025-01-01T00:00:00Z"),
            "end_time": payload.get("end_time", "2025-01-01T00:00:01Z"),
            "attributes": {
                "input": payload.get("input"),
                "output": payload.get("output"),
                "tokens": payload.get("tokens"),
                "cost": payload.get("cost"),
                "duration": payload.get("duration"),
                **payload.get("metadata", {})
            }
        }

        return self.send_span(span)

    # ---------------------------------------------
    # Provisioning test call
    # ---------------------------------------------
    def send_test_trace(self) -> Dict[str, Any]:

        payload = {
            "trace_id": str(uuid.uuid4()),
            "operation": "provision-test",
            "input": "ping",
            "output": "pong",
            "tokens": 1,
            "cost": 0.0,
            "duration": 0.1,
            "metadata": {"source": "info-llm-observe"}
        }

        return self.send_trace(payload)
