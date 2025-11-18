"""Unit tests for crisis detection.

100% coverage required. Vulnerable humans depend on it.
"""

from safety.crisis_detection import detect_crisis


class TestCrisisDetection:
    """Tests for crisis language detection."""

    def test_detect_self_harm_explicit(self):
        """Explicit self-harm language triggers crisis detection."""
        result = detect_crisis("I want to kill myself")
        assert result.is_crisis is True
        assert result.severity == "high"

    def test_detect_self_harm_implicit(self):
        """Implicit self-harm language triggers crisis detection."""
        result = detect_crisis("I don't want to be here anymore")
        assert result.is_crisis is True

    def test_detect_suicide_ideation(self):
        """Suicide ideation triggers crisis detection."""
        messages = [
            "I'm thinking about suicide",
            "I wish I was dead",
            "I want to end my life",
            "better off dead",
        ]
        for msg in messages:
            result = detect_crisis(msg)
            assert result.is_crisis is True, f"Failed to detect crisis in: {msg}"

    def test_detect_immediate_danger(self):
        """Immediate danger escalates severity to critical."""
        result = detect_crisis("I'm going to kill myself tonight")
        assert result.is_crisis is True
        assert result.severity == "critical"

    def test_detect_harm_to_others(self):
        """Harm to others triggers crisis detection."""
        messages = [
            "I want to hurt them",
            "I'm going to kill him",
            "murder",
        ]
        for msg in messages:
            result = detect_crisis(msg)
            assert result.is_crisis is True, f"Failed to detect crisis in: {msg}"

    def test_safe_message(self):
        """Safe messages do not trigger crisis detection."""
        messages = [
            "I'm feeling sad today",
            "I'm struggling with anxiety",
            "I feel alone",
            "Everything is overwhelming",
        ]
        for msg in messages:
            result = detect_crisis(msg)
            assert result.is_crisis is False, (
                f"False positive crisis detection in: {msg}"
            )
            assert result.severity == "none"

    def test_case_insensitive(self):
        """Crisis detection is case-insensitive."""
        result1 = detect_crisis("I WANT TO KILL MYSELF")
        result2 = detect_crisis("i want to kill myself")
        result3 = detect_crisis("I WaNt To KiLl MySeLf")

        assert result1.is_crisis is True
        assert result2.is_crisis is True
        assert result3.is_crisis is True

    def test_matched_patterns_logged(self):
        """Matched patterns are logged for transparency."""
        result = detect_crisis("I'm going to kill myself tonight")
        assert len(result.matched_patterns) > 0
        assert result.reason != ""
