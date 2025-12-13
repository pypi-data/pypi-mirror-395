"""Tests for the TPU Inference Client."""

import pytest
from unittest.mock import Mock, patch

from tpu_inference_server.client import TPUInferenceClient


class TestTPUInferenceClient:
    """Tests for TPUInferenceClient."""

    def test_init_default(self):
        """Test default initialization."""
        client = TPUInferenceClient()
        assert client.base_url == "http://localhost:8080"
        assert client.timeout == 300

    def test_init_custom(self):
        """Test custom initialization."""
        client = TPUInferenceClient("http://example.com:9000", timeout=60)
        assert client.base_url == "http://example.com:9000"
        assert client.timeout == 60

    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is stripped from base_url."""
        client = TPUInferenceClient("http://localhost:8080/")
        assert client.base_url == "http://localhost:8080"

    @patch("tpu_inference_server.client.requests.Session")
    def test_health(self, mock_session_class):
        """Test health check."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "device": "xla:0",
            "loaded_models": ["gpt2"],
        }
        mock_session.get.return_value = mock_response

        client = TPUInferenceClient()
        result = client.health()

        assert result["status"] == "healthy"
        mock_session.get.assert_called_once()

    @patch("tpu_inference_server.client.requests.Session")
    def test_generate(self, mock_session_class):
        """Test text generation."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "generated_text": "Hello world!",
            "model": "gpt2",
        }
        mock_session.post.return_value = mock_response

        client = TPUInferenceClient()
        result = client.generate("Hello", max_new_tokens=10)

        assert result["generated_text"] == "Hello world!"
        mock_session.post.assert_called_once()

    @patch("tpu_inference_server.client.requests.Session")
    def test_chat(self, mock_session_class):
        """Test chat completion."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "chatcmpl-123",
            "choices": [{"message": {"role": "assistant", "content": "Hi!"}}],
        }
        mock_session.post.return_value = mock_response

        client = TPUInferenceClient()
        result = client.chat([{"role": "user", "content": "Hello"}])

        assert result["choices"][0]["message"]["content"] == "Hi!"

    @patch("tpu_inference_server.client.requests.Session")
    def test_chat_simple(self, mock_session_class):
        """Test simple chat interface."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "chatcmpl-123",
            "choices": [{"message": {"role": "assistant", "content": "I'm fine!"}}],
        }
        mock_session.post.return_value = mock_response

        client = TPUInferenceClient()
        result = client.chat_simple("How are you?")

        assert result == "I'm fine!"

    @patch("tpu_inference_server.client.requests.Session")
    def test_is_healthy_true(self, mock_session_class):
        """Test is_healthy returns True when healthy."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy"}
        mock_session.get.return_value = mock_response

        client = TPUInferenceClient()
        assert client.is_healthy() is True

    @patch("tpu_inference_server.client.requests.Session")
    def test_is_healthy_false_on_error(self, mock_session_class):
        """Test is_healthy returns False on error."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.get.side_effect = Exception("Connection error")

        client = TPUInferenceClient()
        assert client.is_healthy() is False
