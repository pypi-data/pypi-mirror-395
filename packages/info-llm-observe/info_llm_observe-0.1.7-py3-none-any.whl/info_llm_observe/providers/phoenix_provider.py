import os
import requests
import uuid
from typing import Dict, Any, List, Optional

from info_llm_observe.providers.base import ObservabilityProvider


class PhoenixProvider(ObservabilityProvider):
    """
    Minimal Phoenix provider adapter.

    Expects PHOENIX_BASE_URL environment variable, e.g.
        https://phoenix.example.com

    Note: adapt endpoints as required by your Phoenix deployment.
    """

    def __init__(self, project_name: str, base_url: Optional[str] = None, timeout: int = 8):
        self.project_name = project_name
        self.base_url = (base_url or os.getenv("PHOENIX_BASE_URL", "")).rstrip("/")
        if not self.base_url:
            raise RuntimeError("PHOENIX_BASE_URL must be provided (env or base_url).")

        self.timeout = timeout
        # project_id is resolved on construction
        self.project_id = self.ensure_project()

    # -------------------------
    # Low-level helpers
    # -------------------------
    def _get(self, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        r = requests.post(url, json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # -------------------------
    # Implementation
    # -------------------------
    def ensure_project(self) -> str:
        """
        Check for existing project by name; create if missing.
        Returns the provider's project id string.
        """
        try:
            # list projects - adapt to Phoenix API contract
            resp = self._get("/v1/projects")
            projects = resp.get("data", resp) if isinstance(resp, dict) else resp
            if isinstance(projects, list):
                for p in projects:
                    # assume p has 'name' and 'id' fields; adapt if different
                    if p.get("name") == self.project_name:
                        return p.get("id") or p.get("project_id")
        except Exception:
            # if listing fails, we'll try to create anyway
            pass

        # create project
        payload = {"name": self.project_name, "description": f"Project created by info-llm-observe for {self.project_name}"}
        created = self._post("/v1/projects", payload)
        data = created.get("data", created) if isinstance(created, dict) else created
        if isinstance(data, dict):
            return data.get("id") or data.get("project_id") or data.get("name")
        raise RuntimeError(f"Unexpected response when creating Phoenix project: {created}")

    def send_trace(self, trace_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post a trace to Phoenix under the previously resolved project_id.
        trace_payload should be a dict with details per your Phoenix API schema.
        """
        path = f"/v1/projects/{self.project_id}/traces"
        return self._post(path, trace_payload)

    def send_test_trace(self) -> Dict[str, Any]:
        """
        Convenience function used in provisioning: sends a small test trace.
        """
        trace_payload = {
            "trace_id": str(uuid.uuid4()),
            "session_id": str(uuid.uuid4()),
            "user_id": "system-test",
            "operation": "provision-test",
            "input": "ping",
            "output": "pong",
            "tokens": 1,
            "cost": 0.0,
            "duration": 0.0,
            "metadata": {"info": "test-trace-from-info-llm-observe"},
        }
        return self.send_trace(trace_payload)
