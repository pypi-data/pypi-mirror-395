from typing import Any, Dict, Optional

from agentgear.sdk.client import AgentGearClient


def instrument_openai_chat(
    openai_client: Any,
    agentgear: AgentGearClient,
    model: str,
    prompt_version_id: Optional[str] = None,
):
    """
    Wraps OpenAI chat completions to automatically log runs.
    """

    original = openai_client.chat.completions.create

    def wrapped(**kwargs):
        messages = kwargs.get("messages")
        input_text = str(messages)
        response = original(**kwargs)
        output_text = _response_text(response)

        usage = getattr(response, "usage", None) or {}
        token_usage = {
            "prompt": getattr(usage, "prompt_tokens", None) or usage.get("prompt_tokens"),
            "completion": getattr(usage, "completion_tokens", None) or usage.get("completion_tokens"),
            "total": getattr(usage, "total_tokens", None) or usage.get("total_tokens"),
        }
        agentgear.log_run(
            name=f"openai:{model}",
            input_text=input_text,
            output_text=output_text,
            prompt_version_id=prompt_version_id,
            token_usage=token_usage,
            latency_ms=None,
        )
        return response

    openai_client.chat.completions.create = wrapped
    return openai_client


def _response_text(response: Any) -> str:
    try:
        if hasattr(response, "choices") and response.choices:
            content = getattr(response.choices[0].message, "content", None)
            if content:
                return content
        return str(response)
    except Exception:
        return str(response)
