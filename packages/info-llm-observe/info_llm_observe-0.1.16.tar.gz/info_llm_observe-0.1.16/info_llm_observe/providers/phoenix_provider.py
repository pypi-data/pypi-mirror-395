import os
import uuid
import requests
from typing import Dict, Any, Optional

from info_llm_observe.providers.base import ObservabilityProvider


class PhoenixProvider(ObservabilityProvider):
    """
    Phoenix provider for info-llm-observe.

    This version matches your Phoenix API requirements:
      POST /v1/spans
      Required body:
      {
        "project_id": "...",
        "queries": [],
        "spans": [ {...} ]
      }
    """

    def __init__(self, project_name: str, base_url: Optional[str] = None, timeout: int = 10):
        self.project_name = os.getenv("LLM_OBSERVE_PROJECT_NAME", project_name)
        self.base = (base_url or os.getenv("PHOENIX_BASE_URL", "")).rstrip("/")
        if not self.base:
            raise RuntimeError("PHOENIX_BASE_URL must be set")

        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}

        # Resolve or create the Phoenix project
        self.project_id = self._resolve_or_create_project()

    # -----------------------------
    # HTTP helpers
    # -----------------------------
    def _get(self, path: str):
        url = f"{self.base}{path}"
        r = requests.get(url, headers=self.headers, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, payload: Dict[str, Any]):
        url = f"{self.base}{path}"
        r = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)
        if r.status_code >= 400:
            raise RuntimeError(f"Phoenix POST {url} failed: {r.status_code} {r.text}")
        return r.json() if r.text else {}

    # -----------------------------
    # Project searching + creation
    # -----------------------------
    def _resolve_or_create_project(self) -> str:
        try:
            projects = self._get("/v1/projects")
            if isinstance(projects, dict) and "data" in projects:
                projects = projects["data"]

            for p in projects:
                if p.get("name") == self.project_name:
                    return p.get("id") or p.get("project_id") or self.project_name
        except Exception:
            pass

        # Otherwise create project
        payload = {"name": self.project_name, "description": "created by info-llm-observe"}
        created = self._post("/v1/projects", payload)

        data = created.get("data", created)
        return data.get("id") or data.get("project_id") or self.project_name

    # -----------------------------
    # SPAN INGESTION
    # -----------------------------
    def send_span(self, span: Dict[str, Any]) -> Dict[str, Any]:
        """
        Correct Phoenix ingestion payload shape.
        """
        payload = {
            "project_id": self.project_id,
            "queries": [],       # REQUIRED by Phoenix API even if empty
            "spans": [span]
        }

        return self._post("/v1/spans", payload)

    def send_test_trace(self) -> Dict[str, Any]:
        span = {
            "span_id": str(uuid.uuid4()),
            "trace_id": str(uuid.uuid4()),
            "name": "provision-test",
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": "2025-01-01T00:00:01Z",
            "attributes": {
                "input": "ping",
                "output": "pong",
                "tokens": 1,
                "cost": 0.0,
                "duration": 0.1,
                "source": "info-llm-observe"
            }
        }
        return self.send_span(span)
