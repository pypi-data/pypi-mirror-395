"""
SHIP Protocol LangChain Tools

Provides tools for AI agents to assess coding task reliability.

Design Principles:
    - Talebian/Antifragile: Never crash, always return useful info
    - Self-Learning: Every assessment feeds the improvement loop
    - Modular: Each tool is independent and composable
"""

from typing import Any, Optional, Type
from pydantic import BaseModel, Field

from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun

from vibeatlas_ship import (
    ShipClient,
    ShipClientConfig,
    FileInfo,
    Language,
    TaskOutcome,
    ShipError,
)


class AssessInput(BaseModel):
    """Input schema for SHIP assessment."""

    code: str = Field(description="The code to assess")
    prompt: str = Field(description="The task/prompt describing what to do with the code")
    language: str = Field(
        default="python",
        description="Programming language (python, typescript, javascript, go, rust, etc.)",
    )
    file_path: str = Field(
        default="main.py",
        description="Virtual file path for context",
    )


class FeedbackInput(BaseModel):
    """Input schema for SHIP feedback."""

    request_id: str = Field(description="The request_id from the assessment response")
    task_completed: bool = Field(description="Whether the task was completed successfully")
    first_attempt_success: bool = Field(
        default=True,
        description="Whether it succeeded on first attempt",
    )
    total_attempts: int = Field(
        default=1,
        description="Total number of attempts needed",
    )
    user_satisfaction: int = Field(
        default=5,
        description="User satisfaction score 1-5",
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional notes about the outcome",
    )


class QuickAssessInput(BaseModel):
    """Input schema for quick SHIP assessment."""

    code: str = Field(description="The code snippet to assess")
    prompt: str = Field(description="The task description")


class SHIPAssessTool(BaseTool):
    """
    Assess code reliability before AI modification.

    Returns a SHIP Score (0-100) predicting success probability.
    Use this before asking an AI to modify code to know if it will work.

    Example:
        score = ship_assess.run({
            "code": "def hello(): print('world')",
            "prompt": "Add type hints",
            "language": "python"
        })
    """

    name: str = "ship_assess"
    description: str = (
        "Assess code reliability before AI modification. "
        "Returns SHIP Score (0-100) predicting task success probability. "
        "Input: code, prompt, language. Output: score, grade, recommendations."
    )
    args_schema: Type[BaseModel] = AssessInput

    # Client configuration
    api_key: Optional[str] = None
    base_url: str = "https://ship.vibeatlas.dev"
    timeout_seconds: float = 30.0

    def _get_language(self, lang_str: str) -> Language:
        """Convert string to Language enum."""
        lang_map = {
            "python": Language.PYTHON,
            "py": Language.PYTHON,
            "typescript": Language.TYPESCRIPT,
            "ts": Language.TYPESCRIPT,
            "javascript": Language.JAVASCRIPT,
            "js": Language.JAVASCRIPT,
            "go": Language.GO,
            "golang": Language.GO,
            "rust": Language.RUST,
            "rs": Language.RUST,
            "java": Language.JAVA,
            "kotlin": Language.KOTLIN,
            "kt": Language.KOTLIN,
            "swift": Language.SWIFT,
            "csharp": Language.CSHARP,
            "cs": Language.CSHARP,
            "c#": Language.CSHARP,
            "cpp": Language.CPP,
            "c++": Language.CPP,
            "c": Language.CPP,  # C maps to CPP (closely related)
            "ruby": Language.RUBY,
            "rb": Language.RUBY,
            "php": Language.PHP,
        }
        return lang_map.get(lang_str.lower(), Language.OTHER)

    def _run(
        self,
        code: str,
        prompt: str,
        language: str = "python",
        file_path: str = "main.py",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Run SHIP assessment synchronously."""
        try:
            config = ShipClientConfig(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout_seconds=self.timeout_seconds,
            )

            from vibeatlas_ship import SyncShipClient

            with SyncShipClient(config) as client:
                response = client.assess(
                    files=[
                        FileInfo(
                            path=file_path,
                            content=code,
                            language=self._get_language(language),
                        )
                    ],
                    prompt=prompt,
                )

            # Format response for agent consumption
            result = {
                "ship_score": response.ship_score.score,
                "grade": response.ship_score.grade.value,
                "confidence": response.confidence.confidence_score,
                "focus": response.focus.focus_score,
                "context": response.context.context_score,
                "efficiency": response.efficiency.efficiency_score,
                "request_id": response.request_id,
                "recommendations": [
                    {"type": r.type, "message": r.message}
                    for r in response.recommendations[:3]  # Top 3
                ],
            }

            return str(result)

        except ShipError as e:
            # Antifragile: Return degraded response instead of failing
            return str({
                "error": str(e),
                "ship_score": None,
                "grade": "UNKNOWN",
                "fallback": True,
                "message": "Assessment unavailable, proceed with caution",
            })

    async def _arun(
        self,
        code: str,
        prompt: str,
        language: str = "python",
        file_path: str = "main.py",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Run SHIP assessment asynchronously."""
        try:
            config = ShipClientConfig(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout_seconds=self.timeout_seconds,
            )

            async with ShipClient(config) as client:
                response = await client.assess(
                    files=[
                        FileInfo(
                            path=file_path,
                            content=code,
                            language=self._get_language(language),
                        )
                    ],
                    prompt=prompt,
                )

            result = {
                "ship_score": response.ship_score.score,
                "grade": response.ship_score.grade.value,
                "confidence": response.confidence.confidence_score,
                "focus": response.focus.focus_score,
                "context": response.context.context_score,
                "efficiency": response.efficiency.efficiency_score,
                "request_id": response.request_id,
                "recommendations": [
                    {"type": r.type, "message": r.message}
                    for r in response.recommendations[:3]
                ],
            }

            return str(result)

        except ShipError as e:
            return str({
                "error": str(e),
                "ship_score": None,
                "grade": "UNKNOWN",
                "fallback": True,
                "message": "Assessment unavailable, proceed with caution",
            })


class SHIPFeedbackTool(BaseTool):
    """
    Submit feedback on task outcome.

    This feeds the self-learning loop to improve future predictions.
    Always submit feedback after completing AI coding tasks.

    Example:
        ship_feedback.run({
            "request_id": "req-123",
            "task_completed": True,
            "first_attempt_success": True
        })
    """

    name: str = "ship_feedback"
    description: str = (
        "Submit feedback on AI coding task outcome. "
        "Improves future predictions through self-learning. "
        "Input: request_id, task_completed, attempts. Output: confirmation."
    )
    args_schema: Type[BaseModel] = FeedbackInput

    api_key: Optional[str] = None
    base_url: str = "https://ship.vibeatlas.dev"
    timeout_seconds: float = 30.0

    def _run(
        self,
        request_id: str,
        task_completed: bool,
        first_attempt_success: bool = True,
        total_attempts: int = 1,
        user_satisfaction: int = 5,
        notes: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Submit feedback synchronously."""
        try:
            config = ShipClientConfig(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout_seconds=self.timeout_seconds,
            )

            from vibeatlas_ship import SyncShipClient

            with SyncShipClient(config) as client:
                client.feedback(
                    request_id=request_id,
                    outcome=TaskOutcome(
                        task_completed=task_completed,
                        first_attempt_success=first_attempt_success,
                        total_attempts=total_attempts,
                        user_satisfaction=user_satisfaction,
                        notes=notes,
                    ),
                )

            return str({
                "status": "success",
                "message": "Feedback submitted, thank you for improving SHIP!",
                "request_id": request_id,
            })

        except ShipError as e:
            return str({
                "status": "error",
                "error": str(e),
                "message": "Feedback submission failed, but your task continues",
            })

    async def _arun(
        self,
        request_id: str,
        task_completed: bool,
        first_attempt_success: bool = True,
        total_attempts: int = 1,
        user_satisfaction: int = 5,
        notes: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Submit feedback asynchronously."""
        try:
            config = ShipClientConfig(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout_seconds=self.timeout_seconds,
            )

            async with ShipClient(config) as client:
                await client.feedback(
                    request_id=request_id,
                    outcome=TaskOutcome(
                        task_completed=task_completed,
                        first_attempt_success=first_attempt_success,
                        total_attempts=total_attempts,
                        user_satisfaction=user_satisfaction,
                        notes=notes,
                    ),
                )

            return str({
                "status": "success",
                "message": "Feedback submitted, thank you for improving SHIP!",
                "request_id": request_id,
            })

        except ShipError as e:
            return str({
                "status": "error",
                "error": str(e),
                "message": "Feedback submission failed, but your task continues",
            })


class SHIPQuickAssessTool(BaseTool):
    """
    Quick code assessment with minimal input.

    Simplified version of SHIPAssessTool for fast checks.
    Auto-detects language from code patterns.
    """

    name: str = "ship_quick_assess"
    description: str = (
        "Quick SHIP score check. Input: code and prompt. "
        "Returns score/grade. Use for fast reliability checks."
    )
    args_schema: Type[BaseModel] = QuickAssessInput

    api_key: Optional[str] = None
    base_url: str = "https://ship.vibeatlas.dev"

    def _run(
        self,
        code: str,
        prompt: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Quick assessment."""
        try:
            from vibeatlas_ship import SyncShipClient

            with SyncShipClient() as client:
                response = client.quick_assess(
                    code=code,
                    prompt=prompt,
                    language=Language.PYTHON,  # Default, auto-detect in future
                )

            return f"SHIP Score: {response.ship_score.score} ({response.ship_score.grade.value})"

        except ShipError as e:
            return f"Assessment unavailable: {e}"

    async def _arun(
        self,
        code: str,
        prompt: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Quick assessment async."""
        try:
            async with ShipClient() as client:
                response = await client.quick_assess(
                    code=code,
                    prompt=prompt,
                    language=Language.PYTHON,
                )

            return f"SHIP Score: {response.ship_score.score} ({response.ship_score.grade.value})"

        except ShipError as e:
            return f"Assessment unavailable: {e}"


class SHIPHealthTool(BaseTool):
    """
    Check SHIP API health status.

    Use before batch operations to verify API availability.
    """

    name: str = "ship_health"
    description: str = "Check SHIP API availability. Returns health status."

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Check health sync."""
        try:
            from vibeatlas_ship import SyncShipClient

            with SyncShipClient() as client:
                health = client.health()

            return str({
                "status": "healthy",
                "version": health.get("version", "unknown"),
                "message": "SHIP API is available",
            })

        except Exception as e:
            return str({
                "status": "unhealthy",
                "error": str(e),
                "message": "SHIP API unavailable, assessments will use fallback mode",
            })

    async def _arun(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Check health async."""
        try:
            async with ShipClient() as client:
                health = await client.health()

            return str({
                "status": "healthy",
                "version": health.get("version", "unknown"),
                "message": "SHIP API is available",
            })

        except Exception as e:
            return str({
                "status": "unhealthy",
                "error": str(e),
                "message": "SHIP API unavailable, assessments will use fallback mode",
            })
