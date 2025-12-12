import os
import uuid
from typing import Dict, Any, Optional

import requests
from info_llm_observe.providers.base import ObservabilityProvider


class PhoenixProvider(ObservabilityProvider):
    """
    Phoenix Observability Provider (REST based).

    This implementation matches the REAL endpoints found in your Phoenix OpenAPI:

        POST /v1/projects/{project_identifier}/spans

    IMPORTANT:
    - Phoenix DOES NOT support project creation via REST.
    - Phoenix DOES NOT support POST /traces.
    - We send *spans*, not traces.
    """

    def __init__(self, project_name: str, base_url: Optional[str] = None, timeout: int = 8):
        self.project_name = project_name
        self.base_url = (base_url or os.getenv("PHOENIX_BASE_URL", "")).rstrip("/")
        self.timeout = timeout

        if not self.base_url:
            raise RuntimeError("PHOENIX_BASE_URL must be set in environment or provided explicitly.")

        # In your Phoenix API, project identifiers are simply names.
        self.project_id = self.ensure_project()

    # ---------------------------------------------------------
    # Low-level HTTP helpers
    # ---------------------------------------------------------
    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        r = requests.post(url, json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json() if r.text else {}

    # ---------------------------------------------------------
    # Project handling
    # Phoenix has NO project creation API → just return name.
    # ---------------------------------------------------------
    def ensure_project(self) -> str:
        """
        Phoenix does not support project creation via API.
        The project identifier is simply the project name.
        """
        return self.project_name

    # ---------------------------------------------------------
    # Span publishing (Phoenx-compatible)
    # ---------------------------------------------------------
    def send_trace(self, trace_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish a *span* to Phoenix.

        According to your Phoenix OpenAPI:

            POST /v1/projects/{project_identifier}/spans
            Body:
            {
                "spans": [
                    { span object... }
                ]
            }
        """

        span = {
            "trace_id": trace_payload["trace_id"],
            "span_id": str(uuid.uuid4()),
            "name": trace_payload.get("operation", "provision-test"),
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": "2025-01-01T00:00:01Z",
            "attributes": {
                "input": trace_payload.get("input"),
                "output": trace_payload.get("output"),
                "tokens": trace_payload.get("tokens"),
                "cost": trace_payload.get("cost"),
                "duration": trace_payload.get("duration"),
                **trace_payload.get("metadata", {})
            }
        }

        payload = {"spans": [span]}

        path = f"/v1/projects/{self.project_id}/spans"

        return self._post(path, payload)

    # ---------------------------------------------------------
    # Test trace for provisioning
    # ---------------------------------------------------------
    def send_test_trace(self) -> Dict[str, Any]:
        """
        Sends a simple test span to Phoenix to confirm connectivity.
        """
        trace_payload = {
            "trace_id": str(uuid.uuid4()),
            "session_id": str(uuid.uuid4()),
            "operation": "provision-test",
            "input": "ping",
            "output": "pong",
            "tokens": 1,
            "cost": 0.0,
            "duration": 0.1,
            "metadata": {"source": "info-llm-observe"},
        }

        return self.send_trace(trace_payload)
