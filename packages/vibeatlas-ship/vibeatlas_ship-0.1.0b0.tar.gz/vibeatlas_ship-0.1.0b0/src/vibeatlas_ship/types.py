"""
SHIP Protocol Types - Pydantic Models

Success Heuristics for Intelligent Programming.
Fully typed, validated, and serializable.

Philosophy: Antifragile - All types have sensible defaults and graceful degradation.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


# =============================================================================
# ENUMS
# =============================================================================


class Language(str, Enum):
    """Supported programming languages."""

    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    CSHARP = "csharp"
    CPP = "cpp"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    OTHER = "other"


class AIModel(str, Enum):
    """Supported AI models."""

    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"
    CLAUDE_OPUS = "claude-opus"
    CLAUDE_SONNET = "claude-sonnet"
    CLAUDE_HAIKU = "claude-haiku"
    GEMINI_PRO = "gemini-pro"
    GEMINI_ULTRA = "gemini-ultra"
    CODESTRAL = "codestral"
    DEEPSEEK_CODER = "deepseek-coder"
    OTHER = "other"


class ConfidenceLevel(str, Enum):
    """Confidence level categories."""

    VERY_HIGH = "very_high"  # 90-100%
    HIGH = "high"  # 75-89%
    MEDIUM = "medium"  # 50-74%
    LOW = "low"  # 25-49%
    UNCERTAIN = "uncertain"  # 0-24%


class RiskTolerance(str, Enum):
    """Risk tolerance settings."""

    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class RetryStrategy(str, Enum):
    """Retry strategies for failed tasks."""

    NONE = "none"
    INCREMENTAL = "incremental"
    FULL_RESET = "full_reset"
    DECOMPOSE = "decompose"


class ShipGrade(str, Enum):
    """SHIP Score grades."""

    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class ShipErrorCode(str, Enum):
    """SHIP Protocol error codes."""

    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_VERSION = "INVALID_VERSION"
    TIMEOUT = "TIMEOUT"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    RATE_LIMITED = "RATE_LIMITED"
    CONTEXT_TOO_LARGE = "CONTEXT_TOO_LARGE"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


# =============================================================================
# CORE TYPES
# =============================================================================


class FileInfo(BaseModel):
    """File information with metadata."""

    path: str = Field(..., description="File path relative to project root")
    content: str = Field(..., description="File content")
    language: Language = Field(default=Language.OTHER, description="Programming language")
    size_bytes: int = Field(default=0, description="Size in bytes")
    relevance_score: float | None = Field(default=None, ge=0, le=1, description="Relevance score")
    tokens: int | None = Field(default=None, description="Token count")
    last_modified: str | None = Field(default=None, description="Last modified timestamp")
    git_status: Literal["modified", "added", "deleted", "unchanged"] | None = Field(
        default=None, description="Git status"
    )

    @field_validator("size_bytes", mode="before")
    @classmethod
    def compute_size(cls, v: int, info: Any) -> int:
        """Auto-compute size from content if not provided."""
        if v == 0 and "content" in info.data:
            return len(info.data["content"].encode("utf-8"))
        return v


class Context(BaseModel):
    """Context to be optimized."""

    files: list[FileInfo] = Field(..., min_length=1, description="Files in context")
    prompt: str = Field(..., min_length=1, description="User prompt or query")
    project_root: str | None = Field(default=None, description="Project root path")
    metadata: dict[str, Any] | None = Field(default=None, description="Additional metadata")


class RiskFactor(BaseModel):
    """Risk factor identified in context."""

    factor: str = Field(..., description="Description of the risk")
    severity: float = Field(..., ge=0, le=1, description="Severity score")
    mitigation: str | None = Field(default=None, description="Suggested mitigation")
    category: Literal["complexity", "dependency", "ambiguity", "scope", "technical"] | None = (
        Field(default=None, description="Category of risk")
    )


class SuccessPattern(BaseModel):
    """Success pattern matched from historical data."""

    pattern_id: str = Field(..., description="Pattern identifier")
    description: str = Field(..., description="Pattern description")
    match_confidence: float = Field(..., ge=0, le=1, description="Match confidence")
    success_rate: float = Field(..., ge=0, le=1, description="Historical success rate")


# =============================================================================
# SHIP SCORE
# =============================================================================


class ShipScore(BaseModel):
    """SHIP Score breakdown - the core reliability metric."""

    score: int = Field(..., ge=0, le=100, description="Overall SHIP Score")
    grade: ShipGrade = Field(..., description="Score grade")
    confidence_component: float = Field(..., description="Confidence component (0-100) x 0.40")
    focus_component: float = Field(..., description="Focus component (0-100) x 0.30")
    context_component: float = Field(..., description="Context component (0-100) x 0.20")
    efficiency_component: float = Field(..., description="Efficiency component (0-100) x 0.10")
    layer_scores: dict[str, float] = Field(..., description="Individual layer scores")
    percentile: int | None = Field(default=None, ge=0, le=100, description="Percentile rank")

    @classmethod
    def calculate(
        cls,
        confidence: float,
        focus: float,
        context: float,
        efficiency: float,
    ) -> "ShipScore":
        """Calculate SHIP Score from layer scores."""
        confidence_component = confidence * 0.40
        focus_component = focus * 0.30
        context_component = context * 0.20
        efficiency_component = efficiency * 0.10

        score = round(
            confidence_component + focus_component + context_component + efficiency_component
        )

        return cls(
            score=score,
            grade=cls._get_grade(score),
            confidence_component=round(confidence_component, 2),
            focus_component=round(focus_component, 2),
            context_component=round(context_component, 2),
            efficiency_component=round(efficiency_component, 2),
            layer_scores={
                "confidence": confidence,
                "focus": focus,
                "context": context,
                "efficiency": efficiency,
            },
        )

    @staticmethod
    def _get_grade(score: int) -> ShipGrade:
        """Get grade from numeric score."""
        if score >= 95:
            return ShipGrade.A_PLUS
        if score >= 85:
            return ShipGrade.A
        if score >= 70:
            return ShipGrade.B
        if score >= 50:
            return ShipGrade.C
        if score >= 30:
            return ShipGrade.D
        return ShipGrade.F


# =============================================================================
# ASSESSMENTS
# =============================================================================


class ConfidenceAssessment(BaseModel):
    """Confidence assessment for a task."""

    task_completion_probability: float = Field(..., ge=0, le=1)
    confidence_level: ConfidenceLevel
    confidence_score: float = Field(..., ge=0, le=100)
    risk_factors: list[RiskFactor] = Field(default_factory=list)
    success_patterns: list[SuccessPattern] = Field(default_factory=list)
    historical_success_rate: float = Field(default=0.8, ge=0, le=1)
    recommended_retry_strategy: RetryStrategy = Field(default=RetryStrategy.INCREMENTAL)
    similar_tasks_count: int = Field(default=0, ge=0)


class FileFocus(BaseModel):
    """File focus specification."""

    file: str
    lines: str | None = None
    reason: str | None = None
    attention_weight: float | None = Field(default=None, ge=0, le=1)
    semantic_role: Literal["primary", "dependency", "reference", "context"] | None = None


class SemanticCoverage(BaseModel):
    """Semantic coverage analysis."""

    anchors_found: list[str] = Field(default_factory=list)
    anchors_missing: list[str] = Field(default_factory=list)
    coverage_percentage: float = Field(default=0, ge=0, le=100)


class FocusAssessment(BaseModel):
    """Focus assessment in response."""

    focus_score: float = Field(..., ge=0, le=100)
    primary_context: list[FileFocus] = Field(default_factory=list)
    semantic_coverage: SemanticCoverage = Field(default_factory=SemanticCoverage)
    focus_distribution: dict[str, float] = Field(default_factory=dict)
    distractions_filtered: int = Field(default=0, ge=0)
    focus_efficiency: float = Field(default=0, ge=0, le=1)


class ContextAssessment(BaseModel):
    """Context assessment in response."""

    context_score: float = Field(..., ge=0, le=100)
    original_tokens: int = Field(default=0, ge=0)
    optimized_tokens: int = Field(default=0, ge=0)
    reduction_percentage: float = Field(default=0, ge=0, le=100)
    relevance_distribution: dict[str, int] = Field(
        default_factory=lambda: {"high": 0, "medium": 0, "low": 0}
    )


class EfficiencyMetrics(BaseModel):
    """Efficiency metrics."""

    efficiency_score: float = Field(..., ge=0, le=100)
    tokens_saved: int = Field(default=0, ge=0)
    percentage_saved: float = Field(default=0, ge=0, le=100)
    cost_saved_usd: float = Field(default=0, ge=0)
    co2_saved_grams: float = Field(default=0, ge=0)
    processing_time_ms: int = Field(default=0, ge=0)
    throughput_rps: float | None = Field(default=None, ge=0)


class Recommendation(BaseModel):
    """Recommendation for improving SHIP Score."""

    type: Literal["confidence", "focus", "context", "efficiency"]
    priority: int = Field(..., ge=1, le=5)
    message: str
    expected_improvement: float = Field(default=0, ge=0)
    action: str | None = None


class OptimizedContext(BaseModel):
    """Optimized context result."""

    files: list[FileInfo] = Field(default_factory=list)
    total_tokens: int = Field(default=0, ge=0)
    excluded_files_count: int = Field(default=0, ge=0)
    context_coverage: float = Field(default=0, ge=0, le=100)


# =============================================================================
# REQUESTS & RESPONSES
# =============================================================================


class ConfidenceRequest(BaseModel):
    """Confidence request parameters."""

    enable_confidence_scoring: bool = True
    historical_context: dict[str, Any] | None = None
    risk_tolerance: RiskTolerance = RiskTolerance.MODERATE
    minimum_confidence: float | None = Field(default=None, ge=0, le=1)


class FocusDirectives(BaseModel):
    """Focus directives for context selection."""

    focus_priority: list[FileFocus] | None = None
    semantic_anchors: list[str] | None = None
    ignore_signals: list[str] | None = None
    max_files: int | None = Field(default=None, gt=0)
    dependency_depth: int | None = Field(default=None, ge=0)


class ContextConstraints(BaseModel):
    """Context optimization constraints."""

    max_tokens: int | None = Field(default=None, gt=0)
    target_model: AIModel | None = None
    min_relevance_score: float | None = Field(default=None, ge=0, le=1)
    exclude_tests: bool = False
    exclude_config: bool = False
    preserve_patterns: list[str] | None = None


class ClientInfo(BaseModel):
    """Client information."""

    name: str = "vibeatlas-ship-python"
    version: str = "0.1.0"
    platform: str | None = None


class ShipRequest(BaseModel):
    """SHIP Request message."""

    ship_version: Literal["1.0"] = "1.0"
    message_type: Literal["ShipRequest"] = "ShipRequest"
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    context: Context
    confidence_request: ConfidenceRequest | None = None
    focus_directives: FocusDirectives | None = None
    context_constraints: ContextConstraints | None = None
    client_info: ClientInfo = Field(default_factory=ClientInfo)


class ShipResponse(BaseModel):
    """SHIP Response message."""

    ship_version: Literal["1.0"] = "1.0"
    message_type: Literal["ShipResponse"] = "ShipResponse"
    message_id: str
    request_id: str
    timestamp: str
    ship_score: ShipScore
    confidence: ConfidenceAssessment
    focus: FocusAssessment
    context: ContextAssessment
    efficiency: EfficiencyMetrics
    optimized_context: OptimizedContext
    recommendations: list[Recommendation] = Field(default_factory=list)


class TaskOutcome(BaseModel):
    """Task outcome for feedback."""

    task_completed: bool
    first_attempt_success: bool = False
    total_attempts: int = Field(default=1, ge=1)
    time_to_completion_ms: int | None = Field(default=None, ge=0)
    user_satisfaction: Literal[1, 2, 3, 4, 5] | None = None
    feedback_text: str | None = None


class FocusFeedback(BaseModel):
    """Focus quality feedback."""

    focus_helpful: bool
    missed_context: list[str] | None = None
    unnecessary_context: list[str] | None = None
    utilization_rate: float = Field(default=0, ge=0, le=1)


class ErrorPattern(BaseModel):
    """Error pattern observation."""

    error_type: str
    error_code: str | None = None
    frequency: int = Field(default=1, ge=1)
    auto_resolved: bool = False
    resolution_method: str | None = None


class LearningSignals(BaseModel):
    """Learning signals for pattern improvement."""

    pattern_reinforcement: list[str] | None = None
    pattern_correction: list[str] | None = None
    new_patterns: list[str] | None = None


class ShipFeedback(BaseModel):
    """SHIP Feedback message - enables the learning flywheel."""

    ship_version: Literal["1.0"] = "1.0"
    message_type: Literal["ShipFeedback"] = "ShipFeedback"
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    request_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    outcome: TaskOutcome
    actual_ship_score: int | None = Field(default=None, ge=0, le=100)
    focus_feedback: FocusFeedback | None = None
    error_patterns: list[ErrorPattern] | None = None
    learning_signals: LearningSignals | None = None


class ShipErrorInfo(BaseModel):
    """Error information."""

    code: ShipErrorCode
    message: str
    details: dict[str, Any] | None = None
    retry: dict[str, Any] | None = None


class ShipError(BaseModel):
    """SHIP Error message."""

    ship_version: Literal["1.0"] = "1.0"
    message_type: Literal["ShipError"] = "ShipError"
    message_id: str
    request_id: str
    timestamp: str
    error: ShipErrorInfo


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_grade_color(grade: ShipGrade) -> str:
    """Get badge color for grade."""
    colors = {
        ShipGrade.A_PLUS: "brightgreen",
        ShipGrade.A: "green",
        ShipGrade.B: "yellowgreen",
        ShipGrade.C: "yellow",
        ShipGrade.D: "orange",
        ShipGrade.F: "red",
    }
    return colors.get(grade, "lightgrey")


def interpret_score(score: int) -> dict[str, str]:
    """Get human-readable interpretation of SHIP Score."""
    grade = ShipScore._get_grade(score)

    interpretations = {
        ShipGrade.A_PLUS: {
            "summary": "Exceptional reliability - Ready for production",
            "reliability": "Tasks will succeed 95%+ of the time with minimal retries",
            "recommendation": "Proceed with confidence. This context is optimally configured.",
        },
        ShipGrade.A: {
            "summary": "High reliability - Production ready",
            "reliability": "Tasks will succeed 85-94% of the time",
            "recommendation": "Good to proceed. Minor improvements possible in focus or context.",
        },
        ShipGrade.B: {
            "summary": "Good reliability - Acceptable for most tasks",
            "reliability": "Tasks will succeed 70-84% of the time",
            "recommendation": "Proceed with awareness. Consider reviewing risk factors.",
        },
        ShipGrade.C: {
            "summary": "Moderate reliability - May require iteration",
            "reliability": "Tasks will succeed 50-69% of the time",
            "recommendation": "Consider breaking task into smaller pieces or providing more context.",
        },
        ShipGrade.D: {
            "summary": "Low reliability - High risk of failure",
            "reliability": "Tasks will succeed 30-49% of the time",
            "recommendation": "Strongly recommend adding more context or simplifying the task.",
        },
        ShipGrade.F: {
            "summary": "Unreliable - Likely to fail",
            "reliability": "Tasks will succeed less than 30% of the time",
            "recommendation": "Do not proceed. Significant changes needed to context or task.",
        },
    }

    return {
        "score": str(score),
        "grade": grade.value,
        **interpretations[grade],
    }
