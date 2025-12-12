"""Tests for the main OpenDota client."""

import sys

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota
from opendota.exceptions import OpenDotaNotFoundError


class TestOpenDota:
    """Test cases for the main client."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    def test_client_initialization(self):
        """Test client initialization."""
        client = OpenDota()
        assert client.BASE_URL == "https://api.opendota.com/api"
        assert client.timeout == 30.0
        assert client.api_key is None
        assert client.format == 'pydantic'
        assert client.auth_method == 'header'  # Default auth method

        # Test with API key and format
        client_with_options = OpenDota(api_key="test_key", format='json')
        assert client_with_options.api_key == "test_key"
        assert client_with_options.format == 'json'
        assert client_with_options.auth_method == 'header'

        # Test with query auth method
        client_query_auth = OpenDota(api_key="test_key", auth_method='query')
        assert client_query_auth.api_key == "test_key"
        assert client_query_auth.auth_method == 'query'

    def test_client_with_env_api_key(self, monkeypatch):
        """Test client reads API key from environment."""
        monkeypatch.setenv("OPENDOTA_API_KEY", "env_key")
        client = OpenDota()
        assert client.api_key == "env_key"

    @pytest.mark.asyncio
    async def test_client_methods_exist(self, client):
        """Test that all methods are available directly on client."""
        # Match methods
        assert hasattr(client, "get_match")
        assert hasattr(client, "get_public_matches")
        assert hasattr(client, "get_pro_matches")

        # Player methods
        assert hasattr(client, "get_player")
        assert hasattr(client, "get_player_matches")

        # Hero methods
        assert hasattr(client, "get_heroes")
        assert hasattr(client, "get_hero_stats")

    @pytest.mark.asyncio
    async def test_request_method_real_api(self, client):
        """Test the internal request method with real API."""
        # Test a simple endpoint that should always work
        response = await client.get("heroes")

        assert isinstance(response, list)
        assert len(response) > 0

        # Verify hero structure
        first_hero = response[0]
        assert "id" in first_hero
        assert "name" in first_hero
        assert "localized_name" in first_hero

    @pytest.mark.asyncio
    async def test_404_error_handling(self, client):
        """Test 404 error handling."""
        with pytest.raises(OpenDotaNotFoundError):
            await client.get("nonexistent_endpoint")

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test client as async context manager."""
        async with OpenDota() as client:
            response = await client.get("heroes")
            assert isinstance(response, list)

        # Client should be closed after context manager
        assert client._client is None

    @pytest.mark.asyncio
    async def test_manual_close(self):
        """Test manual client closing."""
        client = OpenDota()
        await client.close()
        assert client._client is None

    @pytest.mark.asyncio
    async def test_timeout_setting(self):
        """Test custom timeout setting."""
        client = OpenDota(timeout=60.0)
        assert client.timeout == 60.0
        # Timeout is set on the client itself
        await client.close()
