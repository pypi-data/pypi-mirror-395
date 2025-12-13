"""Tests for players endpoints using Golden Master approach with real data."""

import sys
from datetime import datetime

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota
from opendota.exceptions import OpenDotaNotFoundError


class TestPlayers:
    """Test cases for players endpoints using real expected values."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_dendi_profile_golden_master(self, client):
        """Test Dendi's profile returns exact expected data."""
        # Dendi's account ID - well-known professional player
        account_id = 70388657

        player = await client.get_player(account_id)

        # Test profile data from real API (some fields may change over time)
        assert player.profile.account_id == 70388657
        assert player.profile.name == "Dendi"  # Real name doesn't change
        # personaname can change - just check it exists
        assert player.profile.personaname is not None
        assert len(player.profile.personaname) > 0
        assert player.profile.plus is True
        assert player.profile.loccountrycode == "UA"  # Ukraine

        # Test that he has a rank (high skill player)
        assert player.rank_tier is not None
        assert player.rank_tier >= 70  # At least Ancient rank
        # Leaderboard rank can change
        if player.leaderboard_rank is not None:
            assert player.leaderboard_rank > 0

        # Test computed rating should be None or a reasonable value
        if player.computed_rating is not None:
            assert player.computed_rating > 5000  # High MMR player

        # Test Steam profile fields
        assert player.profile.steamid is not None
        assert player.profile.steamid.startswith("7656119")  # Steam ID format
        assert player.profile.avatar is not None
        assert "steamstatic.com" in player.profile.avatar

        # Test contributor status (Dendi is well-known)
        assert player.profile.is_contributor is False  # Not an OpenDota contributor
        assert player.profile.is_subscriber is False   # Not a Plus subscriber in API

    @pytest.mark.asyncio
    async def test_dendi_recent_matches_golden_master(self, client):
        """Test Dendi's recent matches return expected data structure."""
        account_id = 70388657

        matches = await client.get_player_matches(account_id, limit=3)

        # Should return exactly 3 matches as requested
        assert len(matches) == 3

        # Test first match (most recent) - Match 8449874074
        recent_match = matches[0]
        assert recent_match.match_id == 8449874074
        assert recent_match.hero_id == 97  # Magnus
        assert recent_match.kills == 11
        assert recent_match.deaths == 1
        assert recent_match.assists == 16
        assert recent_match.radiant_win is True
        assert recent_match.duration == 1886
        assert recent_match.party_size == 10  # Full lobby party

        # Test datetime conversion
        expected_datetime = datetime.fromtimestamp(recent_match.start_time)
        assert recent_match.start_datetime == expected_datetime

        # Test that all matches have required fields
        for match in matches:
            assert match.match_id > 8000000000  # Recent match IDs
            assert 1 <= match.hero_id <= 140  # Valid hero ID range
            assert 0 <= match.kills <= 50  # Reasonable kill range
            assert 0 <= match.deaths <= 50  # Reasonable death range
            assert 0 <= match.assists <= 100  # Reasonable assist range
            assert 600 <= match.duration <= 7200  # 10 minutes to 2 hours
            assert isinstance(match.radiant_win, bool)
            assert match.start_time > 1700000000  # Recent timestamp

    @pytest.mark.asyncio
    async def test_player_matches_filtering_business_logic(self, client):
        """Test player match filtering works with real data."""
        account_id = 70388657

        # Test win filter
        wins = await client.get_player_matches(account_id, limit=5, win=1)
        losses = await client.get_player_matches(account_id, limit=5, win=0)

        # Should return some wins and losses for active player
        if wins:
            for match in wins:
                # Calculate if player was on winning team
                player_on_radiant = match.player_slot < 128
                is_win = (player_on_radiant and match.radiant_win) or (not player_on_radiant and not match.radiant_win)
                assert is_win, f"Match {match.match_id} should be a win but wasn't"

        if losses:
            for match in losses:
                # Calculate if player was on losing team
                player_on_radiant = match.player_slot < 128
                is_loss = (player_on_radiant and not match.radiant_win) or (not player_on_radiant and match.radiant_win)
                assert is_loss, f"Match {match.match_id} should be a loss but wasn't"

        # Test hero filter - get matches with specific hero
        hero_matches = await client.get_player_matches(account_id, limit=3, hero_id=97)  # Magnus

        if hero_matches:
            for match in hero_matches:
                assert match.hero_id == 97, f"Match {match.match_id} should be Magnus but was hero {match.hero_id}"

    @pytest.mark.asyncio
    async def test_player_slot_team_logic(self, client):
        """Test player slot correctly indicates team (Radiant/Dire)."""
        account_id = 70388657

        matches = await client.get_player_matches(account_id, limit=10)

        for match in matches:
            # Player slots 0-4 are Radiant, 128-132 are Dire
            if match.player_slot < 128:
                # Radiant player
                assert 0 <= match.player_slot <= 4, f"Invalid Radiant slot: {match.player_slot}"
            else:
                # Dire player
                assert 128 <= match.player_slot <= 132, f"Invalid Dire slot: {match.player_slot}"

    @pytest.mark.asyncio
    async def test_match_duration_constraints(self, client):
        """Test matches have realistic duration constraints."""
        account_id = 70388657

        matches = await client.get_player_matches(account_id, limit=20)

        for match in matches:
            # Real Dota 2 matches have these constraints
            assert 300 <= match.duration <= 10800, f"Match {match.match_id} duration {match.duration}s is unrealistic"

            # Most matches are between 20-60 minutes
            if 1200 <= match.duration <= 3600:
                # This is normal duration, no additional checks needed
                pass
            elif match.duration < 1200:
                # Short game - could be early surrender or stomp
                assert match.duration >= 300, "Even short games should be at least 5 minutes"
            else:
                # Long game - should be under 3 hours
                assert match.duration <= 10800, "Even very long games should be under 3 hours"

    @pytest.mark.asyncio
    async def test_player_not_found_error_handling(self, client):
        """Test proper error handling for non-existent players."""
        fake_account_id = 999999999

        with pytest.raises(OpenDotaNotFoundError) as exc_info:
            await client.get_player(fake_account_id)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_high_mmr_player_characteristics(self, client):
        """Test that high MMR players have expected characteristics."""
        account_id = 70388657  # Dendi - professional player

        player = await client.get_player(account_id)

        # High MMR players should have reasonable stats
        assert player.rank_tier is not None
        assert player.rank_tier >= 70  # At least Ancient rank

        # Should have leaderboard rank (top players)
        assert player.leaderboard_rank is not None
        assert player.leaderboard_rank > 0
        assert player.leaderboard_rank <= 10000  # Reasonable leaderboard position

        # Test recent match performance expectations
        matches = await client.get_player_matches(account_id, limit=10)

        if matches:
            # Calculate average KDA for skill assessment
            total_kills = sum(m.kills for m in matches)
            total_deaths = sum(m.deaths for m in matches)
            total_assists = sum(m.assists for m in matches)

            # High skill players should have reasonable KDA
            if total_deaths > 0:
                kda_ratio = (total_kills + total_assists) / total_deaths
                assert kda_ratio > 1.0, f"High MMR player should have KDA > 1.0, got {kda_ratio:.2f}"

    @pytest.mark.asyncio
    async def test_professional_player_plus_status(self, client):
        """Test professional player's OpenDota Plus status and features."""
        account_id = 70388657  # Dendi

        player = await client.get_player(account_id)

        # Dendi should have OpenDota Plus (professional player)
        assert player.profile.plus is True

        # Plus users should have enhanced profile data
        assert player.profile.name is not None  # Real name available
        assert player.profile.name == "Dendi"

        # Should have country code
        assert player.profile.loccountrycode is not None
        assert player.profile.loccountrycode == "UA"  # Ukraine
