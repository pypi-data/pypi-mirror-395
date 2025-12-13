"""
SHIP Protocol Exceptions

Antifragile error handling - all exceptions carry context for recovery.
"""

from __future__ import annotations

from typing import Any

from .types import ShipErrorCode


class ShipError(Exception):
    """Base exception for SHIP Protocol errors."""

    def __init__(
        self,
        message: str,
        code: ShipErrorCode = ShipErrorCode.INTERNAL_ERROR,
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
        should_retry: bool = False,
        retry_after_ms: int | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.request_id = request_id
        self.details = details or {}
        self.should_retry = should_retry
        self.retry_after_ms = retry_after_ms

    def __str__(self) -> str:
        parts = [f"[{self.code.value}] {self.message}"]
        if self.request_id:
            parts.append(f"(request_id: {self.request_id})")
        if self.should_retry:
            retry_info = f"retry in {self.retry_after_ms}ms" if self.retry_after_ms else "retry"
            parts.append(f"[{retry_info}]")
        return " ".join(parts)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "code": self.code.value,
            "message": self.message,
            "request_id": self.request_id,
            "details": self.details,
            "retry": {
                "should_retry": self.should_retry,
                "retry_after_ms": self.retry_after_ms,
            },
        }


class ShipValidationError(ShipError):
    """Request validation failed."""

    def __init__(
        self,
        message: str,
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.INVALID_REQUEST,
            request_id=request_id,
            details=details,
            should_retry=False,
        )


class ShipVersionError(ShipError):
    """Unsupported SHIP Protocol version."""

    def __init__(
        self,
        version: str,
        request_id: str | None = None,
    ) -> None:
        super().__init__(
            message=f"Unsupported SHIP version: {version}. Expected: 1.0",
            code=ShipErrorCode.INVALID_VERSION,
            request_id=request_id,
            should_retry=False,
        )


class ShipTimeoutError(ShipError):
    """Request timed out."""

    def __init__(
        self,
        message: str = "Request timed out",
        request_id: str | None = None,
        timeout_ms: int | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.TIMEOUT,
            request_id=request_id,
            details={"timeout_ms": timeout_ms} if timeout_ms else None,
            should_retry=True,
            retry_after_ms=1000,
        )


class ShipRateLimitError(ShipError):
    """Rate limit exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        request_id: str | None = None,
        retry_after_ms: int = 60000,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.RATE_LIMITED,
            request_id=request_id,
            should_retry=True,
            retry_after_ms=retry_after_ms,
        )


class ShipQuotaError(ShipError):
    """API quota exceeded."""

    def __init__(
        self,
        message: str = "API quota exceeded",
        request_id: str | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.QUOTA_EXCEEDED,
            request_id=request_id,
            should_retry=False,
        )


class ShipContextTooLargeError(ShipError):
    """Context exceeds maximum allowed size."""

    def __init__(
        self,
        message: str = "Context too large",
        request_id: str | None = None,
        max_tokens: int | None = None,
        actual_tokens: int | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.CONTEXT_TOO_LARGE,
            request_id=request_id,
            details={
                "max_tokens": max_tokens,
                "actual_tokens": actual_tokens,
            },
            should_retry=False,
        )


class ShipServiceError(ShipError):
    """Internal service error."""

    def __init__(
        self,
        message: str = "Internal service error",
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.INTERNAL_ERROR,
            request_id=request_id,
            details=details,
            should_retry=True,
            retry_after_ms=5000,
        )


class ShipUnavailableError(ShipError):
    """Service temporarily unavailable."""

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        request_id: str | None = None,
        retry_after_ms: int = 30000,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.SERVICE_UNAVAILABLE,
            request_id=request_id,
            should_retry=True,
            retry_after_ms=retry_after_ms,
        )


class CircuitBreakerOpenError(ShipError):
    """Circuit breaker is open - too many failures."""

    def __init__(
        self,
        message: str = "Circuit breaker open - service temporarily disabled",
        retry_after_ms: int = 30000,
    ) -> None:
        super().__init__(
            message=message,
            code=ShipErrorCode.SERVICE_UNAVAILABLE,
            should_retry=True,
            retry_after_ms=retry_after_ms,
        )


def exception_from_response(
    status_code: int,
    error_data: dict[str, Any] | None,
    request_id: str | None = None,
) -> ShipError:
    """Create appropriate exception from API response."""
    if error_data is None:
        error_data = {}

    error_info = error_data.get("error", {})
    code_str = error_info.get("code", "INTERNAL_ERROR")
    message = error_info.get("message", f"HTTP {status_code}")
    details = error_info.get("details")
    retry_info = error_info.get("retry", {})

    try:
        code = ShipErrorCode(code_str)
    except ValueError:
        code = ShipErrorCode.INTERNAL_ERROR

    # Map to specific exception types
    exception_map = {
        ShipErrorCode.INVALID_REQUEST: ShipValidationError,
        ShipErrorCode.INVALID_VERSION: lambda msg, rid, det: ShipVersionError("1.0", rid),
        ShipErrorCode.TIMEOUT: ShipTimeoutError,
        ShipErrorCode.RATE_LIMITED: ShipRateLimitError,
        ShipErrorCode.QUOTA_EXCEEDED: ShipQuotaError,
        ShipErrorCode.CONTEXT_TOO_LARGE: ShipContextTooLargeError,
        ShipErrorCode.SERVICE_UNAVAILABLE: ShipUnavailableError,
    }

    exception_class = exception_map.get(code, ShipServiceError)

    if exception_class in (ShipValidationError, ShipServiceError):
        return exception_class(message=message, request_id=request_id, details=details)
    elif exception_class == ShipTimeoutError:
        return ShipTimeoutError(message=message, request_id=request_id)
    elif exception_class == ShipRateLimitError:
        return ShipRateLimitError(
            message=message,
            request_id=request_id,
            retry_after_ms=retry_info.get("retry_after_ms", 60000),
        )
    elif exception_class == ShipUnavailableError:
        return ShipUnavailableError(
            message=message,
            request_id=request_id,
            retry_after_ms=retry_info.get("retry_after_ms", 30000),
        )
    else:
        return exception_class(message, request_id, details)
