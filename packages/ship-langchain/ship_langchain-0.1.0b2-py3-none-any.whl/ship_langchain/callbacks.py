"""
SHIP Protocol LangChain Callback Handler

Automatically tracks SHIP scores across agent runs for observability.

Design Principles:
    - Non-invasive: Plugs into existing callback system
    - Observable: Rich metrics for monitoring
    - Antifragile: Never crashes the main execution
"""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID
import logging

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.agents import AgentAction, AgentFinish


logger = logging.getLogger(__name__)


class SHIPCallbackHandler(BaseCallbackHandler):
    """
    Callback handler that tracks SHIP metrics across agent runs.

    Integrates with LangChain's callback system to provide observability
    into AI coding task reliability.

    Usage:
        ```python
        from ship_langchain import SHIPCallbackHandler

        handler = SHIPCallbackHandler()
        agent = create_agent(callbacks=[handler])

        # After run
        print(handler.get_summary())
        ```
    """

    def __init__(
        self,
        log_assessments: bool = True,
        track_feedback: bool = True,
        verbose: bool = False,
    ) -> None:
        """
        Initialize SHIP callback handler.

        Args:
            log_assessments: Whether to log SHIP assessments
            track_feedback: Whether to auto-track for feedback
            verbose: Enable verbose logging
        """
        super().__init__()
        self.log_assessments = log_assessments
        self.track_feedback = track_feedback
        self.verbose = verbose

        # Tracking state
        self._assessments: List[Dict[str, Any]] = []
        self._feedbacks: List[Dict[str, Any]] = []
        self._current_run_id: Optional[str] = None
        self._tool_calls: List[Dict[str, Any]] = []

    @property
    def assessments(self) -> List[Dict[str, Any]]:
        """Get all recorded assessments."""
        return self._assessments.copy()

    @property
    def feedbacks(self) -> List[Dict[str, Any]]:
        """Get all recorded feedbacks."""
        return self._feedbacks.copy()

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Handle chain start."""
        self._current_run_id = str(run_id)
        if self.verbose:
            logger.info(f"SHIP: Chain started - {run_id}")

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Handle chain end."""
        if self.verbose:
            logger.info(f"SHIP: Chain ended - {run_id}")

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Handle tool start - track SHIP tool calls."""
        tool_name = serialized.get("name", "unknown")

        if tool_name.startswith("ship_"):
            self._tool_calls.append({
                "run_id": str(run_id),
                "tool": tool_name,
                "input": input_str,
                "status": "started",
            })

            if self.verbose:
                logger.info(f"SHIP: Tool {tool_name} started")

    def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Handle tool end - record SHIP results."""
        # Find matching tool call
        for call in self._tool_calls:
            if call["run_id"] == str(run_id) and call["status"] == "started":
                call["status"] = "completed"
                call["output"] = output

                # Parse SHIP assessment results
                if call["tool"] == "ship_assess" and self.log_assessments:
                    try:
                        # Output is a string repr of dict
                        import ast
                        result = ast.literal_eval(output)
                        if "ship_score" in result and result["ship_score"] is not None:
                            self._assessments.append({
                                "run_id": str(run_id),
                                "score": result["ship_score"],
                                "grade": result.get("grade"),
                                "request_id": result.get("request_id"),
                            })
                    except (ValueError, SyntaxError):
                        pass

                # Track feedback submissions
                if call["tool"] == "ship_feedback" and self.track_feedback:
                    try:
                        import ast
                        result = ast.literal_eval(output)
                        if result.get("status") == "success":
                            self._feedbacks.append({
                                "run_id": str(run_id),
                                "request_id": result.get("request_id"),
                            })
                    except (ValueError, SyntaxError):
                        pass

                break

        if self.verbose:
            logger.info(f"SHIP: Tool completed - {run_id}")

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Handle tool error - never fail the main execution."""
        for call in self._tool_calls:
            if call["run_id"] == str(run_id) and call["status"] == "started":
                call["status"] = "error"
                call["error"] = str(error)
                break

        # Log but don't raise - antifragile
        logger.warning(f"SHIP: Tool error (non-fatal) - {error}")

    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Handle agent action."""
        if self.verbose and action.tool.startswith("ship_"):
            logger.info(f"SHIP: Agent using {action.tool}")

    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Handle agent finish."""
        if self.verbose:
            logger.info("SHIP: Agent finished")

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of SHIP metrics from the run.

        Returns:
            Dict with assessment stats, scores, and feedback counts
        """
        scores = [a["score"] for a in self._assessments if a.get("score") is not None]

        return {
            "total_assessments": len(self._assessments),
            "total_feedbacks": len(self._feedbacks),
            "average_score": sum(scores) / len(scores) if scores else None,
            "min_score": min(scores) if scores else None,
            "max_score": max(scores) if scores else None,
            "assessments": self._assessments,
            "tool_calls": len(self._tool_calls),
        }

    def reset(self) -> None:
        """Reset tracking state for new run."""
        self._assessments = []
        self._feedbacks = []
        self._tool_calls = []
        self._current_run_id = None
