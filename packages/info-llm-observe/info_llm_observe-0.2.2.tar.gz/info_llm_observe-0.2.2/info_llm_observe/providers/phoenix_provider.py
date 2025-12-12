import os
import uuid
import requests
from typing import Any, Dict, Optional
from datetime import datetime, timezone, timedelta

from info_llm_observe.providers.base import ObservabilityProvider


class PhoenixProvider(ObservabilityProvider):
    """
    Phoenix Observability Provider (correct schema)
    """

    def __init__(self, project_name: str, base_url: Optional[str] = None, timeout: int = 10):
        self.project_name = project_name
        self.base = (base_url or os.getenv("PHOENIX_BASE_URL", "")).rstrip("/")

        if not self.base:
            raise RuntimeError("PHOENIX_BASE_URL must be set.")

        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}

        # Resolve Phoenix project_id
        self.project_id = self.ensure_project()

    # ---------------------------
    # HTTP helpers
    # ---------------------------
    def _get(self, path: str):
        resp = requests.get(f"{self.base}{path}", headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, payload: Dict[str, Any]):
        resp = requests.post(f"{self.base}{path}", headers=self.headers, json=payload, timeout=self.timeout)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            try:
                body = resp.json()
            except:
                body = resp.text
            raise RuntimeError(f"HTTP {resp.status_code} error for {resp.url}: {body}") from e
        return resp.json() if resp.text else {}

    # ---------------------------
    # PROJECT MANAGEMENT
    # ---------------------------
    def ensure_project(self) -> str:
        try:
            resp = self._get("/v1/projects")
            projects = resp.get("data", resp)

            for p in projects:
                if p.get("name") == self.project_name:
                    return p.get("id")
        except:
            pass

        created = self._post(
            "/v1/projects",
            {"name": self.project_name, "description": f"Project {self.project_name}"}
        )

        data = created.get("data", created)
        pid = data.get("id")

        if not pid:
            raise RuntimeError(f"Phoenix project creation failed: {created}")

        return pid

    # ---------------------------
    # SEND TRACE (adapter function)
    # ---------------------------
    def send_trace(self, trace_payload: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        span = {
            "span_id": str(uuid.uuid4()),
            "trace_id": trace_payload.get("trace_id", str(uuid.uuid4())),
            "name": trace_payload.get("operation", "trace"),
            "start_time": now.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "end_time": (now + timedelta(seconds=1)).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "attributes": trace_payload
        }
        return self.send_span(span)

    # ---------------------------
    # SEND SPAN (CORRECT PAYLOAD)
    # ---------------------------
    def send_span(self, span: Dict[str, Any]) -> Dict[str, Any]:

        payload = {
            "data": {                # REQUIRED WRAPPER
                "queries": [],
                "spans": [span]
            }
        }

        path = f"/v1/projects/{self.project_id}/spans"
        return self._post(path, payload)

    # ---------------------------
    # TEST TRACE FOR PROVISION
    # ---------------------------
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
                "source": "llmops",
            }
        }
        return self.send_span(span)
