"""
SHIP Protocol Client - Async-first, Antifragile HTTP Client

Philosophy:
- Antifragile: Circuit breaker, exponential backoff, graceful degradation
- Self-learning: Tracks success/failure patterns for optimization
- Modular: Swappable HTTP backend (httpx by default)
- Observable: Rich logging and metrics
"""

from __future__ import annotations

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncGenerator

import httpx

from .exceptions import (
    CircuitBreakerOpenError,
    ShipError,
    ShipRateLimitError,
    ShipTimeoutError,
    ShipUnavailableError,
    exception_from_response,
)
from .types import (
    ClientInfo,
    ConfidenceRequest,
    Context,
    ContextConstraints,
    FileInfo,
    FocusDirectives,
    Language,
    ShipFeedback,
    ShipRequest,
    ShipResponse,
    TaskOutcome,
)

logger = logging.getLogger("vibeatlas_ship")


# =============================================================================
# CIRCUIT BREAKER
# =============================================================================


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreaker:
    """
    Antifragile circuit breaker - prevents cascade failures.

    Opens after `failure_threshold` failures within `failure_window_seconds`.
    Resets after `recovery_timeout_seconds` in half-open state.
    """

    failure_threshold: int = 5
    failure_window_seconds: float = 60.0
    recovery_timeout_seconds: float = 30.0

    _state: CircuitState = field(default=CircuitState.CLOSED)
    _failures: list[float] = field(default_factory=list)
    _last_failure_time: float = 0.0
    _last_success_time: float = 0.0

    @property
    def state(self) -> CircuitState:
        """Get current circuit state, auto-transitioning if needed."""
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time >= self.recovery_timeout_seconds:
                self._state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker transitioning to HALF_OPEN")
        return self._state

    def record_success(self) -> None:
        """Record successful request."""
        self._last_success_time = time.time()
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            self._failures.clear()
            logger.info("Circuit breaker CLOSED - service recovered")

    def record_failure(self) -> None:
        """Record failed request."""
        now = time.time()
        self._last_failure_time = now

        # Remove old failures outside window
        self._failures = [t for t in self._failures if now - t < self.failure_window_seconds]
        self._failures.append(now)

        if len(self._failures) >= self.failure_threshold:
            self._state = CircuitState.OPEN
            logger.warning(
                f"Circuit breaker OPEN - {len(self._failures)} failures "
                f"in {self.failure_window_seconds}s"
            )
        elif self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
            logger.warning("Circuit breaker OPEN - half-open test failed")

    def allow_request(self) -> bool:
        """Check if request should be allowed."""
        return self.state != CircuitState.OPEN


# =============================================================================
# RETRY POLICY
# =============================================================================


@dataclass
class RetryPolicy:
    """Exponential backoff retry policy."""

    max_retries: int = 3
    base_delay_ms: int = 1000
    max_delay_ms: int = 30000
    exponential_base: float = 2.0
    jitter: bool = True

    def get_delay_ms(self, attempt: int) -> int:
        """Calculate delay for retry attempt."""
        import random

        delay = self.base_delay_ms * (self.exponential_base**attempt)
        delay = min(delay, self.max_delay_ms)

        if self.jitter:
            delay = delay * (0.5 + random.random())  # noqa: S311

        return int(delay)

    def should_retry(self, attempt: int, error: Exception) -> bool:
        """Determine if we should retry based on error type and attempt count."""
        if attempt >= self.max_retries:
            return False

        # Retry on specific error types
        if isinstance(error, (ShipTimeoutError, ShipUnavailableError, ShipRateLimitError)):
            return error.should_retry

        if isinstance(error, ShipError):
            return error.should_retry

        # Retry on connection errors
        if isinstance(error, (httpx.ConnectError, httpx.ReadTimeout)):
            return True

        return False


# =============================================================================
# CLIENT CONFIGURATION
# =============================================================================


@dataclass
class ShipClientConfig:
    """Client configuration with sensible defaults."""

    base_url: str = "https://ship.vibeatlas.dev"
    api_key: str | None = None
    timeout_seconds: float = 30.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    circuit_breaker: CircuitBreaker = field(default_factory=CircuitBreaker)
    client_info: ClientInfo = field(default_factory=ClientInfo)

    # Feature flags
    enable_caching: bool = True
    enable_telemetry: bool = True
    enable_feedback_loop: bool = True


# =============================================================================
# SHIP CLIENT
# =============================================================================


class ShipClient:
    """
    SHIP Protocol Client - Your gateway to AI coding reliability.

    Features:
    - Async-first with sync wrapper
    - Circuit breaker for resilience
    - Exponential backoff retry
    - Request caching
    - Automatic feedback loop

    Example:
        ```python
        async with ShipClient() as client:
            response = await client.assess(
                files=[FileInfo(path="main.py", content="...", language=Language.PYTHON)],
                prompt="Add error handling",
            )
            print(f"SHIP Score: {response.ship_score.score} ({response.ship_score.grade})")
        ```
    """

    def __init__(self, config: ShipClientConfig | None = None) -> None:
        self.config = config or ShipClientConfig()
        self._http_client: httpx.AsyncClient | None = None
        self._cache: dict[str, tuple[float, ShipResponse]] = {}
        self._cache_ttl_seconds = 300  # 5 minutes

        # Metrics for self-learning
        self._request_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._total_latency_ms = 0

    @property
    def http_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": f"{self.config.client_info.name}/{self.config.client_info.version}",
            }
            if self.config.api_key:
                headers["Authorization"] = f"Bearer {self.config.api_key}"

            self._http_client = httpx.AsyncClient(
                base_url=self.config.base_url,
                headers=headers,
                timeout=httpx.Timeout(self.config.timeout_seconds),
            )
        return self._http_client

    async def __aenter__(self) -> "ShipClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def close(self) -> None:
        """Close the client and release resources."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    # =========================================================================
    # CORE API METHODS
    # =========================================================================

    async def assess(
        self,
        files: list[FileInfo],
        prompt: str,
        *,
        project_root: str | None = None,
        confidence_request: ConfidenceRequest | None = None,
        focus_directives: FocusDirectives | None = None,
        context_constraints: ContextConstraints | None = None,
    ) -> ShipResponse:
        """
        Assess code context and get SHIP Score.

        Args:
            files: List of files to assess
            prompt: The task prompt
            project_root: Project root path
            confidence_request: Confidence scoring options
            focus_directives: Focus management options
            context_constraints: Context optimization constraints

        Returns:
            ShipResponse with score, assessments, and recommendations

        Raises:
            ShipError: On API errors
            CircuitBreakerOpenError: When circuit breaker is open
        """
        context = Context(
            files=files,
            prompt=prompt,
            project_root=project_root,
        )

        request = ShipRequest(
            context=context,
            confidence_request=confidence_request,
            focus_directives=focus_directives,
            context_constraints=context_constraints,
            client_info=self.config.client_info,
        )

        return await self._execute_with_retry(
            method="POST",
            endpoint="/v1/ship/assess",
            data=request.model_dump(exclude_none=True),
            response_model=ShipResponse,
        )

    async def feedback(
        self,
        request_id: str,
        outcome: TaskOutcome,
        *,
        actual_ship_score: int | None = None,
    ) -> None:
        """
        Submit feedback for a previous assessment - enables the learning flywheel.

        Args:
            request_id: The request_id from the original assessment
            outcome: The task outcome
            actual_ship_score: The actual score achieved (optional)
        """
        feedback = ShipFeedback(
            request_id=request_id,
            outcome=outcome,
            actual_ship_score=actual_ship_score,
        )

        await self._execute_with_retry(
            method="POST",
            endpoint="/v1/ship/feedback",
            data=feedback.model_dump(exclude_none=True),
            response_model=None,  # 204 No Content
        )

    async def get_score(self, project_id: str) -> dict[str, Any]:
        """
        Get current SHIP Score for a project.

        Args:
            project_id: Project identifier

        Returns:
            Project score data
        """
        return await self._execute_with_retry(
            method="GET",
            endpoint=f"/v1/ship/score/{project_id}",
            response_model=None,
        )

    async def get_metrics(self) -> dict[str, Any]:
        """
        Get account-level metrics.

        Returns:
            Metrics data
        """
        return await self._execute_with_retry(
            method="GET",
            endpoint="/v1/ship/metrics",
            response_model=None,
        )

    async def get_badge_url(
        self,
        project_id: str,
        style: str = "flat",
        format: str = "svg",
    ) -> str:
        """
        Get badge URL for a project.

        Args:
            project_id: Project identifier
            style: Badge style (flat, flat-square, plastic, for-the-badge)
            format: Output format (svg, json)

        Returns:
            Badge URL
        """
        return f"{self.config.base_url}/v1/ship/badge/{project_id}?style={style}&format={format}"

    async def health(self) -> dict[str, Any]:
        """
        Check API health.

        Returns:
            Health status data
        """
        return await self._execute_with_retry(
            method="GET",
            endpoint="/health",
            response_model=None,
        )

    # =========================================================================
    # CONVENIENCE METHODS
    # =========================================================================

    async def quick_assess(
        self,
        code: str,
        prompt: str,
        *,
        language: Language = Language.OTHER,
        filename: str = "code.txt",
    ) -> ShipResponse:
        """
        Quick assessment from a single code snippet.

        Args:
            code: Code content
            prompt: Task prompt
            language: Programming language
            filename: Virtual filename

        Returns:
            ShipResponse
        """
        file = FileInfo(
            path=filename,
            content=code,
            language=language,
        )
        return await self.assess(files=[file], prompt=prompt)

    async def assess_files(
        self,
        file_paths: list[str],
        prompt: str,
        *,
        project_root: str | None = None,
    ) -> ShipResponse:
        """
        Assess files from disk.

        Args:
            file_paths: List of file paths to read and assess
            prompt: Task prompt
            project_root: Project root path

        Returns:
            ShipResponse
        """
        from pathlib import Path

        files: list[FileInfo] = []

        for path_str in file_paths:
            path = Path(path_str)
            if path.exists():
                content = path.read_text(encoding="utf-8")
                language = self._detect_language(path.suffix)
                files.append(
                    FileInfo(
                        path=str(path),
                        content=content,
                        language=language,
                    )
                )

        if not files:
            raise ValueError("No valid files found")

        return await self.assess(files=files, prompt=prompt, project_root=project_root)

    # =========================================================================
    # INTERNAL METHODS
    # =========================================================================

    async def _execute_with_retry(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        response_model: type | None = None,
    ) -> Any:
        """Execute request with circuit breaker and retry logic."""
        # Check circuit breaker
        if not self.config.circuit_breaker.allow_request():
            raise CircuitBreakerOpenError()

        last_error: Exception | None = None

        for attempt in range(self.config.retry_policy.max_retries + 1):
            try:
                result = await self._execute_request(
                    method=method,
                    endpoint=endpoint,
                    data=data,
                    response_model=response_model,
                )
                self.config.circuit_breaker.record_success()
                return result

            except Exception as e:
                last_error = e
                self.config.circuit_breaker.record_failure()

                if not self.config.retry_policy.should_retry(attempt, e):
                    raise

                delay_ms = self.config.retry_policy.get_delay_ms(attempt)
                logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {delay_ms}ms")
                await asyncio.sleep(delay_ms / 1000)

        if last_error:
            raise last_error
        raise ShipError("Request failed after all retries")

    async def _execute_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        response_model: type | None = None,
    ) -> Any:
        """Execute single HTTP request."""
        self._request_count += 1
        start_time = time.time()

        try:
            if method == "GET":
                response = await self.http_client.get(endpoint)
            elif method == "POST":
                response = await self.http_client.post(endpoint, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            latency_ms = int((time.time() - start_time) * 1000)
            self._total_latency_ms += latency_ms

            # Handle response
            if response.status_code == 204:
                self._success_count += 1
                return None

            if response.status_code >= 400:
                self._failure_count += 1
                error_data = response.json() if response.content else None
                request_id = data.get("message_id") if data else None
                raise exception_from_response(response.status_code, error_data, request_id)

            self._success_count += 1

            if response_model:
                return response_model.model_validate(response.json())
            return response.json()

        except httpx.TimeoutException as e:
            self._failure_count += 1
            request_id = data.get("message_id") if data else None
            raise ShipTimeoutError(request_id=request_id) from e

        except httpx.HTTPError as e:
            self._failure_count += 1
            raise ShipUnavailableError(str(e)) from e

    def _detect_language(self, suffix: str) -> Language:
        """Detect language from file extension."""
        mapping = {
            ".ts": Language.TYPESCRIPT,
            ".tsx": Language.TYPESCRIPT,
            ".js": Language.JAVASCRIPT,
            ".jsx": Language.JAVASCRIPT,
            ".py": Language.PYTHON,
            ".java": Language.JAVA,
            ".go": Language.GO,
            ".rs": Language.RUST,
            ".cs": Language.CSHARP,
            ".cpp": Language.CPP,
            ".cc": Language.CPP,
            ".c": Language.CPP,
            ".rb": Language.RUBY,
            ".php": Language.PHP,
            ".swift": Language.SWIFT,
            ".kt": Language.KOTLIN,
        }
        return mapping.get(suffix.lower(), Language.OTHER)

    # =========================================================================
    # METRICS (Self-Learning)
    # =========================================================================

    def get_client_metrics(self) -> dict[str, Any]:
        """Get client-side metrics for self-learning."""
        return {
            "request_count": self._request_count,
            "success_count": self._success_count,
            "failure_count": self._failure_count,
            "success_rate": (
                self._success_count / self._request_count if self._request_count > 0 else 0
            ),
            "avg_latency_ms": (
                self._total_latency_ms / self._request_count if self._request_count > 0 else 0
            ),
            "circuit_breaker_state": self.config.circuit_breaker.state.value,
        }


# =============================================================================
# SYNC WRAPPER
# =============================================================================


class SyncShipClient:
    """
    Synchronous wrapper for ShipClient.

    For users who prefer synchronous code or are working in sync contexts.

    Example:
        ```python
        with SyncShipClient() as client:
            response = client.assess(
                files=[FileInfo(path="main.py", content="...", language=Language.PYTHON)],
                prompt="Add error handling",
            )
            print(f"SHIP Score: {response.ship_score.score}")
        ```
    """

    def __init__(self, config: ShipClientConfig | None = None) -> None:
        self._async_client = ShipClient(config)
        self._loop: asyncio.AbstractEventLoop | None = None

    def __enter__(self) -> "SyncShipClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the client."""
        self._run(self._async_client.close())

    def _run(self, coro: Any) -> Any:
        """Run async coroutine in sync context."""
        try:
            loop = asyncio.get_running_loop()
            # Already in async context, use run_until_complete
            import nest_asyncio

            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        except RuntimeError:
            # No running loop, create new one
            return asyncio.run(coro)

    def assess(self, *args: Any, **kwargs: Any) -> ShipResponse:
        """Sync wrapper for assess()."""
        return self._run(self._async_client.assess(*args, **kwargs))

    def feedback(self, *args: Any, **kwargs: Any) -> None:
        """Sync wrapper for feedback()."""
        return self._run(self._async_client.feedback(*args, **kwargs))

    def quick_assess(self, *args: Any, **kwargs: Any) -> ShipResponse:
        """Sync wrapper for quick_assess()."""
        return self._run(self._async_client.quick_assess(*args, **kwargs))

    def assess_files(self, *args: Any, **kwargs: Any) -> ShipResponse:
        """Sync wrapper for assess_files()."""
        return self._run(self._async_client.assess_files(*args, **kwargs))

    def health(self) -> dict[str, Any]:
        """Sync wrapper for health()."""
        return self._run(self._async_client.health())

    def get_client_metrics(self) -> dict[str, Any]:
        """Get client metrics."""
        return self._async_client.get_client_metrics()


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================


def create_client(
    api_key: str | None = None,
    base_url: str = "https://ship.vibeatlas.dev",
    **kwargs: Any,
) -> ShipClient:
    """
    Create a SHIP client with sensible defaults.

    Args:
        api_key: API key (optional for free tier)
        base_url: API base URL
        **kwargs: Additional config options

    Returns:
        Configured ShipClient
    """
    config = ShipClientConfig(
        api_key=api_key,
        base_url=base_url,
        **kwargs,
    )
    return ShipClient(config)


def create_sync_client(
    api_key: str | None = None,
    base_url: str = "https://ship.vibeatlas.dev",
    **kwargs: Any,
) -> SyncShipClient:
    """
    Create a synchronous SHIP client.

    Args:
        api_key: API key (optional for free tier)
        base_url: API base URL
        **kwargs: Additional config options

    Returns:
        Configured SyncShipClient
    """
    config = ShipClientConfig(
        api_key=api_key,
        base_url=base_url,
        **kwargs,
    )
    return SyncShipClient(config)


@asynccontextmanager
async def ship_client(
    api_key: str | None = None,
    **kwargs: Any,
) -> AsyncGenerator[ShipClient, None]:
    """
    Context manager for creating a SHIP client.

    Example:
        ```python
        async with ship_client() as client:
            response = await client.quick_assess(
                code="def hello(): print('world')",
                prompt="Add type hints",
                language=Language.PYTHON,
            )
        ```
    """
    client = create_client(api_key=api_key, **kwargs)
    try:
        yield client
    finally:
        await client.close()
