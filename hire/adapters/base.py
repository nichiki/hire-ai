"""Base adapter class."""

from abc import ABC, abstractmethod
from typing import Any


class AgentAdapter(ABC):
    """Abstract base class for agent adapters."""

    name: str = "base"

    @abstractmethod
    def ask(
        self,
        message: str,
        session_id: str | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """
        Send a message to the agent and get a response.

        Args:
            message: The message to send
            session_id: Optional CLI session ID for continuation
            model: Optional model to use

        Returns:
            dict with keys:
                - response: The agent's response text
                - session_id: The CLI session ID for future continuation
                - raw: The raw output from the CLI (for debugging)
        """
        pass

    def build_command(
        self,
        message: str,
        session_id: str | None = None,
        model: str | None = None,
    ) -> list[str]:
        """Build the command to execute. Override in subclasses."""
        raise NotImplementedError
