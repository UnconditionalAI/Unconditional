"""Integration tests for conversation endpoint.

Tests the full message processing pipeline end-to-end.
"""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestConversationEndpoint:
    """Integration tests for /api/v1 conversation endpoints."""

    def test_get_opening_message(self):
        """Opening message endpoint returns expected structure."""
        response = client.get("/api/v1/opening")

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "normal"
        assert "content" in data
        assert "timestamp" in data
        assert len(data["content"]) > 0

    def test_post_message_banned_content(self):
        """Messages with banned content are rejected."""
        response = client.post(
            "/api/v1/message",
            json={"content": "fuck you stupid bot"},
        )

        assert response.status_code == 400
        assert "inappropriate" in response.json()["detail"].lower()

    @patch("api.v1.endpoints.conversation.get_llm_service")
    def test_post_message_crisis_detection(self, mock_llm):
        """Crisis language triggers crisis response."""
        response = client.post(
            "/api/v1/message",
            json={"content": "I want to kill myself"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "crisis"
        assert "resources" in data
        assert len(data["resources"]) > 0
        assert data["session_locked"] is True

        # LLM should not be called for crisis messages
        mock_llm.assert_not_called()

    @patch("api.v1.endpoints.conversation.get_llm_service")
    def test_post_message_normal_flow(self, mock_llm):
        """Normal messages flow through full pipeline."""
        # Mock LLM response
        mock_service = MagicMock()
        mock_service.generate.return_value = (
            "I hear that you're feeling sad. What's making this moment difficult?"
        )
        mock_llm.return_value = mock_service

        response = client.post(
            "/api/v1/message",
            json={"content": "I'm feeling really sad today"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "normal"
        assert "content" in data
        assert len(data["content"]) > 0

        # LLM should have been called
        mock_llm.assert_called_once()
        mock_service.generate.assert_called_once()

    @patch("api.v1.endpoints.conversation.get_llm_service")
    def test_post_message_guardrails_applied(self, mock_llm):
        """Guardrails block inappropriate LLM responses."""
        # Mock LLM returning something that violates guardrails
        mock_service = MagicMock()
        mock_service.generate.return_value = (
            "You should definitely see a therapist about this."
        )
        mock_llm.return_value = mock_service

        response = client.post(
            "/api/v1/message",
            json={"content": "I'm struggling with my thoughts"},
        )

        assert response.status_code == 200
        data = response.json()
        # Response should be the guardrail replacement, not the LLM output
        assert "should" not in data["content"].lower()
        assert "hear what you're sharing" in data["content"].lower()

    def test_health_check(self):
        """Health check endpoint works."""
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
