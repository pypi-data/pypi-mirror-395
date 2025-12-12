"""Tests for heroes endpoints using Golden Master approach with real data."""

import sys

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota


class TestHeroes:
    """Test cases for heroes endpoints using real expected values."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_heroes_exact_data_golden_master(self, client):
        """Test heroes endpoint returns exact expected data from real API."""
        heroes = await client.get_heroes()

        # Dota 2 has exactly 126 heroes as of this API version
        assert len(heroes) == 126

        # Test exact first three heroes (always consistent order)
        # Hero 0: Anti-Mage (id=1)
        antimage = heroes[0]
        assert antimage.id == 1
        assert antimage.name == "npc_dota_hero_antimage"
        assert antimage.localized_name == "Anti-Mage"
        assert antimage.primary_attr == "agi"
        assert antimage.attack_type == "Melee"
        assert "Carry" in antimage.roles
        assert "Escape" in antimage.roles
        assert "Nuker" in antimage.roles
        assert antimage.legs == 2

        # Hero 1: Axe (id=2)
        axe = heroes[1]
        assert axe.id == 2
        assert axe.name == "npc_dota_hero_axe"
        assert axe.localized_name == "Axe"
        assert axe.primary_attr == "str"
        assert axe.attack_type == "Melee"
        assert "Initiator" in axe.roles
        assert "Durable" in axe.roles
        assert "Disabler" in axe.roles
        assert "Carry" in axe.roles
        assert axe.legs == 2

        # Hero 2: Bane (id=3)
        bane = heroes[2]
        assert bane.id == 3
        assert bane.name == "npc_dota_hero_bane"
        assert bane.localized_name == "Bane"
        assert bane.primary_attr == "all"  # Universal attribute
        assert bane.attack_type == "Ranged"
        assert "Support" in bane.roles
        assert "Disabler" in bane.roles
        assert "Nuker" in bane.roles
        assert "Durable" in bane.roles
        assert bane.legs == 4  # Bane has 4 legs, not 2

        # Test specific well-known heroes exist at expected positions
        hero_by_name = {hero.name: hero for hero in heroes}

        # Pudge should exist and be a Strength melee hero
        pudge = hero_by_name["npc_dota_hero_pudge"]
        assert pudge.localized_name == "Pudge"
        assert pudge.primary_attr == "str"
        assert pudge.attack_type == "Melee"
        assert "Durable" in pudge.roles

        # Invoker should exist and be an Intelligence ranged hero
        invoker = hero_by_name["npc_dota_hero_invoker"]
        assert invoker.localized_name == "Invoker"
        assert invoker.primary_attr == "int"
        assert invoker.attack_type == "Ranged"
        assert "Nuker" in invoker.roles

        # Crystal Maiden should exist and be Intelligence ranged support
        cm = hero_by_name["npc_dota_hero_crystal_maiden"]
        assert cm.localized_name == "Crystal Maiden"
        assert cm.primary_attr == "int"
        assert cm.attack_type == "Ranged"
        assert "Support" in cm.roles
        assert "Nuker" in cm.roles

    @pytest.mark.asyncio
    async def test_hero_attribute_distribution(self, client):
        """Test hero attribute distribution matches expected game design."""
        heroes = await client.get_heroes()

        # Count heroes by primary attribute
        str_heroes = [h for h in heroes if h.primary_attr == "str"]
        agi_heroes = [h for h in heroes if h.primary_attr == "agi"]
        int_heroes = [h for h in heroes if h.primary_attr == "int"]
        all_heroes = [h for h in heroes if h.primary_attr == "all"]

        # Test exact distribution from real API data
        assert len(str_heroes) == 35, f"Expected exactly 35 STR heroes, got {len(str_heroes)}"
        assert len(agi_heroes) == 34, f"Expected exactly 34 AGI heroes, got {len(agi_heroes)}"
        assert len(int_heroes) == 34, f"Expected exactly 34 INT heroes, got {len(int_heroes)}"
        assert len(all_heroes) == 23, f"Expected exactly 23 Universal heroes, got {len(all_heroes)}"

        # Total should equal exactly 126
        total_attributed = len(str_heroes) + len(agi_heroes) + len(int_heroes) + len(all_heroes)
        assert total_attributed == 126

        # Attack type distribution
        melee_heroes = [h for h in heroes if h.attack_type == "Melee"]
        ranged_heroes = [h for h in heroes if h.attack_type == "Ranged"]

        # Should have reasonable melee/ranged split
        assert len(melee_heroes) >= 50, f"Expected at least 50 melee heroes, got {len(melee_heroes)}"
        assert len(ranged_heroes) >= 50, f"Expected at least 50 ranged heroes, got {len(ranged_heroes)}"
        assert len(melee_heroes) + len(ranged_heroes) == 126

    @pytest.mark.asyncio
    async def test_hero_stats_consistency_with_heroes(self, client):
        """Test hero stats data is consistent with heroes data."""
        heroes = await client.get_heroes()
        hero_stats = await client.get_hero_stats()

        # Both endpoints should return same number of heroes
        assert len(heroes) == len(hero_stats) == 126

        # Create mappings for comparison
        heroes_by_id = {h.id: h for h in heroes}
        stats_by_id = {s.id: s for s in hero_stats}

        # Every hero should have corresponding stats
        assert set(heroes_by_id.keys()) == set(stats_by_id.keys())

        # Test first few heroes have matching basic data
        for hero_id in [1, 2, 3]:  # Anti-Mage, Axe, Bane
            hero = heroes_by_id[hero_id]
            stat = stats_by_id[hero_id]

            assert hero.name == stat.name
            assert hero.localized_name == stat.localized_name
            assert hero.primary_attr == stat.primary_attr
            assert hero.attack_type == stat.attack_type
            assert hero.roles == stat.roles

    @pytest.mark.asyncio
    async def test_hero_stats_pro_scene_data(self, client):
        """Test hero statistics contain reasonable professional scene data."""
        hero_stats = await client.get_hero_stats()

        # Get stats for well-known competitive heroes
        stats_by_name = {s.name: s for s in hero_stats}

        # Pudge should have some pro picks/bans (always picked/banned in some games)
        pudge_stats = stats_by_name["npc_dota_hero_pudge"]
        if pudge_stats.pro_pick is not None:
            assert pudge_stats.pro_pick >= 0
        if pudge_stats.pro_ban is not None:
            assert pudge_stats.pro_ban >= 0
        if pudge_stats.pro_win is not None:
            assert pudge_stats.pro_win >= 0
            # Wins should not exceed picks
            if pudge_stats.pro_pick is not None:
                assert pudge_stats.pro_win <= pudge_stats.pro_pick

        # Test that popular heroes have reasonable public pick rates
        antimage_stats = stats_by_name["npc_dota_hero_antimage"]
        if antimage_stats.pub_pick is not None:
            assert antimage_stats.pub_pick > 100000, "Anti-Mage should have high public pick rate"

        # Test bracket statistics for at least one hero
        if antimage_stats.field_1_pick is not None and antimage_stats.field_7_pick is not None:
            # Higher skill brackets (7) should generally have different pick patterns than lower (1)
            # This is a reasonable business logic test
            total_low_bracket = antimage_stats.field_1_pick or 0
            total_high_bracket = antimage_stats.field_7_pick or 0
            assert total_low_bracket >= 0
            assert total_high_bracket >= 0

    @pytest.mark.asyncio
    async def test_hero_roles_business_logic(self, client):
        """Test hero role assignments follow game design logic."""
        heroes = await client.get_heroes()

        # Every hero should have at least one role
        for hero in heroes:
            assert len(hero.roles) > 0, f"{hero.localized_name} should have at least one role"
            assert len(hero.roles) <= 6, f"{hero.localized_name} should not have more than 6 roles"

        # Test that specific heroes have expected roles
        hero_by_name = {h.name: h for h in heroes}

        # Supports should have Support role
        cm = hero_by_name["npc_dota_hero_crystal_maiden"]
        assert "Support" in cm.roles

        # Carries should have Carry role
        antimage = hero_by_name["npc_dota_hero_antimage"]
        assert "Carry" in antimage.roles

        # Count role distribution
        role_counts = {}
        for hero in heroes:
            for role in hero.roles:
                role_counts[role] = role_counts.get(role, 0) + 1

        # Should have reasonable distribution of common roles
        assert role_counts.get("Support", 0) >= 25, "Should have at least 25 supports"
        assert role_counts.get("Carry", 0) >= 20, "Should have at least 20 carries"
        assert role_counts.get("Nuker", 0) >= 30, "Should have at least 30 nukers"

        # Valid roles should be from expected set
        valid_roles = {
            "Carry", "Support", "Nuker", "Disabler", "Durable", "Escape",
            "Pusher", "Initiator", "Jungler"
        }
        all_roles_used = set()
        for hero in heroes:
            all_roles_used.update(hero.roles)

        # All used roles should be valid
        assert all_roles_used.issubset(valid_roles), f"Invalid roles found: {all_roles_used - valid_roles}"
