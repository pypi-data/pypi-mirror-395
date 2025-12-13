"""Pytest configuration and fixtures for SHIP Protocol tests."""

import pytest
from vibeatlas_ship import (
    ShipClient,
    ShipClientConfig,
    FileInfo,
    Language,
)


@pytest.fixture
def sample_file():
    """Create a sample FileInfo for testing."""
    return FileInfo(
        path="main.py",
        content="""
def calculate_total(items):
    \"\"\"Calculate total price of items.\"\"\"
    return sum(item.price for item in items)
""",
        language=Language.PYTHON,
    )


@pytest.fixture
def sample_files():
    """Create multiple sample files for testing."""
    return [
        FileInfo(
            path="main.py",
            content="from utils import helper\n\ndef main():\n    helper()",
            language=Language.PYTHON,
        ),
        FileInfo(
            path="utils.py",
            content="def helper():\n    return 42",
            language=Language.PYTHON,
        ),
    ]


@pytest.fixture
def test_config():
    """Create a test configuration."""
    return ShipClientConfig(
        base_url="https://test.ship.api.com",
        api_key="test_api_key_12345",
        timeout_seconds=10.0,
    )


@pytest.fixture
def test_client(test_config):
    """Create a test client."""
    return ShipClient(test_config)


@pytest.fixture
def mock_ship_response():
    """Create a mock SHIP response."""
    return {
        "ship_version": "1.0",
        "message_type": "ShipResponse",
        "message_id": "msg-123",
        "request_id": "req-456",
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
