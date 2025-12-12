import os
import uuid
import requests
from typing import Any, Dict, Optional
from datetime import datetime, timezone, timedelta

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

        # Resolve project ID from Phoenix
        self.project_id = self.ensure_project()

    # -----------------------------------------------------
    # HTTP Helpers
    # -----------------------------------------------------
    def _get(self, path: str):
        resp = requests.get(f"{self.base}{path}", headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, payload: Dict[str, Any]):
        resp = requests.post(f"{self.base}{path}", headers=self.headers, json=payload, timeout=self.timeout)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            # Try to surface JSON body when server responds with validation errors
            body = None
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise RuntimeError(f"HTTP {resp.status_code} {resp.reason} for {resp.url}: {body}") from e

        return resp.json() if resp.text else {}

    # -----------------------------------------------------
    # PROJECT MANAGEMENT
    # -----------------------------------------------------
    def ensure_project(self) -> str:
        """
        Checks /v1/projects for an existing project.
        If not found → creates one.
        Returns Phoenix project_id (Base64 encoded).
        """
        try:
            resp = self._get("/v1/projects")
            projects = resp.get("data", resp)

            if isinstance(projects, list):
                for p in projects:
                    if p.get("name") == self.project_name:
                        return p.get("id")
        except Exception:
            pass

        # Create new project
        created = self._post(
            "/v1/projects",
            {
                "name": self.project_name,
                "description": f"Project {self.project_name} created by llm-ops"
            }
        )

        data = created.get("data", created)
        project_id = data.get("id")

        if not project_id:
            raise RuntimeError(f"Unexpected Phoenix project creation response: {created}")

        return project_id

    # -----------------------------------------------------
    # SEND TRACE (adapter method required by ObservabilityProvider)
    # -----------------------------------------------------
    def send_trace(self, trace_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert trace_payload to Phoenix span format.
        """
        now = datetime.now(timezone.utc)
        span = {
            "span_id": str(uuid.uuid4()),
            "trace_id": trace_payload.get("trace_id", str(uuid.uuid4())),
            "name": trace_payload.get("operation", "trace"),
            "start_time": now.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "end_time": (now + timedelta(seconds=1)).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "attributes": trace_payload,
        }

        return self.send_span(span)

    # -----------------------------------------------------
    # SEND SPAN (Phoenix ingestion endpoint)
    # -----------------------------------------------------
    def send_span(self, span: Dict[str, Any]) -> Dict[str, Any]:
        """
        Correct endpoint per Phoenix OpenAPI:
        POST /v1/projects/{project_id}/spans
        """

        payload = {
            "queries": [],   # REQUIRED by Phoenix API
            "spans": [span],
        }

        path = f"/v1/projects/{self.project_id}/spans"
        return self._post(path, payload)

    # -----------------------------------------------------
    # Test Trace for Provisioning
    # -----------------------------------------------------
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
                "source": "llmops-provision",
                "tokens": 1,
                "duration": 0.1,
                "cost": 0.0
            }
        }

        return self.send_span(span)
