"""Tests for SHIP LangChain callback handler."""

import pytest
from uuid import uuid4

from ship_langchain import SHIPCallbackHandler


class TestSHIPCallbackHandler:
    """Tests for SHIPCallbackHandler."""

    def test_initialization(self):
        """Test handler initializes with correct defaults."""
        handler = SHIPCallbackHandler()
        assert handler.log_assessments is True
        assert handler.track_feedback is True
        assert handler.verbose is False
        assert handler.assessments == []
        assert handler.feedbacks == []

    def test_custom_initialization(self):
        """Test handler with custom settings."""
        handler = SHIPCallbackHandler(
            log_assessments=False,
            track_feedback=False,
            verbose=True,
        )
        assert handler.log_assessments is False
        assert handler.track_feedback is False
        assert handler.verbose is True

    def test_on_chain_start(self):
        """Test chain start callback."""
        handler = SHIPCallbackHandler()
        run_id = uuid4()

        handler.on_chain_start(
            serialized={},
            inputs={},
            run_id=run_id,
        )

        assert handler._current_run_id == str(run_id)

    def test_on_tool_start_tracks_ship_tools(self):
        """Test that SHIP tool starts are tracked."""
        handler = SHIPCallbackHandler()
        run_id = uuid4()

        handler.on_tool_start(
            serialized={"name": "ship_assess"},
            input_str='{"code": "test", "prompt": "test"}',
            run_id=run_id,
        )

        assert len(handler._tool_calls) == 1
        assert handler._tool_calls[0]["tool"] == "ship_assess"
        assert handler._tool_calls[0]["status"] == "started"

    def test_on_tool_start_ignores_non_ship_tools(self):
        """Test that non-SHIP tools are ignored."""
        handler = SHIPCallbackHandler()
        run_id = uuid4()

        handler.on_tool_start(
            serialized={"name": "calculator"},
            input_str="2 + 2",
            run_id=run_id,
        )

        assert len(handler._tool_calls) == 0

    def test_on_tool_end_records_assessment(self):
        """Test assessment results are recorded."""
        handler = SHIPCallbackHandler()
        run_id = uuid4()

        # Start tool
        handler.on_tool_start(
            serialized={"name": "ship_assess"},
            input_str='{}',
            run_id=run_id,
        )

        # End with result
        output = "{'ship_score': 85, 'grade': 'A', 'request_id': 'req-123'}"
        handler.on_tool_end(output=output, run_id=run_id)

        assert len(handler._assessments) == 1
        assert handler._assessments[0]["score"] == 85
        assert handler._assessments[0]["grade"] == "A"

    def test_on_tool_end_records_feedback(self):
        """Test feedback submissions are recorded."""
        handler = SHIPCallbackHandler()
        run_id = uuid4()

        # Start feedback tool
        handler.on_tool_start(
            serialized={"name": "ship_feedback"},
            input_str='{}',
            run_id=run_id,
        )

        # End with success
        output = "{'status': 'success', 'request_id': 'req-123'}"
        handler.on_tool_end(output=output, run_id=run_id)

        assert len(handler._feedbacks) == 1
        assert handler._feedbacks[0]["request_id"] == "req-123"

    def test_on_tool_error_handles_gracefully(self):
        """Test tool errors don't crash handler."""
        handler = SHIPCallbackHandler()
        run_id = uuid4()

        # Start tool
        handler.on_tool_start(
            serialized={"name": "ship_assess"},
            input_str='{}',
            run_id=run_id,
        )

        # Error
        handler.on_tool_error(
            error=Exception("Test error"),
            run_id=run_id,
        )

        # Should mark as error, not crash
        assert handler._tool_calls[0]["status"] == "error"
        assert "Test error" in handler._tool_calls[0]["error"]

    def test_get_summary(self):
        """Test summary generation."""
        handler = SHIPCallbackHandler()

        # Add some assessments
        handler._assessments = [
            {"run_id": "1", "score": 80, "grade": "A"},
            {"run_id": "2", "score": 70, "grade": "B"},
            {"run_id": "3", "score": 90, "grade": "A"},
        ]
        handler._feedbacks = [{"run_id": "1", "request_id": "req-1"}]
        handler._tool_calls = [{"tool": "ship_assess"}] * 4

        summary = handler.get_summary()

        assert summary["total_assessments"] == 3
        assert summary["total_feedbacks"] == 1
        assert summary["average_score"] == 80.0
        assert summary["min_score"] == 70
        assert summary["max_score"] == 90
        assert summary["tool_calls"] == 4

    def test_get_summary_empty(self):
        """Test summary with no data."""
        handler = SHIPCallbackHandler()
        summary = handler.get_summary()

        assert summary["total_assessments"] == 0
        assert summary["average_score"] is None
        assert summary["min_score"] is None

    def test_reset(self):
        """Test handler reset."""
        handler = SHIPCallbackHandler()

        # Add some data
        handler._assessments = [{"score": 85}]
        handler._feedbacks = [{"request_id": "test"}]
        handler._tool_calls = [{"tool": "test"}]
        handler._current_run_id = "test-run"

        # Reset
        handler.reset()

        assert handler._assessments == []
        assert handler._feedbacks == []
        assert handler._tool_calls == []
        assert handler._current_run_id is None

    def test_assessments_returns_copy(self):
        """Test assessments property returns copy."""
        handler = SHIPCallbackHandler()
        handler._assessments = [{"score": 85}]

        assessments = handler.assessments
        assessments.append({"score": 90})

        # Original should be unchanged
        assert len(handler._assessments) == 1

    def test_feedbacks_returns_copy(self):
        """Test feedbacks property returns copy."""
        handler = SHIPCallbackHandler()
        handler._feedbacks = [{"request_id": "test"}]

        feedbacks = handler.feedbacks
        feedbacks.append({"request_id": "new"})

        # Original should be unchanged
        assert len(handler._feedbacks) == 1
