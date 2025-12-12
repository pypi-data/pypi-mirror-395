"""Tests for matches endpoints using Golden Master approach with real data."""

import sys
from datetime import datetime

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota
from opendota.exceptions import OpenDotaNotFoundError


class TestMatches:
    """Test cases for matches endpoints using real expected values."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_get_match_8461956309_golden_master(self, client):
        """Test getting match 8461956309 with exact expected values."""
        match_id = 8461956309

        match = await client.get_match(match_id)

        # Test exact match properties from real data
        assert match.match_id == 8461956309
        assert match.duration == 3512
        assert match.radiant_win is False
        assert match.radiant_score == 11
        assert match.dire_score == 24
        assert match.start_time == 1757872818
        assert match.game_mode == 2
        assert match.lobby_type == 1
        assert len(match.players) == 10

        # Test datetime conversion
        expected_datetime = datetime.fromtimestamp(1757872818)
        assert match.start_datetime == expected_datetime

        # Test exact player data from real match
        players = match.players

        # Player 0 (Radiant, slot 0, Juggernaut)
        p0 = players[0]
        assert p0.account_id == 898754153
        assert p0.player_slot == 0
        assert p0.hero_id == 8  # Juggernaut
        assert p0.kills == 4
        assert p0.deaths == 3
        assert p0.assists == 1
        assert p0.last_hits == 866
        assert p0.denies == 11
        assert p0.gold_per_min == 769
        assert p0.xp_per_min == 812

        # Player 1 (Radiant, slot 1, Shadow Fiend)
        p1 = players[1]
        assert p1.account_id == 137129583
        assert p1.player_slot == 1
        assert p1.hero_id == 11  # Shadow Fiend
        assert p1.kills == 3
        assert p1.deaths == 3
        assert p1.assists == 6
        assert p1.last_hits == 632

        # Player 5 (Dire, slot 128, Keeper of the Light)
        p5 = players[5]
        assert p5.account_id == 10366616
        assert p5.player_slot == 128  # Dire team starts at 128
        assert p5.hero_id == 89  # Keeper of the Light
        assert p5.kills == 1
        assert p5.deaths == 0
        assert p5.assists == 15
        assert p5.last_hits == 282

        # Player 9 (Dire, slot 132, Rubick)
        p9 = players[9]
        assert p9.account_id == 25907144
        assert p9.player_slot == 132
        assert p9.hero_id == 87  # Rubick
        assert p9.kills == 7
        assert p9.deaths == 3
        assert p9.assists == 16
        assert p9.last_hits == 30  # Support, low last hits

        # Test team composition - exactly 5 Radiant (slots 0-4) and 5 Dire (slots 128-132)
        radiant_players = [p for p in players if p.player_slot < 128]
        dire_players = [p for p in players if p.player_slot >= 128]
        assert len(radiant_players) == 5
        assert len(dire_players) == 5

        # Test total kills match team scores
        radiant_kills = sum(p.kills for p in radiant_players)
        dire_kills = sum(p.kills for p in dire_players)
        assert radiant_kills == match.radiant_score  # 11
        assert dire_kills == match.dire_score  # 24

    @pytest.mark.asyncio
    async def test_public_matches_structure_validation(self, client):
        """Test public matches return expected structure and reasonable values."""
        matches = await client.get_public_matches()

        # Should return exactly 100 matches (API default)
        assert len(matches) == 100

        # Test first match has required fields with realistic values
        first_match = matches[0]
        assert first_match.match_id > 8000000000  # Recent match IDs are very large
        # Duration can be 0 for abandoned matches, otherwise should be reasonable
        assert first_match.duration >= 0  # Can be 0 for abandoned/invalid
        assert first_match.duration <= 10800  # Max 3 hours
        # Game mode and lobby type can vary widely
        assert first_match.game_mode >= 0
        assert first_match.lobby_type >= 0

        # All matches should have recent timestamps (within last month)
        recent_timestamp = 1757000000  # Approximately recent
        assert first_match.start_time > recent_timestamp

        # Match sequence numbers should exist and be reasonable
        match_seqs = [m.match_seq_num for m in matches if m.match_seq_num is not None]
        if match_seqs:
            # All sequence numbers should be positive and large (recent matches)
            for seq in match_seqs:
                assert seq > 7000000000, f"Match sequence {seq} seems too old"

    @pytest.mark.asyncio
    async def test_pro_matches_business_logic(self, client):
        """Test professional matches have expected professional characteristics."""
        pro_matches = await client.get_pro_matches()

        # Should return 100 matches (API default)
        assert len(pro_matches) == 100

        first_match = pro_matches[0]

        # Pro matches should have team information
        team_names_exist = (
            first_match.radiant_name is not None or
            first_match.dire_name is not None or
            first_match.radiant_team_id is not None or
            first_match.dire_team_id is not None
        )
        assert team_names_exist, "Pro match should have team information"

        # Pro matches should have reasonable durations (not too short)
        assert first_match.duration >= 600, "Pro matches should be at least 10 minutes"

        # League information should exist for pro matches
        has_league_info = (
            first_match.leagueid is not None or
            first_match.league_name is not None
        )
        assert has_league_info, "Pro match should have league information"

    @pytest.mark.asyncio
    async def test_match_not_found_error_handling(self, client):
        """Test proper error handling for non-existent matches."""
        fake_match_id = 999999999999999

        with pytest.raises(OpenDotaNotFoundError) as exc_info:
            await client.get_match(fake_match_id)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_parsed_matches_data_consistency(self, client):
        """Test parsed matches return consistent data structure."""
        parsed_matches = await client.get_parsed_matches()

        # API may return empty list if no recent parsed matches
        if parsed_matches:
            # Should be list of dicts (raw data)
            first_parsed = parsed_matches[0]
            assert "match_id" in first_parsed
            assert isinstance(first_parsed["match_id"], int)
            assert first_parsed["match_id"] > 0
