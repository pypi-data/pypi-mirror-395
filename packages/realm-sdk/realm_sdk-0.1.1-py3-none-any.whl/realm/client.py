"""Realm Client - Main SDK interface"""

import requests
from typing import Any, Optional
from .types import EventType


class RealmClient:
    """
    Realm Client for tracking agent events.

    Usage:
        client = RealmClient(
            api_url="http://localhost:3001",
            project_id="your-project-id"
        )

        # Create a session
        session_id = client.create_session(name="My Agent Run")

        # Track events
        client.track_tool_call(
            session_id=session_id,
            tool_name="search",
            tool_input={"query": "test"},
            tool_output={"result": "success"}
        )

        # Close session
        client.close_session(session_id)
    """

    def __init__(
        self,
        api_url: str = "http://localhost:3001",
        project_id: str = "00000000-0000-0000-0000-000000000000",
        api_key: Optional[str] = None,
    ):
        """
        Initialize Realm client.

        Args:
            api_url: URL of the Realm API server
            project_id: Project ID (get from Realm dashboard)
            api_key: API key for authentication (optional for MVP)
        """
        self.api_url = api_url.rstrip("/")
        self.project_id = project_id
        self.api_key = api_key
        self.session = requests.Session()
        self.current_state: dict[str, Any] = {}

        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def create_session(
        self,
        name: str,
        branch_name: str = "main",
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Create a new session.

        Args:
            name: Name of the session
            branch_name: Branch name (default: "main")
            metadata: Optional metadata

        Returns:
            Session ID
        """
        response = self.session.post(
            f"{self.api_url}/api/sdk/sessions",
            json={
                "projectId": self.project_id,
                "name": name,
                "branchName": branch_name,
                "metadata": metadata,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["id"]

    def track_tool_call(
        self,
        session_id: str,
        tool_name: str,
        tool_input: dict[str, Any],
        tool_output: dict[str, Any],
        reasoning: Optional[str] = None,
        branch_name: str = "main",
    ) -> dict[str, Any]:
        """
        Track a tool call event.

        Args:
            session_id: Session ID
            tool_name: Name of the tool
            tool_input: Tool input data
            tool_output: Tool output data
            reasoning: Optional reasoning
            branch_name: Branch name (default: "main")

        Returns:
            Event data
        """
        state_before = self.current_state.copy()

        # Update current state (simplified)
        self.current_state[f"{tool_name}_result"] = tool_output

        response = self.session.post(
            f"{self.api_url}/api/sdk/events",
            json={
                "sessionId": session_id,
                "eventType": EventType.TOOL_CALL.value,
                "toolName": tool_name,
                "toolInput": tool_input,
                "toolOutput": tool_output,
                "reasoning": reasoning,
                "stateBefore": state_before,
                "stateAfter": self.current_state.copy(),
                "branchName": branch_name,
            },
        )
        response.raise_for_status()
        return response.json()

    def track_decision(
        self,
        session_id: str,
        reasoning: str,
        alternatives: Optional[list[str]] = None,
        confidence: Optional[float] = None,
        branch_name: str = "main",
    ) -> dict[str, Any]:
        """
        Track an LLM decision event.

        Args:
            session_id: Session ID
            reasoning: Decision reasoning
            alternatives: Alternative options considered
            confidence: Confidence score (0.0 to 1.0)
            branch_name: Branch name (default: "main")

        Returns:
            Event data
        """
        state_before = self.current_state.copy()

        response = self.session.post(
            f"{self.api_url}/api/sdk/events",
            json={
                "sessionId": session_id,
                "eventType": EventType.LLM_DECISION.value,
                "reasoning": reasoning,
                "alternativesConsidered": alternatives,
                "confidence": confidence,
                "stateBefore": state_before,
                "stateAfter": self.current_state.copy(),
                "branchName": branch_name,
            },
        )
        response.raise_for_status()
        return response.json()

    def update_state(self, key: str, value: Any):
        """Update the current state."""
        self.current_state[key] = value

    def close_session(self, session_id: str, duration_ms: Optional[int] = None):
        """
        Mark a session as completed.

        Args:
            session_id: Session ID
            duration_ms: Duration in milliseconds
        """
        response = self.session.patch(
            f"{self.api_url}/api/sdk/sessions/{session_id}",
            json={
                "status": "completed",
                "durationMs": duration_ms,
            },
        )
        response.raise_for_status()
        return response.json()

