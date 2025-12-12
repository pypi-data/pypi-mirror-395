"""Tests for leagues endpoints using Golden Master approach with real data."""

import sys

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota


class TestLeagues:
    """Test cases for leagues endpoints using real expected values."""

    @pytest.fixture
    async def client(self):
        """Create a test client with JSON format for dict access."""
        async with OpenDota(format="json") as client:
            yield client

    @pytest.mark.asyncio
    async def test_get_leagues_returns_list(self, client):
        """Test get_leagues returns a list of leagues."""
        leagues = await client.get_leagues()

        assert isinstance(leagues, list)
        assert len(leagues) > 100, "Should have many leagues registered"

    @pytest.mark.asyncio
    async def test_leagues_have_expected_structure(self, client):
        """Test leagues have expected fields."""
        leagues = await client.get_leagues()

        # Check first league has required fields
        league = leagues[0]
        assert "leagueid" in league

    @pytest.mark.asyncio
    async def test_leagues_have_tiers(self, client):
        """Test that leagues have tier information."""
        leagues = await client.get_leagues()

        # Count leagues by tier
        premium = [lg for lg in leagues if lg.get("tier") == "premium"]
        professional = [lg for lg in leagues if lg.get("tier") == "professional"]

        # Should have leagues in different tiers
        assert len(premium) > 0, "Should have premium leagues (TI, Majors)"
        assert len(professional) > 0, "Should have professional leagues"

    @pytest.mark.asyncio
    async def test_leagues_have_names(self, client):
        """Test that most leagues have names."""
        leagues = await client.get_leagues()

        leagues_with_name = [lg for lg in leagues if lg.get("name")]
        assert len(leagues_with_name) > len(leagues) * 0.5, "Most leagues should have names"

    @pytest.mark.asyncio
    async def test_get_league_by_id(self, client):
        """Test fetching a specific league."""
        # Use a known league ID - this may need updating
        leagues = await client.get_leagues()

        if len(leagues) > 0:
            league_id = leagues[0].get("leagueid")
            league = await client.get_league(league_id)

            assert league is not None
            assert league.get("leagueid") == league_id

    @pytest.mark.asyncio
    async def test_get_league_matches(self, client):
        """Test fetching matches from a league."""
        leagues = await client.get_leagues()

        # Find a premium league that likely has matches
        premium_leagues = [lg for lg in leagues if lg.get("tier") == "premium"]

        if len(premium_leagues) > 0:
            league_id = premium_leagues[0].get("leagueid")
            matches = await client.get_league_matches(league_id, limit=10)

            assert isinstance(matches, list)
            # Premium leagues should have matches
            # (though some very old ones might not)

    @pytest.mark.asyncio
    async def test_get_league_teams(self, client):
        """Test fetching teams from a league."""
        leagues = await client.get_leagues()

        # Find a premium league
        premium_leagues = [lg for lg in leagues if lg.get("tier") == "premium"]

        if len(premium_leagues) > 0:
            league_id = premium_leagues[0].get("leagueid")
            teams = await client.get_league_teams(league_id)

            assert isinstance(teams, list)

    @pytest.mark.asyncio
    async def test_premium_leagues_are_major_tournaments(self, client):
        """Test that premium tier contains major tournaments."""
        leagues = await client.get_leagues()

        premium = [lg for lg in leagues if lg.get("tier") == "premium"]
        premium_names = [lg.get("name", "").lower() for lg in premium]

        # Check for known major tournament patterns
        has_ti = any("international" in name for name in premium_names)
        has_major = any("major" in name for name in premium_names)
        has_esl = any("esl" in name for name in premium_names)

        # At least one major tournament type should exist
        assert has_ti or has_major or has_esl, "Premium tier should include major tournaments"
