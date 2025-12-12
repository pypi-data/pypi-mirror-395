import time
from typing import Any, Dict, Optional

import httpx

from agentgear.server.app.db import SessionLocal
from agentgear.server.app.models import Project, Prompt, PromptVersion, Run, Span


class AgentGearClient:
    """Client for sending observability data to AgentGear backend."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        local: bool = False,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.project_id = project_id
        self.local = local
        if not self.local and not self.api_key:
            raise ValueError("api_key is required in remote mode")
        self._http = httpx.Client(base_url=self.base_url, timeout=10.0)

    def _headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers["X-AgentGear-Key"] = self.api_key
        return headers

    def log_run(
        self,
        name: Optional[str] = None,
        input_text: Optional[str] = None,
        output_text: Optional[str] = None,
        prompt_version_id: Optional[str] = None,
        token_usage: Optional[dict[str, Any]] = None,
        cost: Optional[float] = None,
        latency_ms: Optional[float] = None,
        error: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        project_id = self._require_project()
        payload = {
            "project_id": project_id,
            "prompt_version_id": prompt_version_id,
            "name": name,
            "input_text": input_text,
            "output_text": output_text,
            "token_usage": token_usage,
            "cost": cost,
            "latency_ms": latency_ms,
            "error": error,
            "metadata": metadata,
        }
        if self.local:
            return self._log_run_local(payload)
        resp = self._http.post("/api/runs", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def log_span(
        self,
        run_id: str,
        name: str,
        parent_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        latency_ms: Optional[float] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        project_id = self._require_project()
        payload = {
            "project_id": project_id,
            "run_id": run_id,
            "parent_id": parent_id,
            "name": name,
            "start_time": start_time,
            "end_time": end_time,
            "latency_ms": latency_ms,
            "metadata": metadata,
        }
        if self.local:
            return self._log_span_local(payload)
        resp = self._http.post("/api/spans", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def register_prompt(
        self,
        name: str,
        content: str,
        description: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        project_id = self._require_project()
        payload = {
            "project_id": project_id,
            "name": name,
            "description": description,
            "content": content,
            "metadata": metadata,
        }
        if self.local:
            return self._register_prompt_local(payload)
        resp = self._http.post("/api/prompts", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def create_prompt_version(
        self, prompt_id: str, content: str, metadata: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        payload = {"content": content, "metadata": metadata}
        if self.local:
            return self._create_prompt_version_local(prompt_id, payload)
        resp = self._http.post(f"/api/prompts/{prompt_id}/versions", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def _require_project(self) -> str:
        if not self.project_id:
            raise ValueError("project_id is required")
        return self.project_id

    # Local mode helpers (direct DB writes) ---------------------------------
    def _log_run_local(self, payload: dict[str, Any]) -> dict[str, Any]:
        db = SessionLocal()
        try:
            run = Run(
                project_id=payload["project_id"],
                prompt_version_id=payload.get("prompt_version_id"),
                name=payload.get("name"),
                input_text=payload.get("input_text"),
                output_text=payload.get("output_text"),
                token_input=(payload.get("token_usage") or {}).get("prompt"),
                token_output=(payload.get("token_usage") or {}).get("completion"),
                cost=payload.get("cost"),
                latency_ms=payload.get("latency_ms"),
                error=payload.get("error"),
                metadata=payload.get("metadata"),
            )
            db.add(run)
            db.commit()
            db.refresh(run)
            return {
                "id": run.id,
                "project_id": run.project_id,
                "prompt_version_id": run.prompt_version_id,
                "name": run.name,
                "input_text": run.input_text,
                "output_text": run.output_text,
                "token_input": run.token_input,
                "token_output": run.token_output,
                "cost": run.cost,
                "latency_ms": run.latency_ms,
                "error": run.error,
                "metadata": run.metadata,
                "created_at": run.created_at.isoformat(),
            }
        finally:
            db.close()

    def _log_span_local(self, payload: dict[str, Any]) -> dict[str, Any]:
        db = SessionLocal()
        try:
            start_time = payload.get("start_time")
            end_time = payload.get("end_time")
            if isinstance(start_time, str):
                try:
                    from datetime import datetime

                    start_time = datetime.fromisoformat(start_time)
                except Exception:
                    start_time = None
            if isinstance(end_time, str):
                try:
                    from datetime import datetime

                    end_time = datetime.fromisoformat(end_time)
                except Exception:
                    end_time = None
            span = Span(
                project_id=payload["project_id"],
                run_id=payload["run_id"],
                parent_id=payload.get("parent_id"),
                name=payload["name"],
                start_time=start_time or None,
                end_time=end_time or None,
                latency_ms=payload.get("latency_ms"),
                metadata=payload.get("metadata"),
            )
            db.add(span)
            db.commit()
            db.refresh(span)
            return {
                "id": span.id,
                "project_id": span.project_id,
                "run_id": span.run_id,
                "parent_id": span.parent_id,
                "name": span.name,
                "start_time": span.start_time.isoformat(),
                "end_time": span.end_time.isoformat() if span.end_time else None,
                "latency_ms": span.latency_ms,
                "metadata": span.metadata,
            }
        finally:
            db.close()

    def _register_prompt_local(self, payload: dict[str, Any]) -> dict[str, Any]:
        db = SessionLocal()
        try:
            prompt = Prompt(
                project_id=payload["project_id"],
                name=payload["name"],
                description=payload.get("description"),
            )
            db.add(prompt)
            db.commit()
            db.refresh(prompt)
            version = PromptVersion(
                prompt_id=prompt.id,
                version=1,
                content=payload["content"],
                metadata=payload.get("metadata"),
            )
            db.add(version)
            db.commit()
            return {
                "id": prompt.id,
                "project_id": prompt.project_id,
                "name": prompt.name,
                "description": prompt.description,
                "created_at": prompt.created_at.isoformat(),
            }
        finally:
            db.close()

    def _create_prompt_version_local(self, prompt_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        db = SessionLocal()
        try:
            latest = (
                db.query(PromptVersion).filter(PromptVersion.prompt_id == prompt_id).order_by(PromptVersion.version.desc()).first()
            )
            next_version = (latest.version + 1) if latest else 1
            version = PromptVersion(
                prompt_id=prompt_id,
                version=next_version,
                content=payload["content"],
                metadata=payload.get("metadata"),
            )
            db.add(version)
            db.commit()
            db.refresh(version)
            return {
                "id": version.id,
                "prompt_id": version.prompt_id,
                "version": version.version,
                "content": version.content,
                "metadata": version.metadata,
                "created_at": version.created_at.isoformat(),
            }
        finally:
            db.close()


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        return result, elapsed

    return wrapper
