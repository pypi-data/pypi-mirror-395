"""
AgentGear SDK and utilities.

Primary exports:
- AgentGearClient: backend client for logging runs/spans/prompts
- observe: decorator for capturing LLM calls
- trace: context manager for spans
- Prompt: prompt templating and version metadata helper
"""

from agentgear.sdk.client import AgentGearClient
from agentgear.sdk.decorators import observe
from agentgear.sdk.trace import trace
from agentgear.sdk.prompt import Prompt

__version__ = "0.1.0"

__all__ = ["AgentGearClient", "observe", "trace", "Prompt", "__version__"]
