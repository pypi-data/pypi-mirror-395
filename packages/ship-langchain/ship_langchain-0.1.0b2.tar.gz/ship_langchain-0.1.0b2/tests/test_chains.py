"""Tests for SHIP LangChain chains."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from ship_langchain import SHIPAssessmentChain, create_ship_chain
from ship_langchain.chains import AssessmentResult


class TestAssessmentResult:
    """Tests for AssessmentResult model."""

    def test_successful_result(self):
        """Test creating successful assessment result."""
        result = AssessmentResult(
            score=85,
            grade="A",
            confidence=85,
            focus=85,
            context=85,
            efficiency=85,
            request_id="req-123",
            recommendations=["Add type hints"],
            success=True,
        )

        assert result.score == 85
        assert result.grade == "A"
        assert result.success is True
        assert result.error is None

    def test_failed_result(self):
        """Test creating failed assessment result."""
        result = AssessmentResult(
            score=None,
            grade=None,
            confidence=None,
            focus=None,
            context=None,
            efficiency=None,
            request_id=None,
            recommendations=[],
            success=False,
            error="Connection timeout",
        )

        assert result.success is False
        assert result.error == "Connection timeout"
        assert result.score is None


class TestSHIPAssessmentChain:
    """Tests for SHIPAssessmentChain."""

    def test_initialization(self):
        """Test chain initialization."""
        chain = SHIPAssessmentChain(
            api_key="test_key",
            base_url="https://test.api.com",
            timeout_seconds=60.0,
        )

        assert chain.config.api_key == "test_key"
        assert chain.config.base_url == "https://test.api.com"
        assert chain.config.timeout_seconds == 60.0

    def test_language_mapping(self):
        """Test language string to enum conversion."""
        chain = SHIPAssessmentChain()
        from vibeatlas_ship import Language

        assert chain._get_language("python") == Language.PYTHON
        assert chain._get_language("typescript") == Language.TYPESCRIPT
        assert chain._get_language("unknown") == Language.OTHER

    @patch("ship_langchain.chains.SyncShipClient")
    def test_invoke_sync_success(self, mock_client_class):
        """Test successful synchronous invocation."""
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

        chain = SHIPAssessmentChain()
        result = chain.invoke_sync({
            "code": "def hello(): pass",
            "prompt": "Add docstring",
        })

        assert result.success is True
        assert result.score == 85
        assert result.grade == "A"
        assert result.request_id == "req-123"

    @patch("ship_langchain.chains.SyncShipClient")
    def test_invoke_sync_error(self, mock_client_class):
        """Test synchronous invocation with error."""
        from vibeatlas_ship import ShipTimeoutError

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.assess.side_effect = ShipTimeoutError("Timeout")
        mock_client_class.return_value = mock_client

        chain = SHIPAssessmentChain()
        result = chain.invoke_sync({
            "code": "def hello(): pass",
            "prompt": "Add docstring",
        })

        assert result.success is False
        assert result.error is not None
        assert result.score is None

    def test_as_runnable(self):
        """Test conversion to LangChain Runnable."""
        chain = SHIPAssessmentChain()
        runnable = chain.as_runnable()

        # Should be callable
        assert callable(runnable.invoke)


class TestCreateShipChain:
    """Tests for create_ship_chain factory."""

    def test_creates_chain_with_defaults(self):
        """Test factory creates chain with defaults."""
        chain = create_ship_chain()

        assert isinstance(chain, SHIPAssessmentChain)
        assert chain.config.base_url == "https://ship.vibeatlas.dev"

    def test_creates_chain_with_custom_config(self):
        """Test factory creates chain with custom config."""
        chain = create_ship_chain(
            api_key="test_key",
            base_url="https://custom.api.com",
        )

        assert chain.config.api_key == "test_key"
        assert chain.config.base_url == "https://custom.api.com"
