import time
from typing import Any, Optional

from agentgear.sdk.client import AgentGearClient


class trace:
    """
    Context manager for recording spans.
    Usage:
        with trace(client, run_id, name="step"):
            ...
    """

    def __init__(
        self,
        client: AgentGearClient,
        run_id: str,
        name: str,
        parent_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        self.client = client
        self.run_id = run_id
        self.name = name
        self.parent_id = parent_id
        self.metadata = metadata
        self.span_id: Optional[str] = None
        self._start = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        latency_ms = (time.perf_counter() - self._start) * 1000 if self._start else None
        try:
            span = self.client.log_span(
                run_id=self.run_id,
                name=self.name,
                parent_id=self.parent_id,
                latency_ms=latency_ms,
                metadata=self.metadata,
            )
            self.span_id = span.get("id")
        except Exception:
            # Best-effort
            pass
        return False

    def child(self, name: str, metadata: Optional[dict[str, Any]] = None) -> "trace":
        """Create a child span context."""
        return trace(
            client=self.client,
            run_id=self.run_id,
            name=name,
            parent_id=self.span_id or self.parent_id,
            metadata=metadata,
        )
