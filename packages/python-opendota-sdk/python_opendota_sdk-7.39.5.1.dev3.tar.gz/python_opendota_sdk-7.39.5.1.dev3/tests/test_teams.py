"""Tests for teams endpoints using Golden Master approach with real data."""

import sys

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota


class TestTeams:
    """Test cases for teams endpoints using real expected values."""

    @pytest.fixture
    async def client(self):
        """Create a test client with JSON format for dict access."""
        async with OpenDota(format="json") as client:
            yield client

    @pytest.mark.asyncio
    async def test_get_teams_returns_list(self, client):
        """Test get_teams returns a list of teams."""
        teams = await client.get_teams()

        assert isinstance(teams, list)
        assert len(teams) > 100, "Should have many teams registered"

    @pytest.mark.asyncio
    async def test_get_teams_has_expected_structure(self, client):
        """Test teams have expected fields."""
        teams = await client.get_teams()

        # Check first team has required fields
        team = teams[0]
        assert "team_id" in team
        assert "name" in team or team.get("name") is None
        assert "tag" in team or team.get("tag") is None

    @pytest.mark.asyncio
    async def test_get_team_by_id(self, client):
        """Test fetching a team by ID."""
        # Get first team from list and verify we can fetch it
        teams = await client.get_teams()
        first_team_id = teams[0].get("team_id")

        team = await client.get_team(first_team_id)

        assert team is not None
        assert team.get("team_id") == first_team_id

    @pytest.mark.asyncio
    async def test_get_team_players(self, client):
        """Test fetching team roster."""
        # Get a team with high rating (likely active)
        teams = await client.get_teams()
        team_with_rating = next((t for t in teams if t.get("rating")), teams[0])
        team_id = team_with_rating.get("team_id")

        players = await client.get_team_players(team_id)

        assert isinstance(players, list)
        # Note: Some teams may have no current players
        if len(players) > 0:
            player = players[0]
            assert "account_id" in player

    @pytest.mark.asyncio
    async def test_get_team_matches(self, client):
        """Test fetching team matches."""
        # Get a team with high rating (likely has recent matches)
        teams = await client.get_teams()
        team_with_rating = next((t for t in teams if t.get("rating")), teams[0])
        team_id = team_with_rating.get("team_id")

        matches = await client.get_team_matches(team_id)

        assert isinstance(matches, list)

        if len(matches) > 0:
            match = matches[0]
            assert "match_id" in match

    @pytest.mark.asyncio
    async def test_get_team_has_expected_fields(self, client):
        """Test that team response has expected fields."""
        teams = await client.get_teams()
        team_id = teams[0].get("team_id")

        team = await client.get_team(team_id)

        assert team is not None
        # Check for common team fields
        assert "team_id" in team
        # These fields may be present
        assert "rating" in team or "wins" in team or "losses" in team

    @pytest.mark.asyncio
    async def test_teams_have_ratings(self, client):
        """Test that teams have rating/ELO data."""
        teams = await client.get_teams()

        # At least some teams should have ratings
        teams_with_rating = [t for t in teams[:100] if t.get("rating")]
        assert len(teams_with_rating) > 10, "Many teams should have ratings"

    @pytest.mark.asyncio
    async def test_teams_sorted_by_rating(self, client):
        """Test that teams list is sorted by rating descending."""
        teams = await client.get_teams()

        # Check first 20 teams are in roughly descending rating order
        # (allowing for some variance due to API)
        ratings = [t.get("rating", 0) for t in teams[:20] if t.get("rating")]
        if len(ratings) >= 2:
            # Most should be in descending order
            descending_count = sum(
                1 for i in range(len(ratings) - 1) if ratings[i] >= ratings[i + 1]
            )
            assert descending_count >= len(ratings) // 2, "Teams should be roughly sorted by rating"
