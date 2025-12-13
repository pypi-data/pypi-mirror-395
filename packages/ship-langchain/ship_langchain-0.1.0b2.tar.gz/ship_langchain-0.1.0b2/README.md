# ship-langchain

[![SHIP Score](https://img.shields.io/badge/SHIP_Score-85%20(A)-green?style=flat)](https://ship.vibeatlas.dev)
[![PyPI version](https://img.shields.io/pypi/v/ship-langchain.svg)](https://pypi.org/project/ship-langchain/)
[![Python Version](https://img.shields.io/pypi/pyversions/ship-langchain.svg)](https://pypi.org/project/ship-langchain/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**LangChain Integration for SHIP Protocol** - AI Coding Reliability Tools

> Know if your AI coding task will succeed before you run it.

## Why SHIP + LangChain?

**70% of AI coding tasks fail.** SHIP tells your agent the probability of success *before* execution.

```python
from ship_langchain import SHIPAssessTool
from langchain.agents import create_react_agent

# Add SHIP assessment to your agent's toolkit
tools = [SHIPAssessTool(), ...other_tools]

# Now your agent can check reliability before modifying code
# Agent: "Let me assess this task first..."
# SHIP: "Score: 85 (A) - High confidence this will work"
```

## Installation

```bash
pip install ship-langchain
```

## Quick Start

### As a Tool

```python
from ship_langchain import SHIPAssessTool, SHIPFeedbackTool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

# Create tools
ship_assess = SHIPAssessTool()
ship_feedback = SHIPFeedbackTool()

# Add to your agent
tools = [ship_assess, ship_feedback]

# The agent can now:
# 1. Assess code before modification
# 2. Submit feedback after task completion
```

### As a Chain

```python
from ship_langchain import SHIPAssessmentChain

chain = SHIPAssessmentChain()

result = await chain.invoke({
    "code": "def hello(): print('world')",
    "prompt": "Add type hints and docstring",
    "language": "python",
})

print(f"Score: {result.score} ({result.grade})")
print(f"Confidence: {result.confidence}")
print(f"Recommendations: {result.recommendations}")
```

### With Callbacks

```python
from ship_langchain import SHIPCallbackHandler

# Track all SHIP metrics automatically
handler = SHIPCallbackHandler()

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[handler],
)

# Run your agent
result = agent_executor.invoke({"input": "Refactor this code..."})

# Get SHIP summary
summary = handler.get_summary()
print(f"Average SHIP Score: {summary['average_score']}")
print(f"Assessments: {summary['total_assessments']}")
```

## Tools Reference

### SHIPAssessTool

Assess code reliability before AI modification.

**Input:**
- `code`: The code to assess
- `prompt`: Task description
- `language`: Programming language (default: "python")
- `file_path`: Virtual file path (default: "main.py")

**Output:**
- `ship_score`: 0-100 reliability score
- `grade`: Letter grade (A+ to F)
- `confidence`, `focus`, `context`, `efficiency`: Component scores
- `recommendations`: Top improvement suggestions

### SHIPFeedbackTool

Submit feedback on task outcomes to improve future predictions.

**Input:**
- `request_id`: From assessment response
- `task_completed`: Whether task succeeded
- `first_attempt_success`: Success on first try
- `total_attempts`: Number of attempts needed

### SHIPQuickAssessTool

Fast assessment with minimal input.

**Input:**
- `code`: Code snippet
- `prompt`: Task description

**Output:**
- Simple "SHIP Score: X (Grade)" string

### SHIPHealthTool

Check API availability before batch operations.

## Philosophy

This integration follows **Talebian/Antifragile** principles:

1. **Never Crash**: Tools return degraded responses instead of exceptions
2. **Self-Learning**: Feedback loop improves predictions over time
3. **Observable**: Callback handler tracks all metrics
4. **Composable**: Works with any LLM and agent setup

## Grade Interpretation

| Grade | Score | What It Means |
|-------|-------|---------------|
| A+ | 95-100 | 95%+ success rate - Ship with confidence |
| A | 85-94 | 85%+ success rate - Reliable |
| B | 70-84 | 70%+ success rate - Good, minor risks |
| C | 50-69 | 50%+ success rate - Proceed with caution |
| D | 30-49 | 30%+ success rate - High risk |
| F | 0-29 | <30% success rate - Likely to fail |

## Example Agent Workflow

```python
# 1. Agent receives coding task
"Add error handling to the payment processor"

# 2. Agent uses SHIPAssessTool first
ship_assess.run({
    "code": payment_processor_code,
    "prompt": "Add error handling",
})
# Result: Score 72 (B) - "Missing type information reduces confidence"

# 3. Agent decides based on score
if score >= 70:
    # Proceed with modification
    ...
else:
    # Request more context or simplify task
    ...

# 4. After completion, agent submits feedback
ship_feedback.run({
    "request_id": "req-123",
    "task_completed": True,
    "first_attempt_success": True,
})
```

## Links

- **SHIP Protocol**: https://vibeatlas.dev/docs/ship
- **PyPI Package**: https://pypi.org/project/vibeatlas-ship/
- **GitHub**: https://github.com/vibeatlas/ship-protocol

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with love by [VibeAtlas](https://vibeatlas.dev) - Making AI coding reliable.
