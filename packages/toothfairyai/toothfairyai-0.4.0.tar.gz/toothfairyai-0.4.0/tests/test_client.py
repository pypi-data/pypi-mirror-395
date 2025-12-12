"""Tests for the ToothFairyClient."""

import pytest

from toothfairyai import (
    ToothFairyClient,
    ToothFairyError,
    MissingApiKeyError,
    MissingWorkspaceIdError,
)


class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_initialization_with_valid_credentials(self):
        """Test that client initializes with valid credentials."""
        client = ToothFairyClient(
            api_key="test-api-key",
            workspace_id="test-workspace-id",
        )
        assert client.config.api_key == "test-api-key"
        assert client.config.workspace_id == "test-workspace-id"

    def test_client_initialization_with_custom_urls(self):
        """Test that client accepts custom URLs."""
        client = ToothFairyClient(
            api_key="test-api-key",
            workspace_id="test-workspace-id",
            base_url="https://custom-api.example.com",
            ai_url="https://custom-ai.example.com",
            ai_stream_url="https://custom-stream.example.com",
        )
        assert client.config.base_url == "https://custom-api.example.com"
        assert client.config.ai_url == "https://custom-ai.example.com"
        assert client.config.ai_stream_url == "https://custom-stream.example.com"

    def test_client_initialization_with_custom_timeout(self):
        """Test that client accepts custom timeout."""
        client = ToothFairyClient(
            api_key="test-api-key",
            workspace_id="test-workspace-id",
            timeout=300,
        )
        assert client.config.timeout == 300

    def test_client_raises_error_without_api_key(self):
        """Test that client raises error without API key."""
        with pytest.raises(MissingApiKeyError):
            ToothFairyClient(api_key="", workspace_id="test-workspace-id")

    def test_client_raises_error_without_workspace_id(self):
        """Test that client raises error without workspace ID."""
        with pytest.raises(MissingWorkspaceIdError):
            ToothFairyClient(api_key="test-api-key", workspace_id="")

    def test_client_has_all_managers(self):
        """Test that client has all manager instances."""
        client = ToothFairyClient(
            api_key="test-api-key",
            workspace_id="test-workspace-id",
        )
        assert hasattr(client, "chat")
        assert hasattr(client, "streaming")
        assert hasattr(client, "documents")
        assert hasattr(client, "entities")
        assert hasattr(client, "folders")
        assert hasattr(client, "prompts")

    def test_client_default_urls(self):
        """Test that client uses default URLs."""
        client = ToothFairyClient(
            api_key="test-api-key",
            workspace_id="test-workspace-id",
        )
        assert client.config.base_url == "https://api.toothfairyai.com"
        assert client.config.ai_url == "https://ai.toothfairyai.com"
        assert client.config.ai_stream_url == "https://ais.toothfairyai.com"

    def test_client_default_timeout(self):
        """Test that client uses default timeout."""
        client = ToothFairyClient(
            api_key="test-api-key",
            workspace_id="test-workspace-id",
        )
        assert client.config.timeout == 120


class TestClientMethods:
    """Tests for client methods."""

    def test_get_streaming_url(self):
        """Test get_streaming_url returns correct URL."""
        client = ToothFairyClient(
            api_key="test-api-key",
            workspace_id="test-workspace-id",
            ai_stream_url="https://custom-stream.example.com",
        )
        assert client.get_streaming_url() == "https://custom-stream.example.com"
