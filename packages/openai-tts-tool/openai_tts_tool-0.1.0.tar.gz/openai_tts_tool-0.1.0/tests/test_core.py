"""
Tests for OpenAI TTS tool core functionality.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from openai import APIStatusError, OpenAIError

from openai_tts_tool.core import get_api_info, get_openai_client, test_credentials


class TestGetOpenAIClient:
    """Test cases for get_openai_client function."""

    def test_get_openai_client_success(self):
        """Test successful client creation with valid API key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123"}):
            client = get_openai_client()
            assert client is not None
            assert hasattr(client, "api_key")

    def test_get_openai_client_missing_key(self):
        """Test error when OPENAI_API_KEY is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                EnvironmentError, match="OPENAI_API_KEY environment variable is not set"
            ):
                get_openai_client()

    def test_get_openai_client_empty_key(self):
        """Test error when OPENAI_API_KEY is empty."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with pytest.raises(ValueError, match="OPENAI_API_KEY is set but empty"):
                get_openai_client()

    def test_get_openai_client_invalid_format(self):
        """Test error when API key format is invalid."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key"}):
            with pytest.raises(ValueError, match="OPENAI_API_KEY format is invalid"):
                get_openai_client()

    @patch("openai.OpenAI")
    def test_get_openai_client_authentication_error(self, mock_openai):
        """Test handling of OpenAI authentication errors."""
        # Mock the client to raise APIStatusError when accessed
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Simulate authentication error on first client operation
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_client.models.list.side_effect = APIStatusError(
            message="Invalid API key",
            response=mock_response,
            body={"error": {"message": "Invalid API key"}},
        )

        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123"}):
            # This should succeed at client creation but fail when used
            client = get_openai_client()
            with pytest.raises(APIStatusError):
                client.models.list()

    @patch("openai.OpenAI")
    def test_get_openai_client_openai_error(self, mock_openai):
        """Test handling of general OpenAI errors."""
        # Mock the client to raise OpenAIError when accessed
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Simulate general OpenAI error on first client operation
        mock_client.models.list.side_effect = OpenAIError("Network error")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123"}):
            # This should succeed at client creation but fail when used
            client = get_openai_client()
            with pytest.raises(OpenAIError):
                client.models.list()


class TestTestCredentials:
    """Test cases for test_credentials function."""

    @patch("openai_tts_tool.core.client.get_openai_client")
    def test_test_credentials_success(self, mock_get_client):
        """Test successful credential testing."""
        mock_client = MagicMock()
        mock_client.models.list.return_value = MagicMock()
        mock_get_client.return_value = mock_client

        result = test_credentials()
        assert result is True
        mock_client.models.list.assert_called_once()

    @patch("openai_tts_tool.core.client.get_openai_client")
    def test_test_credentials_authentication_error(self, mock_get_client):
        """Test credential testing with authentication error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get_client.side_effect = APIStatusError(
            message="Invalid key",
            response=mock_response,
            body={"error": {"message": "Invalid key"}},
        )

        with pytest.raises(APIStatusError, match="OpenAI API credentials are invalid or inactive"):
            test_credentials()

    @patch("openai_tts_tool.core.client.get_openai_client")
    def test_test_credentials_openai_error(self, mock_get_client):
        """Test credential testing with general OpenAI error."""
        mock_get_client.side_effect = OpenAIError("Network error")

        with pytest.raises(OpenAIError, match="Failed to test OpenAI credentials"):
            test_credentials()


class TestGetApiInfo:
    """Test cases for get_api_info function."""

    @patch("openai_tts_tool.core.client.get_openai_client")
    def test_get_api_info_success(self, mock_get_client):
        """Test successful API info retrieval."""
        mock_client = MagicMock()
        mock_models = MagicMock()
        mock_models.data = [
            MagicMock(id="tts-1"),
            MagicMock(id="tts-1-hd"),
            MagicMock(id="gpt-4"),
        ]
        mock_client.models.list.return_value = mock_models
        mock_get_client.return_value = mock_client

        info = get_api_info()

        assert info["api_status"] == "connected"
        assert info["models_count"] == 3
        assert "tts-1" in info["available_tts_models"]
        assert "tts-1-hd" in info["available_tts_models"]
        assert "gpt-4" not in info["available_tts_models"]  # Should filter TTS only

    @patch("openai_tts_tool.core.client.get_openai_client")
    def test_get_api_info_openai_error(self, mock_get_client):
        """Test API info retrieval with OpenAI error."""
        mock_get_client.side_effect = OpenAIError("API error")

        with pytest.raises(OpenAIError, match="Failed to retrieve OpenAI API information"):
            get_api_info()
