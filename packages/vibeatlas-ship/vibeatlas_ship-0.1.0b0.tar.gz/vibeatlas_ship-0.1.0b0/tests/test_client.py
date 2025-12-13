"""Tests for SHIP Protocol client."""

import pytest
import httpx
import respx
from unittest.mock import AsyncMock, patch

from vibeatlas_ship.client import (
    ShipClient,
    ShipClientConfig,
    CircuitBreaker,
    CircuitState,
    RetryPolicy,
    create_client,
)
from vibeatlas_ship.types import FileInfo, Language, ShipGrade
from vibeatlas_ship.exceptions import (
    CircuitBreakerOpenError,
    ShipTimeoutError,
    ShipRateLimitError,
)


class TestCircuitBreaker:
    """Tests for CircuitBreaker."""

    def test_initial_state_closed(self):
        """Test circuit breaker starts closed."""
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED

    def test_opens_after_threshold(self):
        """Test circuit breaker opens after failure threshold."""
        cb = CircuitBreaker(failure_threshold=3, failure_window_seconds=60)

        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED

        cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_success_resets_in_half_open(self):
        """Test success in half-open state closes circuit."""
        cb = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout_seconds=0,  # Immediate recovery for testing
        )

        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        # Should transition to half-open immediately
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        assert cb.state == CircuitState.CLOSED

    def test_allow_request_when_closed(self):
        """Test requests allowed when closed."""
        cb = CircuitBreaker()
        assert cb.allow_request() is True

    def test_deny_request_when_open(self):
        """Test requests denied when open."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout_seconds=60)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        assert cb.allow_request() is False


class TestRetryPolicy:
    """Tests for RetryPolicy."""

    def test_exponential_backoff(self):
        """Test exponential backoff calculation."""
        policy = RetryPolicy(
            base_delay_ms=1000,
            exponential_base=2.0,
            jitter=False,
        )

        assert policy.get_delay_ms(0) == 1000
        assert policy.get_delay_ms(1) == 2000
        assert policy.get_delay_ms(2) == 4000

    def test_max_delay_cap(self):
        """Test delay is capped at max."""
        policy = RetryPolicy(
            base_delay_ms=1000,
            max_delay_ms=5000,
            exponential_base=2.0,
            jitter=False,
        )

        assert policy.get_delay_ms(10) == 5000

    def test_should_retry_on_timeout(self):
        """Test retry on timeout errors."""
        policy = RetryPolicy(max_retries=3)
        error = ShipTimeoutError()
        assert policy.should_retry(0, error) is True
        assert policy.should_retry(2, error) is True
        assert policy.should_retry(3, error) is False

    def test_should_not_retry_exhausted(self):
        """Test no retry after max attempts."""
        policy = RetryPolicy(max_retries=2)
        error = ShipTimeoutError()
        assert policy.should_retry(2, error) is False


class TestShipClientConfig:
    """Tests for ShipClientConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ShipClientConfig()
        assert config.base_url == "https://ship.vibeatlas.dev"
        assert config.api_key is None
        assert config.timeout_seconds == 30.0
        assert config.enable_caching is True

    def test_custom_config(self):
        """Test custom configuration."""
        config = ShipClientConfig(
            api_key="test_key",
            base_url="https://custom.api.com",
            timeout_seconds=60.0,
        )
        assert config.api_key == "test_key"
        assert config.base_url == "https://custom.api.com"
        assert config.timeout_seconds == 60.0


class TestShipClient:
    """Tests for ShipClient."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        config = ShipClientConfig(base_url="https://test.api.com")
        return ShipClient(config)

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with ShipClient() as client:
            assert client._http_client is None or isinstance(
                client._http_client, httpx.AsyncClient
            )

    @pytest.mark.asyncio
    @respx.mock
    async def test_assess_success(self):
        """Test successful assessment."""
        mock_response = {
            "ship_version": "1.0",
            "message_type": "ShipResponse",
            "message_id": "test-msg-id",
            "request_id": "test-req-id",
            "timestamp": "2025-01-01T00:00:00Z",
            "ship_score": {
                "score": 85,
                "grade": "A",
                "confidence_component": 34.0,
                "focus_component": 25.5,
                "context_component": 17.0,
                "efficiency_component": 8.5,
                "layer_scores": {
                    "confidence": 85,
                    "focus": 85,
                    "context": 85,
                    "efficiency": 85,
                },
            },
            "confidence": {
                "task_completion_probability": 0.85,
                "confidence_level": "high",
                "confidence_score": 85,
                "risk_factors": [],
                "success_patterns": [],
                "historical_success_rate": 0.8,
                "recommended_retry_strategy": "incremental",
                "similar_tasks_count": 100,
            },
            "focus": {
                "focus_score": 85,
                "primary_context": [],
                "semantic_coverage": {
                    "anchors_found": [],
                    "anchors_missing": [],
                    "coverage_percentage": 85,
                },
                "focus_distribution": {},
                "distractions_filtered": 0,
                "focus_efficiency": 0.85,
            },
            "context": {
                "context_score": 85,
                "original_tokens": 1000,
                "optimized_tokens": 800,
                "reduction_percentage": 20,
                "relevance_distribution": {"high": 5, "medium": 3, "low": 2},
            },
            "efficiency": {
                "efficiency_score": 85,
                "tokens_saved": 200,
                "percentage_saved": 20,
                "cost_saved_usd": 0.002,
                "co2_saved_grams": 0.1,
                "processing_time_ms": 150,
            },
            "optimized_context": {
                "files": [],
                "total_tokens": 800,
                "excluded_files_count": 2,
                "context_coverage": 85,
            },
            "recommendations": [],
        }

        respx.post("https://test.api.com/v1/ship/assess").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        config = ShipClientConfig(base_url="https://test.api.com")
        async with ShipClient(config) as client:
            response = await client.assess(
                files=[
                    FileInfo(
                        path="test.py",
                        content="print('hello')",
                        language=Language.PYTHON,
                    )
                ],
                prompt="Add type hints",
            )

            assert response.ship_score.score == 85
            assert response.ship_score.grade == ShipGrade.A

    @pytest.mark.asyncio
    async def test_circuit_breaker_blocks_requests(self):
        """Test circuit breaker blocks requests when open."""
        config = ShipClientConfig()
        config.circuit_breaker = CircuitBreaker(
            failure_threshold=1,
            recovery_timeout_seconds=60,
        )

        client = ShipClient(config)
        # Force circuit open
        client.config.circuit_breaker.record_failure()

        with pytest.raises(CircuitBreakerOpenError):
            await client.assess(
                files=[FileInfo(path="test.py", content="x", language=Language.PYTHON)],
                prompt="Test",
            )

    def test_detect_language(self):
        """Test language detection from file extension."""
        client = ShipClient()
        assert client._detect_language(".py") == Language.PYTHON
        assert client._detect_language(".ts") == Language.TYPESCRIPT
        assert client._detect_language(".js") == Language.JAVASCRIPT
        assert client._detect_language(".go") == Language.GO
        assert client._detect_language(".rs") == Language.RUST
        assert client._detect_language(".unknown") == Language.OTHER

    def test_client_metrics(self):
        """Test client metrics tracking."""
        client = ShipClient()
        metrics = client.get_client_metrics()

        assert "request_count" in metrics
        assert "success_count" in metrics
        assert "failure_count" in metrics
        assert "success_rate" in metrics
        assert "circuit_breaker_state" in metrics


class TestCreateClient:
    """Tests for create_client factory."""

    def test_create_with_defaults(self):
        """Test creating client with defaults."""
        client = create_client()
        assert client.config.base_url == "https://ship.vibeatlas.dev"
        assert client.config.api_key is None

    def test_create_with_api_key(self):
        """Test creating client with API key."""
        client = create_client(api_key="test_key")
        assert client.config.api_key == "test_key"

    def test_create_with_custom_url(self):
        """Test creating client with custom URL."""
        client = create_client(base_url="https://custom.api.com")
        assert client.config.base_url == "https://custom.api.com"
