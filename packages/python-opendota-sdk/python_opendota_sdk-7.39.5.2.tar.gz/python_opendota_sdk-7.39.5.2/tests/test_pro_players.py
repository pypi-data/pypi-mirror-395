"""Tests for pro players endpoints using Golden Master approach with real data."""

import sys

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota


class TestProPlayers:
    """Test cases for pro players endpoints using real expected values."""

    @pytest.fixture
    async def client(self):
        """Create a test client with JSON format for dict access."""
        async with OpenDota(format="json") as client:
            yield client

    @pytest.mark.asyncio
    async def test_get_pro_players_returns_list(self, client):
        """Test get_pro_players returns a list of players."""
        players = await client.get_pro_players()

        assert isinstance(players, list)
        assert len(players) > 500, "Should have many pro players registered"

    @pytest.mark.asyncio
    async def test_pro_players_have_expected_structure(self, client):
        """Test pro players have expected fields."""
        players = await client.get_pro_players()

        # Check first player has required fields
        player = players[0]
        assert "account_id" in player

    @pytest.mark.asyncio
    async def test_pro_players_have_valid_ids(self, client):
        """Test that pro players have valid account IDs."""
        players = await client.get_pro_players()

        # All players should have account_id
        for player in players[:100]:
            assert player.get("account_id") is not None
            assert player.get("account_id") > 0

        # Check for unique account IDs (no duplicates)
        account_ids = [p["account_id"] for p in players]
        assert len(account_ids) == len(set(account_ids)), "Account IDs should be unique"

    @pytest.mark.asyncio
    async def test_pro_players_have_team_info(self, client):
        """Test that some pro players have team information."""
        players = await client.get_pro_players()

        # At least some players should have team_id
        players_with_team = [p for p in players if p.get("team_id")]
        assert len(players_with_team) > 100, "Many pro players should have team affiliations"

    @pytest.mark.asyncio
    async def test_pro_players_have_names(self, client):
        """Test that pro players have name data."""
        players = await client.get_pro_players()

        # Most players should have a name or personaname
        players_with_name = [
            p for p in players
            if p.get("name") or p.get("personaname")
        ]
        assert len(players_with_name) > len(players) * 0.9, "Most pro players should have names"

    @pytest.mark.asyncio
    async def test_pro_players_fantasy_roles(self, client):
        """Test that some players have fantasy role data."""
        players = await client.get_pro_players()

        # Some players should have fantasy_role (1=Core, 2=Support)
        players_with_role = [p for p in players if p.get("fantasy_role") in [1, 2]]
        assert len(players_with_role) > 50, "Many pro players should have fantasy roles"

        # Check role distribution
        cores = [p for p in players_with_role if p.get("fantasy_role") == 1]
        supports = [p for p in players_with_role if p.get("fantasy_role") == 2]
        assert len(cores) > 0, "Should have core players"
        assert len(supports) > 0, "Should have support players"

    @pytest.mark.asyncio
    async def test_pro_players_country_codes(self, client):
        """Test that some players have country information."""
        players = await client.get_pro_players()

        # Some players should have country_code
        players_with_country = [p for p in players if p.get("country_code")]
        assert len(players_with_country) > 100, "Many pro players should have country codes"
