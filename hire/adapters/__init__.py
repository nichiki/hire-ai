"""Agent adapters."""

from .base import AgentAdapter
from .claude import ClaudeAdapter
from .codex import CodexAdapter
from .gemini import GeminiAdapter


def get_adapter(agent: str) -> AgentAdapter:
    """Get an adapter for the specified agent."""
    adapters = {
        "claude": ClaudeAdapter,
        "codex": CodexAdapter,
        "gemini": GeminiAdapter,
    }
    if agent not in adapters:
        raise ValueError(f"Unknown agent: {agent}. Available: {list(adapters.keys())}")
    return adapters[agent]()


__all__ = ["AgentAdapter", "ClaudeAdapter", "CodexAdapter", "GeminiAdapter", "get_adapter"]
