"""LangChain integration for Realm observability."""

from typing import Any, Dict, List, Optional
from uuid import UUID

try:
    from langchain_core.callbacks.base import BaseCallbackHandler
    from langchain_core.agents import AgentAction, AgentFinish
    from langchain_core.outputs import LLMResult
except ImportError:
    raise ImportError(
        "LangChain is required for this integration. "
        "Install it with: pip install langchain-core"
    )

from .client import RealmClient


class RealmCallbackHandler(BaseCallbackHandler):
    """
    LangChain callback handler for Realm observability.
    
    Automatically tracks:
    - Agent reasoning (Chain of Thought)
    - Tool executions (with inputs/outputs)
    - Tool errors
    - LLM calls
    
    Usage:
        from realm import RealmClient
        from realm.langchain import RealmCallbackHandler
        
        client = RealmClient(api_url="...", project_id="...")
        session_id = client.create_session(name="My Agent")
        
        handler = RealmCallbackHandler(client, session_id)
        
        # Pass to LangChain agent
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            callbacks=[handler],
            verbose=True
        )
    """
    
    def __init__(
        self, 
        client: RealmClient, 
        session_id: str,
        track_llm_calls: bool = False,
        verbose: bool = False
    ):
        """
        Initialize Realm callback handler.
        
        Args:
            client: RealmClient instance
            session_id: Active session ID
            track_llm_calls: Whether to track individual LLM API calls (default: False)
            verbose: Print tracking info (default: False)
        """
        super().__init__()
        self.client = client
        self.session_id = session_id
        self.track_llm_calls = track_llm_calls
        self.verbose = verbose
        
        # Track tool runs in flight (run_id -> tool data)
        self.tool_runs: Dict[str, Dict[str, Any]] = {}
        
        # Track pending agent actions (for correlating with tool outputs)
        self.pending_actions: Dict[str, Dict[str, Any]] = {}
        
        # Track agent steps
        self.step_count = 0
    
    def _log(self, message: str):
        """Log if verbose mode is enabled."""
        if self.verbose:
            print(f"[Realm] {message}")
    
    # ===== Agent Reasoning (Chain of Thought) =====
    
    def on_agent_action(
        self, 
        action: AgentAction, 
        *, 
        run_id: UUID, 
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """
        Capture agent reasoning (Chain of Thought) and tool calls.
        
        This is called when the agent decides what action to take.
        The action.log contains the full "Thought: ... Action: ..." trace.
        
        For agents that don't trigger on_tool_start/on_tool_end separately
        (like function-calling agents or Gemini), we track the tool call here.
        """
        self.step_count += 1
        reasoning = action.log if action.log else f"Action: {action.tool}"
        tool_name = action.tool
        tool_input = action.tool_input
        
        self._log(f"Step {self.step_count}: Agent action - {tool_name}")
        
        # Store the pending action for correlation with tool output (if on_tool_end fires)
        self.pending_actions[str(run_id)] = {
            "tool": tool_name,
            "input": tool_input,
            "reasoning": reasoning,
            "tracked": False  # Will be set to True if we track from on_tool_end
        }
        
        # Track as tool_call with the available info
        # This ensures tools are tracked even if on_tool_start/on_tool_end don't fire
        input_dict = tool_input if isinstance(tool_input, dict) else {"input": str(tool_input) if tool_input else ""}
        
        self.client.track_tool_call(
            session_id=self.session_id,
            tool_name=tool_name,
            tool_input=input_dict,
            tool_output={"status": "executed"},  # Placeholder, updated if on_tool_end fires
            reasoning=reasoning
        )
        
        # Mark as tracked so on_tool_end doesn't duplicate
        self.pending_actions[str(run_id)]["tracked"] = True
    
    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track agent completion."""
        self._log("Agent finished")
        
        self.client.track_decision(
            session_id=self.session_id,
            reasoning=f"Agent completed: {finish.return_values.get('output', 'No output')}",
            confidence=1.0
        )
    
    # ===== Tool Execution =====
    
    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Buffer tool inputs for correlation with outputs."""
        tool_name = serialized.get("name", "unknown_tool")
        
        self._log(f"Tool started: {tool_name}")
        
        # Check if we have a pending action for this tool from on_agent_action
        parent_id = str(parent_run_id) if parent_run_id else None
        pending = None
        if parent_id and parent_id in self.pending_actions:
            pending = self.pending_actions.get(parent_id)
        
        self.tool_runs[str(run_id)] = {
            "name": tool_name,
            "input": input_str,
            "pending_action": pending,
            "parent_run_id": parent_id
        }
    
    def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track successful tool execution with full input/output."""
        run_data = self.tool_runs.pop(str(run_id), None)
        
        # Check if this was already tracked from on_agent_action
        parent_id = str(parent_run_id) if parent_run_id else None
        if parent_id and parent_id in self.pending_actions:
            pending = self.pending_actions[parent_id]
            if pending.get("tracked"):
                # Already tracked from on_agent_action, just log
                self._log(f"Tool output received: {pending['tool']} (already tracked)")
                del self.pending_actions[parent_id]
                return
        
        if run_data:
            self._log(f"Tool completed: {run_data['name']}")
            
            # Parse tool input - try to get structured data
            tool_input = run_data.get("input", "")
            if isinstance(tool_input, str):
                # Try to parse as JSON
                import json
                try:
                    tool_input = json.loads(tool_input)
                except (json.JSONDecodeError, TypeError):
                    tool_input = {"input": tool_input}
            
            # Parse tool output
            tool_output = output
            if isinstance(tool_output, str):
                import json
                try:
                    tool_output = json.loads(tool_output)
                except (json.JSONDecodeError, TypeError):
                    tool_output = {"output": tool_output}
            
            # Get reasoning from pending action if available
            pending = run_data.get("pending_action")
            reasoning = pending.get("reasoning") if pending else f"Executed {run_data['name']}"
            
            self.client.track_tool_call(
                session_id=self.session_id,
                tool_name=run_data["name"],
                tool_input=tool_input if isinstance(tool_input, dict) else {"input": tool_input},
                tool_output=tool_output if isinstance(tool_output, dict) else {"output": tool_output},
                reasoning=reasoning
            )
            
            # Clean up pending action if we had one
            parent_id = run_data.get("parent_run_id")
            if parent_id and parent_id in self.pending_actions:
                del self.pending_actions[parent_id]
        else:
            self._log(f"Tool completed but no start event found (run_id: {run_id})")
    
    def on_tool_error(
        self,
        error: Exception,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track tool failures."""
        run_data = self.tool_runs.pop(str(run_id), None)
        
        if run_data:
            self._log(f"Tool failed: {run_data['name']} - {str(error)}")
            
            self.client.track_tool_call(
                session_id=self.session_id,
                tool_name=run_data["name"],
                tool_input={"input": run_data["input"]},
                tool_output={"error": str(error), "error_type": type(error).__name__},
                reasoning=f"Tool execution failed: {str(error)}"
            )
        else:
            self._log(f"Tool failed but no start event found (run_id: {run_id})")
    
    # ===== LLM Calls (Optional) =====
    
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track LLM API calls (if enabled)."""
        if not self.track_llm_calls:
            return
        
        model_name = serialized.get("name", "unknown_model")
        self._log(f"LLM call started: {model_name}")
    
    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track LLM completion (if enabled)."""
        if not self.track_llm_calls:
            return
        
        self._log("LLM call completed")
        
        # Could track as a special event type if needed
        # For now, we focus on agent-level reasoning and tools
    
    def on_llm_error(
        self,
        error: Exception,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track LLM errors (if enabled)."""
        if not self.track_llm_calls:
            return
        
        self._log(f"LLM call failed: {str(error)}")
    
    # ===== Chain Events (Optional, for future use) =====
    
    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track chain execution start."""
        pass  # Can be used for more granular tracking if needed
    
    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track chain execution end."""
        pass  # Can be used for more granular tracking if needed
    
    def on_chain_error(
        self,
        error: Exception,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> None:
        """Track chain execution errors."""
        self._log(f"Chain failed: {str(error)}")
        
        self.client.track_decision(
            session_id=self.session_id,
            reasoning=f"Chain execution failed: {str(error)}",
            confidence=0.0
        )

