"""
SHIP Protocol LangChain Chains

Pre-built chains for common SHIP workflows.

Design Principles:
    - Composable: Works with any LLM and tool setup
    - Observable: Rich output for debugging
    - Antifragile: Graceful degradation on failures
"""

from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from vibeatlas_ship import (
    ShipClient,
    ShipClientConfig,
    FileInfo,
    Language,
    ShipError,
)


class AssessmentResult(BaseModel):
    """Result of SHIP assessment chain."""

    score: Optional[int] = Field(description="SHIP score 0-100")
    grade: Optional[str] = Field(description="Letter grade A+ to F")
    confidence: Optional[int] = Field(description="Confidence score")
    focus: Optional[int] = Field(description="Focus score")
    context: Optional[int] = Field(description="Context score")
    efficiency: Optional[int] = Field(description="Efficiency score")
    request_id: Optional[str] = Field(description="Request ID for feedback")
    recommendations: List[str] = Field(default_factory=list)
    success: bool = Field(description="Whether assessment succeeded")
    error: Optional[str] = Field(default=None)


class SHIPAssessmentChain:
    """
    Chain that assesses code and returns structured results.

    Usage:
        ```python
        chain = SHIPAssessmentChain()
        result = await chain.invoke({
            "code": "def hello(): print('world')",
            "prompt": "Add type hints",
        })
        print(f"Score: {result.score} ({result.grade})")
        ```
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://ship.vibeatlas.dev",
        timeout_seconds: float = 30.0,
    ) -> None:
        """Initialize assessment chain."""
        self.config = ShipClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
        )

    def _get_language(self, lang_str: str) -> Language:
        """Convert string to Language enum."""
        lang_map = {
            "python": Language.PYTHON,
            "typescript": Language.TYPESCRIPT,
            "javascript": Language.JAVASCRIPT,
            "go": Language.GO,
            "rust": Language.RUST,
        }
        return lang_map.get(lang_str.lower(), Language.OTHER)

    async def invoke(
        self,
        inputs: Dict[str, Any],
    ) -> AssessmentResult:
        """
        Run assessment chain.

        Args:
            inputs: Dict with 'code', 'prompt', optional 'language', 'file_path'

        Returns:
            AssessmentResult with score and recommendations
        """
        code = inputs.get("code", "")
        prompt = inputs.get("prompt", "")
        language = inputs.get("language", "python")
        file_path = inputs.get("file_path", "main.py")

        try:
            async with ShipClient(self.config) as client:
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

            return AssessmentResult(
                score=response.ship_score.score,
                grade=response.ship_score.grade.value,
                confidence=response.confidence.confidence_score,
                focus=response.focus.focus_score,
                context=response.context.context_score,
                efficiency=response.efficiency.efficiency_score,
                request_id=response.request_id,
                recommendations=[r.message for r in response.recommendations],
                success=True,
            )

        except ShipError as e:
            return AssessmentResult(
                score=None,
                grade=None,
                confidence=None,
                focus=None,
                context=None,
                efficiency=None,
                request_id=None,
                recommendations=[],
                success=False,
                error=str(e),
            )

    def invoke_sync(
        self,
        inputs: Dict[str, Any],
    ) -> AssessmentResult:
        """
        Run assessment chain synchronously.

        Args:
            inputs: Dict with 'code', 'prompt', optional 'language', 'file_path'

        Returns:
            AssessmentResult with score and recommendations
        """
        code = inputs.get("code", "")
        prompt = inputs.get("prompt", "")
        language = inputs.get("language", "python")
        file_path = inputs.get("file_path", "main.py")

        try:
            from vibeatlas_ship import SyncShipClient

            with SyncShipClient(self.config) as client:
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

            return AssessmentResult(
                score=response.ship_score.score,
                grade=response.ship_score.grade.value,
                confidence=response.confidence.confidence_score,
                focus=response.focus.focus_score,
                context=response.context.context_score,
                efficiency=response.efficiency.efficiency_score,
                request_id=response.request_id,
                recommendations=[r.message for r in response.recommendations],
                success=True,
            )

        except ShipError as e:
            return AssessmentResult(
                score=None,
                grade=None,
                confidence=None,
                focus=None,
                context=None,
                efficiency=None,
                request_id=None,
                recommendations=[],
                success=False,
                error=str(e),
            )

    def as_runnable(self):
        """
        Convert to LangChain Runnable for use in LCEL chains.

        Usage:
            ```python
            chain = SHIPAssessmentChain().as_runnable()
            result = chain.invoke({"code": "...", "prompt": "..."})
            ```
        """
        return RunnableLambda(self.invoke_sync)


def create_ship_chain(
    api_key: Optional[str] = None,
    base_url: str = "https://ship.vibeatlas.dev",
) -> SHIPAssessmentChain:
    """
    Factory function to create SHIP assessment chain.

    Args:
        api_key: Optional API key
        base_url: API base URL

    Returns:
        Configured SHIPAssessmentChain
    """
    return SHIPAssessmentChain(
        api_key=api_key,
        base_url=base_url,
    )


# Pre-built prompt template for code assessment
SHIP_ASSESSMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a code quality analyst using SHIP Protocol.
Assess the code reliability before modification.

SHIP Score interpretation:
- A+ (95-100): Exceptional, 95%+ success rate
- A (85-94): Reliable, 85-94% success rate
- B (70-84): Good, 70-84% success rate
- C (50-69): Fair, 50-69% success rate
- D (30-49): Poor, 30-49% success rate
- F (0-29): Unreliable, <30% success rate

Always check SHIP score before modifying code."""),
    ("human", """Assess this code:

```{language}
{code}
```

Task: {prompt}

Provide your analysis based on the SHIP score."""),
])
