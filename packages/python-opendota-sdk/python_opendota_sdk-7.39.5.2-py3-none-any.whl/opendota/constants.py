"""
Dota 2 constants module for python-opendota.

This module provides access to Dota 2 constants from the official odota/dotaconstants repository.
It includes comprehensive hero data, items, abilities, and other game constants.
"""

from typing import Any, Dict, List, Optional

import httpx


class DotaConstants:
    """Access to official Dota 2 constants from odota/dotaconstants."""

    BASE_URL = "https://raw.githubusercontent.com/odota/dotaconstants/master/build"

    def __init__(self):
        """Initialize the constants manager."""
        self._cache: Dict[str, Any] = {}

    async def _fetch_constants(self, endpoint: str) -> Dict[str, Any]:
        """
        Fetch constants from the dotaconstants repository.

        Args:
            endpoint: The endpoint to fetch (e.g., 'heroes.json', 'items.json')

        Returns:
            The parsed JSON data
        """
        if endpoint not in self._cache:
            url = f"{self.BASE_URL}/{endpoint}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                self._cache[endpoint] = response.json()

        result: Dict[str, Any] = self._cache[endpoint]
        return result

    async def get_heroes_constants(self) -> Dict[str, Dict[str, Any]]:
        """
        Get comprehensive hero constants data.

        Returns:
            Dictionary with hero IDs as keys and detailed hero data as values
        """
        return await self._fetch_constants("heroes.json")

    async def get_hero_by_id(self, hero_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific hero by ID from constants.

        Args:
            hero_id: The hero ID to look up

        Returns:
            Hero data dictionary or None if not found
        """
        heroes = await self.get_heroes_constants()
        return heroes.get(str(hero_id))

    async def get_hero_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific hero by localized name from constants.

        Args:
            name: The hero's localized name (e.g., "Anti-Mage")

        Returns:
            Hero data dictionary or None if not found
        """
        heroes = await self.get_heroes_constants()
        for hero_data in heroes.values():
            if hero_data.get("localized_name", "").lower() == name.lower():
                return hero_data
        return None

    async def get_items_constants(self) -> Dict[str, Dict[str, Any]]:
        """
        Get comprehensive item constants data.

        Returns:
            Dictionary with item IDs as keys and detailed item data as values
        """
        return await self._fetch_constants("items.json")

    async def get_abilities_constants(self) -> Dict[str, Dict[str, Any]]:
        """
        Get comprehensive abilities constants data.

        Returns:
            Dictionary with ability names as keys and detailed ability data as values
        """
        return await self._fetch_constants("abilities.json")

    async def get_game_modes(self) -> Dict[str, Dict[str, Any]]:
        """
        Get game mode constants.

        Returns:
            Dictionary with game mode IDs as keys and mode data as values
        """
        return await self._fetch_constants("game_modes.json")

    async def get_lobby_types(self) -> Dict[str, Dict[str, Any]]:
        """
        Get lobby type constants.

        Returns:
            Dictionary with lobby type IDs as keys and lobby data as values
        """
        return await self._fetch_constants("lobby_type.json")

    async def search_heroes_by_role(self, role: str) -> List[Dict[str, Any]]:
        """
        Search heroes by their role.

        Args:
            role: The role to search for (e.g., "Carry", "Support", "Initiator")

        Returns:
            List of heroes that have the specified role
        """
        heroes = await self.get_heroes_constants()
        matching_heroes = []

        for hero_data in heroes.values():
            roles = hero_data.get("roles", [])
            if role in roles:
                matching_heroes.append(hero_data)

        return matching_heroes

    async def get_heroes_by_attribute(self, attribute: str) -> List[Dict[str, Any]]:
        """
        Get heroes filtered by primary attribute.

        Args:
            attribute: Primary attribute ("str", "agi", "int", or "all")

        Returns:
            List of heroes with the specified primary attribute
        """
        heroes = await self.get_heroes_constants()
        matching_heroes = []

        for hero_data in heroes.values():
            if hero_data.get("primary_attr") == attribute:
                matching_heroes.append(hero_data)

        return matching_heroes

    def clear_cache(self):
        """Clear the constants cache."""
        self._cache.clear()


# Create a singleton instance for easy access
dota_constants = DotaConstants()
