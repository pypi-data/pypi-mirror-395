import os
import uuid
import requests
from typing import Any, Dict, Optional, List

from info_llm_observe.providers.base import ObservabilityProvider


class PhoenixProvider(ObservabilityProvider):
    """
    Phoenix Observability Provider
    Implements the required abstract methods:
        - ensure_project
        - send_trace
    """

    def __init__(self, project_name: str, base_url: Optional[str] = None, timeout: int = 10):
        self.project_name = project_name
        self.base = (base_url or os.getenv("PHOENIX_BASE_URL", "")).rstrip("/")
        if not self.base:
            raise RuntimeError("PHOENIX_BASE_URL must be set.")

        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}

        # resolve project_id at init
        self.project_id = self.ensure_project()

    # ---------------------------
    # HTTP Helpers
    # ---------------------------
    def _get(self, path: str):
        resp = requests.get(f"{self.base}{path}", headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, json_payload: Dict[str, Any]):
        resp = requests.post(f"{self.base}{path}", headers=self.headers, json=json_payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json() if resp.text else {}

    # ---------------------------
    # REQUIRED ABSTRACT METHODS
    # ---------------------------
    def ensure_project(self) -> str:
        """
        Checks Phoenix /v1/projects for an existing project. If not found, creates it.
        Returns: project_id (string)
        """

        # Try list first
        try:
            resp = self._get("/v1/projects")
            projects = resp.get("data", resp)

            if isinstance(projects, list):
                for p in projects:
                    if p.get("name") == self.project_name:
                        return p.get("id") or p.get("project_id")
        except Exception:
            pass  # ignore list failure → fallback to create

        # Create new project
        body = self._post("/v1/projects", {
            "name": self.project_name,
            "description": f"Project {self.project_name} created by llm-ops"
        })

        data = body.get("data", body)
        pid = data.get("id") or data.get("project_id")
        if not pid:
            raise RuntimeError(f"Phoenix returned unexpected project response: {body}")

        return pid

    def send_trace(self, trace_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapter-level required method.
        Convert trace into a span and send via /v1/spans
        """

        span = {
            "span_id": trace_payload.get("trace_id", str(uuid.uuid4())),
            "trace_id": trace_payload.get("trace_id", str(uuid.uuid4())),
            "name": trace_payload.get("operation", "trace"),
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": "2025-01-01T00:00:01Z",
            "attributes": trace_payload
        }

        return self.send_span(span)

    # ---------------------------
    # Phoenix API span ingestion
    # ---------------------------
    def send_span(self, span: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "project_id": self.project_id,
            "queries": [],     # REQUIRED by Phoenix API
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
