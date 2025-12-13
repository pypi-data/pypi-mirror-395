"""Type definitions for Realm SDK"""

from enum import Enum
from typing import Any, Optional, TypedDict


class EventType(str, Enum):
    """Event types"""

    TOOL_CALL = "tool_call"
    LLM_DECISION = "llm_decision"
    STATE_CHANGE = "state_change"
    ERROR = "error"


class ToolCallEvent(TypedDict, total=False):
    """Tool call event data"""

    session_id: str
    event_type: str
    tool_name: str
    tool_input: dict[str, Any]
    tool_output: dict[str, Any]
    tool_error: Optional[dict[str, Any]]
    reasoning: Optional[str]
    state_before: Optional[dict[str, Any]]
    state_after: Optional[dict[str, Any]]
    branch_name: str
    metadata: Optional[dict[str, Any]]


class DecisionEvent(TypedDict, total=False):
    """LLM decision event data"""

    session_id: str
    event_type: str
    reasoning: str
    alternatives_considered: Optional[list[str]]
    confidence: Optional[float]
    state_before: Optional[dict[str, Any]]
    state_after: Optional[dict[str, Any]]
    branch_name: str
    metadata: Optional[dict[str, Any]]

