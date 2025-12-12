import requests
from typing import Any, Dict, Optional

def call_llm(provider: str, api_key: str, model_name: str, messages: list[Dict[str, str]], config: Optional[Dict[str, Any]] = None) -> str:
    if provider == "openai":
        return _call_openai(api_key, model_name, messages, config)
    else:
        raise ValueError(f"Provider {provider} not supported yet")

def _call_openai(api_key: str, model: str, messages: list[Dict[str, str]], config: Optional[Dict[str, Any]]) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        **(config or {})
    }
    
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    if not resp.ok:
        raise Exception(f"OpenAI Error: {resp.text}")
    
    result = resp.json()
    return result["choices"][0]["message"]["content"]
