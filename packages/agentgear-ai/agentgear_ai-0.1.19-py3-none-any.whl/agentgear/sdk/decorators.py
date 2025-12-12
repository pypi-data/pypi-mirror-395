import functools
import json
import time
from typing import Any, Callable, Optional

from agentgear.sdk.client import AgentGearClient


def observe(
    client: AgentGearClient,
    name: Optional[str] = None,
    prompt_version_id: Optional[str] = None,
    metadata: Optional[dict[str, Any]] = None,
):
    """
    Decorator to capture function inputs/outputs and log a run.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            error_text = None
            output_text = None
            try:
                result = func(*args, **kwargs)
                output_text = _safe_string(result)
                return result
            except Exception as exc:  # noqa: BLE001
                error_text = str(exc)
                raise
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                input_repr = _inputs_to_string(args, kwargs)
                try:
                    client.log_run(
                        name=name or func.__name__,
                        input_text=input_repr,
                        output_text=output_text,
                        prompt_version_id=prompt_version_id,
                        latency_ms=elapsed_ms,
                        error=error_text,
                        metadata=metadata,
                    )
                except Exception:
                    # Do not break caller; best-effort logging.
                    pass

        return wrapper

    return decorator


def _inputs_to_string(args, kwargs) -> str:
    try:
        return json.dumps({"args": args, "kwargs": kwargs}, default=str)
    except Exception:
        return f"args={args}, kwargs={kwargs}"


def _safe_string(value: Any) -> str:
    try:
        return json.dumps(value, default=str)
    except Exception:
        return str(value)
