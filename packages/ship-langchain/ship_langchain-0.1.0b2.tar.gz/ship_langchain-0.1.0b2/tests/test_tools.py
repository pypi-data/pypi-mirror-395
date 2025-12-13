"""Tests for SHIP LangChain tools."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from ship_langchain import (
    SHIPAssessTool,
    SHIPFeedbackTool,
    SHIPQuickAssessTool,
    SHIPHealthTool,
)
from ship_langchain.tools import AssessInput, FeedbackInput


class TestSHIPAssessTool:
    """Tests for SHIPAssessTool."""

    def test_tool_metadata(self):
        """Test tool has correct metadata."""
        tool = SHIPAssessTool()
        assert tool.name == "ship_assess"
        assert "SHIP" in tool.description
        assert "reliability" in tool.description.lower()

    def test_args_schema(self):
        """Test input schema is defined."""
        tool = SHIPAssessTool()
        assert tool.args_schema == AssessInput

    def test_language_mapping(self):
        """Test language string to enum conversion."""
        tool = SHIPAssessTool()
        from vibeatlas_ship import Language

        assert tool._get_language("python") == Language.PYTHON
        assert tool._get_language("py") == Language.PYTHON
        assert tool._get_language("typescript") == Language.TYPESCRIPT
        assert tool._get_language("ts") == Language.TYPESCRIPT
        assert tool._get_language("javascript") == Language.JAVASCRIPT
        assert tool._get_language("unknown") == Language.OTHER

    @patch("ship_langchain.tools.SyncShipClient")
    def test_run_success(self, mock_client_class):
        """Test successful assessment."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.ship_score.score = 85
        mock_response.ship_score.grade.value = "A"
        mock_response.confidence.confidence_score = 85
        mock_response.focus.focus_score = 85
        mock_response.context.context_score = 85
        mock_response.efficiency.efficiency_score = 85
        mock_response.request_id = "req-123"
        mock_response.recommendations = []

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.assess.return_value = mock_response
        mock_client_class.return_value = mock_client

        tool = SHIPAssessTool()
        result = tool._run(
            code="def hello(): print('world')",
            prompt="Add type hints",
            language="python",
        )

        assert "85" in result
        assert "A" in result
        assert "req-123" in result

    @patch("ship_langchain.tools.SyncShipClient")
    def test_run_error_returns_fallback(self, mock_client_class):
        """Test error returns fallback response instead of raising."""
        from vibeatlas_ship import ShipTimeoutError

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.assess.side_effect = ShipTimeoutError()
        mock_client_class.return_value = mock_client

        tool = SHIPAssessTool()
        result = tool._run(
            code="def hello(): print('world')",
            prompt="Add type hints",
        )

        # Should not raise, should return fallback
        assert "fallback" in result.lower() or "error" in result.lower()
        assert "UNKNOWN" in result


class TestSHIPFeedbackTool:
    """Tests for SHIPFeedbackTool."""

    def test_tool_metadata(self):
        """Test tool has correct metadata."""
        tool = SHIPFeedbackTool()
        assert tool.name == "ship_feedback"
        assert "feedback" in tool.description.lower()

    def test_args_schema(self):
        """Test input schema is defined."""
        tool = SHIPFeedbackTool()
        assert tool.args_schema == FeedbackInput

    @patch("ship_langchain.tools.SyncShipClient")
    def test_run_success(self, mock_client_class):
        """Test successful feedback submission."""
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.feedback.return_value = None
        mock_client_class.return_value = mock_client

        tool = SHIPFeedbackTool()
        result = tool._run(
            request_id="req-123",
            task_completed=True,
            first_attempt_success=True,
        )

        assert "success" in result.lower()
        assert "req-123" in result


class TestSHIPQuickAssessTool:
    """Tests for SHIPQuickAssessTool."""

    def test_tool_metadata(self):
        """Test tool has correct metadata."""
        tool = SHIPQuickAssessTool()
        assert tool.name == "ship_quick_assess"
        assert "quick" in tool.description.lower()

    @patch("ship_langchain.tools.SyncShipClient")
    def test_run_returns_simple_format(self, mock_client_class):
        """Test quick assess returns simple format."""
        mock_response = MagicMock()
        mock_response.ship_score.score = 85
        mock_response.ship_score.grade.value = "A"

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.quick_assess.return_value = mock_response
        mock_client_class.return_value = mock_client

        tool = SHIPQuickAssessTool()
        result = tool._run(
            code="def hello(): pass",
            prompt="Add docstring",
        )

        assert "SHIP Score:" in result
        assert "85" in result
        assert "A" in result


class TestSHIPHealthTool:
    """Tests for SHIPHealthTool."""

    def test_tool_metadata(self):
        """Test tool has correct metadata."""
        tool = SHIPHealthTool()
        assert tool.name == "ship_health"
        assert "health" in tool.description.lower()

    @patch("ship_langchain.tools.SyncShipClient")
    def test_run_healthy(self, mock_client_class):
        """Test health check when API is healthy."""
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.health.return_value = {"version": "1.0", "status": "ok"}
        mock_client_class.return_value = mock_client

        tool = SHIPHealthTool()
        result = tool._run()

        assert "healthy" in result.lower()

    @patch("ship_langchain.tools.SyncShipClient")
    def test_run_unhealthy(self, mock_client_class):
        """Test health check when API is unavailable."""
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.health.side_effect = Exception("Connection refused")
        mock_client_class.return_value = mock_client

        tool = SHIPHealthTool()
        result = tool._run()

        assert "unhealthy" in result.lower()


class TestInputSchemas:
    """Tests for input schemas."""

    def test_assess_input_defaults(self):
        """Test AssessInput has correct defaults."""
        input_data = AssessInput(
            code="def test(): pass",
            prompt="Test prompt",
        )
        assert input_data.language == "python"
        assert input_data.file_path == "main.py"

    def test_feedback_input_defaults(self):
        """Test FeedbackInput has correct defaults."""
        input_data = FeedbackInput(
            request_id="req-123",
            task_completed=True,
        )
        assert input_data.first_attempt_success is True
        assert input_data.total_attempts == 1
        assert input_data.user_satisfaction == 5
