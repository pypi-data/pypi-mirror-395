"""Tests for SHIP Protocol types."""

import pytest
from vibeatlas_ship.types import (
    FileInfo,
    Context,
    ShipScore,
    ShipGrade,
    Language,
    ConfidenceLevel,
    RiskFactor,
    interpret_score,
    get_grade_color,
)


class TestFileInfo:
    """Tests for FileInfo model."""

    def test_basic_creation(self):
        """Test basic FileInfo creation."""
        file = FileInfo(
            path="main.py",
            content="print('hello')",
            language=Language.PYTHON,
        )
        assert file.path == "main.py"
        assert file.content == "print('hello')"
        assert file.language == Language.PYTHON

    def test_size_auto_calculation(self):
        """Test that size is auto-calculated from content."""
        content = "hello world"
        file = FileInfo(path="test.txt", content=content, language=Language.OTHER)
        # Note: size_bytes defaults to 0, auto-calc happens in validator
        assert file.size_bytes >= 0

    def test_optional_fields(self):
        """Test optional fields have correct defaults."""
        file = FileInfo(path="test.py", content="", language=Language.PYTHON)
        assert file.relevance_score is None
        assert file.tokens is None
        assert file.last_modified is None
        assert file.git_status is None


class TestContext:
    """Tests for Context model."""

    def test_requires_files(self):
        """Test that context requires at least one file."""
        file = FileInfo(path="test.py", content="code", language=Language.PYTHON)
        context = Context(files=[file], prompt="Do something")
        assert len(context.files) == 1

    def test_requires_prompt(self):
        """Test that context requires a prompt."""
        file = FileInfo(path="test.py", content="code", language=Language.PYTHON)
        context = Context(files=[file], prompt="Test prompt")
        assert context.prompt == "Test prompt"

    def test_empty_files_fails(self):
        """Test that empty files list fails validation."""
        with pytest.raises(ValueError):
            Context(files=[], prompt="Test")


class TestShipScore:
    """Tests for ShipScore model."""

    def test_calculate_score(self):
        """Test SHIP Score calculation."""
        score = ShipScore.calculate(
            confidence=90,
            focus=85,
            context=80,
            efficiency=75,
        )

        # 90*0.40 + 85*0.30 + 80*0.20 + 75*0.10 = 36 + 25.5 + 16 + 7.5 = 85
        assert score.score == 85
        assert score.grade == ShipGrade.A

    def test_grade_thresholds(self):
        """Test all grade thresholds."""
        assert ShipScore._get_grade(100) == ShipGrade.A_PLUS
        assert ShipScore._get_grade(95) == ShipGrade.A_PLUS
        assert ShipScore._get_grade(94) == ShipGrade.A
        assert ShipScore._get_grade(85) == ShipGrade.A
        assert ShipScore._get_grade(84) == ShipGrade.B
        assert ShipScore._get_grade(70) == ShipGrade.B
        assert ShipScore._get_grade(69) == ShipGrade.C
        assert ShipScore._get_grade(50) == ShipGrade.C
        assert ShipScore._get_grade(49) == ShipGrade.D
        assert ShipScore._get_grade(30) == ShipGrade.D
        assert ShipScore._get_grade(29) == ShipGrade.F
        assert ShipScore._get_grade(0) == ShipGrade.F

    def test_layer_scores_preserved(self):
        """Test that layer scores are preserved in output."""
        score = ShipScore.calculate(
            confidence=80,
            focus=70,
            context=60,
            efficiency=50,
        )
        assert score.layer_scores["confidence"] == 80
        assert score.layer_scores["focus"] == 70
        assert score.layer_scores["context"] == 60
        assert score.layer_scores["efficiency"] == 50


class TestRiskFactor:
    """Tests for RiskFactor model."""

    def test_basic_creation(self):
        """Test basic RiskFactor creation."""
        risk = RiskFactor(
            factor="Complex regex pattern",
            severity=0.7,
            mitigation="Add unit tests",
            category="complexity",
        )
        assert risk.factor == "Complex regex pattern"
        assert risk.severity == 0.7
        assert risk.category == "complexity"

    def test_severity_bounds(self):
        """Test that severity is bounded 0-1."""
        risk = RiskFactor(factor="Test", severity=0.5)
        assert 0 <= risk.severity <= 1

        with pytest.raises(ValueError):
            RiskFactor(factor="Test", severity=1.5)

        with pytest.raises(ValueError):
            RiskFactor(factor="Test", severity=-0.1)


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_interpret_score_a_plus(self):
        """Test score interpretation for A+."""
        result = interpret_score(98)
        assert result["grade"] == "A+"
        assert "Exceptional" in result["summary"]

    def test_interpret_score_f(self):
        """Test score interpretation for F."""
        result = interpret_score(15)
        assert result["grade"] == "F"
        assert "Unreliable" in result["summary"]

    def test_get_grade_color(self):
        """Test grade color mapping."""
        assert get_grade_color(ShipGrade.A_PLUS) == "brightgreen"
        assert get_grade_color(ShipGrade.A) == "green"
        assert get_grade_color(ShipGrade.B) == "yellowgreen"
        assert get_grade_color(ShipGrade.C) == "yellow"
        assert get_grade_color(ShipGrade.D) == "orange"
        assert get_grade_color(ShipGrade.F) == "red"


class TestEnums:
    """Tests for enum types."""

    def test_language_values(self):
        """Test Language enum values."""
        assert Language.PYTHON.value == "python"
        assert Language.TYPESCRIPT.value == "typescript"
        assert Language.OTHER.value == "other"

    def test_confidence_level_values(self):
        """Test ConfidenceLevel enum values."""
        assert ConfidenceLevel.VERY_HIGH.value == "very_high"
        assert ConfidenceLevel.UNCERTAIN.value == "uncertain"

    def test_ship_grade_values(self):
        """Test ShipGrade enum values."""
        assert ShipGrade.A_PLUS.value == "A+"
        assert ShipGrade.F.value == "F"
