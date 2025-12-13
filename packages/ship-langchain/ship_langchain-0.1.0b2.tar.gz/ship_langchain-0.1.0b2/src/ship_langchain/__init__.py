"""
SHIP Protocol LangChain Integration

Provides LangChain tools for assessing AI coding task reliability.

Usage:
    ```python
    from ship_langchain import SHIPAssessTool, SHIPFeedbackTool
    from langchain.agents import AgentExecutor

    # Add to your agent's toolkit
    tools = [SHIPAssessTool(), SHIPFeedbackTool()]
    ```

Philosophy:
    - Antifragile: Graceful degradation when API unavailable
    - Self-learning: Feedback loop improves predictions
    - Observable: Rich metadata in tool outputs
"""

from .tools import (
    SHIPAssessTool,
    SHIPFeedbackTool,
    SHIPQuickAssessTool,
    SHIPHealthTool,
)
from .callbacks import SHIPCallbackHandler
from .chains import (
    SHIPAssessmentChain,
    create_ship_chain,
)

__version__ = "0.1.0-beta"
__all__ = [
    "__version__",
    # Tools
    "SHIPAssessTool",
    "SHIPFeedbackTool",
    "SHIPQuickAssessTool",
    "SHIPHealthTool",
    # Callbacks
    "SHIPCallbackHandler",
    # Chains
    "SHIPAssessmentChain",
    "create_ship_chain",
]
