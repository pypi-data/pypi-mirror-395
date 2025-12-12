import os
import uuid
from typing import Dict, Any, Optional
import requests

from info_llm_observe.providers.base import ObservabilityProvider


class PhoenixProvider(ObservabilityProvider):

    def __init__(self, project_name: str, base_url: Optional[str] = None, timeout: int = 8):

        # Prefer explicit env override (from GitHub Actions)
        self.project_name = os.getenv("LLM_OBSERVE_PROJECT_NAME", project_name)

        self.base_url = (base_url or os.getenv("PHOENIX_BASE_URL", "")).rstrip("/")
        if not self.base_url:
            raise RuntimeError("PHOENIX_BASE_URL must be provided")

        self.timeout = timeout

        # Phoenix uses project identifier = project name directly
        self.project_id = self.project_name

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        r = requests.post(url, json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json() if r.text else {}

    def ensure_project(self) -> str:
        # Phoenix does not support CRUD of projects via REST
        return self.project_name

    def send_trace(self, trace_payload: Dict[str, Any]) -> Dict[str, Any]:

        span = {
            "span_id": str(uuid.uuid4()),
            "trace_id": trace_payload["trace_id"],
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

        return self._post(f"/v1/projects/{self.project_id}/spans", payload)

    def send_test_trace(self) -> Dict[str, Any]:
        trace_payload = {
            "trace_id": str(uuid.uuid4()),
            "operation": "provision-test",
            "input": "ping",
            "output": "pong",
            "tokens": 1,
            "cost": 0.0,
            "duration": 0.1,
            "metadata": {"source": "info-llm-observe"},
        }
        return self.send_trace(trace_payload)
