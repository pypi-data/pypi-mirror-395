"""
SHIP Protocol SDK - Success Heuristics for Intelligent Programming

The industry standard for measuring AI coding agent reliability.

Get started:
    ```python
    from vibeatlas_ship import ShipClient, FileInfo, Language

    async with ShipClient() as client:
        response = await client.assess(
            files=[FileInfo(path="main.py", content="...", language=Language.PYTHON)],
            prompt="Add error handling",
        )
        print(f"SHIP Score: {response.ship_score.score} ({response.ship_score.grade.value})")

    # Or use the sync client
    with SyncShipClient() as client:
        response = client.quick_assess(
            code="def hello(): print('world')",
            prompt="Add type hints",
            language=Language.PYTHON,
        )
    ```

Philosophy:
    - Antifragile: Circuit breaker, exponential backoff, graceful degradation
    - Self-learning: Tracks patterns for optimization via feedback loop
    - Modular: Swappable components, typed, validated
    - Observable: Rich metrics and logging

Links:
    - Documentation: https://vibeatlas.dev/docs/ship
    - API Reference: https://ship.vibeatlas.dev
    - GitHub: https://github.com/vibeatlas/ship-protocol
"""

from .client import (
    CircuitBreaker,
    CircuitState,
    RetryPolicy,
    ShipClient,
    ShipClientConfig,
    SyncShipClient,
    create_client,
    create_sync_client,
    ship_client,
)
from .exceptions import (
    CircuitBreakerOpenError,
    ShipContextTooLargeError,
    ShipError,
    ShipQuotaError,
    ShipRateLimitError,
    ShipServiceError,
    ShipTimeoutError,
    ShipUnavailableError,
    ShipValidationError,
    ShipVersionError,
)
from .types import (
    AIModel,
    ClientInfo,
    ConfidenceAssessment,
    ConfidenceLevel,
    ConfidenceRequest,
    Context,
    ContextAssessment,
    ContextConstraints,
    EfficiencyMetrics,
    ErrorPattern,
    FileInfo,
    FileFocus,
    FocusAssessment,
    FocusDirectives,
    FocusFeedback,
    Language,
    LearningSignals,
    OptimizedContext,
    Recommendation,
    RetryStrategy,
    RiskFactor,
    RiskTolerance,
    SemanticCoverage,
    ShipErrorCode,
    ShipErrorInfo,
    ShipFeedback,
    ShipGrade,
    ShipRequest,
    ShipResponse,
    ShipScore,
    SuccessPattern,
    TaskOutcome,
    get_grade_color,
    interpret_score,
)

__version__ = "0.1.0-beta"
__author__ = "VibeAtlas"
__all__ = [
    # Version
    "__version__",
    # Client
    "ShipClient",
    "SyncShipClient",
    "ShipClientConfig",
    "create_client",
    "create_sync_client",
    "ship_client",
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitState",
    "RetryPolicy",
    # Exceptions
    "ShipError",
    "ShipValidationError",
    "ShipVersionError",
    "ShipTimeoutError",
    "ShipRateLimitError",
    "ShipQuotaError",
    "ShipContextTooLargeError",
    "ShipServiceError",
    "ShipUnavailableError",
    "CircuitBreakerOpenError",
    # Enums
    "Language",
    "AIModel",
    "ConfidenceLevel",
    "RiskTolerance",
    "RetryStrategy",
    "ShipGrade",
    "ShipErrorCode",
    # Core Types
    "FileInfo",
    "Context",
    "RiskFactor",
    "SuccessPattern",
    "ShipScore",
    # Assessments
    "ConfidenceAssessment",
    "FileFocus",
    "SemanticCoverage",
    "FocusAssessment",
    "ContextAssessment",
    "EfficiencyMetrics",
    "Recommendation",
    "OptimizedContext",
    # Requests
    "ConfidenceRequest",
    "FocusDirectives",
    "ContextConstraints",
    "ClientInfo",
    "ShipRequest",
    # Responses
    "ShipResponse",
    "ShipErrorInfo",
    # Feedback
    "TaskOutcome",
    "FocusFeedback",
    "ErrorPattern",
    "LearningSignals",
    "ShipFeedback",
    # Utilities
    "get_grade_color",
    "interpret_score",
]
