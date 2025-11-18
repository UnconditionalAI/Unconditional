"""Unit tests for response guardrails.

100% coverage required. Vulnerable humans depend on it.
"""

from safety.guardrails import apply_guardrails, check_length


class TestGuardrails:
    """Tests for LLM output guardrails."""

    def test_block_diagnosis(self):
        """Diagnostic language is blocked."""
        response = "You might have depression or anxiety disorder."
        result = apply_guardrails(response)
        assert result != response
        assert "hear what you're sharing" in result.lower()

    def test_block_prescriptive_advice(self):
        """Prescriptive advice is blocked."""
        responses = [
            "You should go see a therapist",
            "You must stop thinking this way",
            "You need to exercise more",
        ]
        for response in responses:
            result = apply_guardrails(response)
            assert result != response, f"Failed to block: {response}"

    def test_block_false_intimacy(self):
        """False intimacy language is blocked."""
        responses = [
            "I love you and care deeply about you",
            "You're special to me",
            "We're friends",
        ]
        for response in responses:
            result = apply_guardrails(response)
            assert result != response, f"Failed to block: {response}"

    def test_block_promises(self):
        """Promises are blocked."""
        responses = [
            "I promise it will get better",
            "I guarantee you'll feel better",
            "Everything will be okay",
        ]
        for response in responses:
            result = apply_guardrails(response)
            assert result != response, f"Failed to block: {response}"

    def test_block_spiritual_claims(self):
        """Spiritual/metaphysical claims are blocked."""
        responses = [
            "God has a plan for you",
            "Everything happens for a reason",
            "The universe has a plan",
        ]
        for response in responses:
            result = apply_guardrails(response)
            assert result != response, f"Failed to block: {response}"

    def test_block_flattery(self):
        """Flattery is blocked."""
        responses = [
            "You're so strong and brave",
            "I'm so proud of you",
        ]
        for response in responses:
            result = apply_guardrails(response)
            assert result != response, f"Failed to block: {response}"

    def test_allow_safe_response(self):
        """Safe responses pass through unchanged."""
        response = (
            "I hear that you're feeling overwhelmed. "
            "What's making this moment particularly difficult?"
        )
        result = apply_guardrails(response)
        assert result == response

    def test_check_length_normal(self):
        """Normal-length responses pass through."""
        response = "This is a normal response."
        result = check_length(response)
        assert result == response

    def test_check_length_truncate(self):
        """Overly long responses are truncated."""
        response = "a " * 300  # 600 characters
        result = check_length(response, max_length=100)
        assert len(result) <= 100
        assert result.endswith("...")

    def test_case_insensitive(self):
        """Guardrail matching is case-insensitive."""
        response1 = "YOU SHOULD see a therapist"
        response2 = "you should see a therapist"

        result1 = apply_guardrails(response1)
        result2 = apply_guardrails(response2)

        assert result1 != response1
        assert result2 != response2
