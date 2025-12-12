"""Pydantic models for player-related data."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Profile(BaseModel):
    """Player profile sub-model."""
    account_id: int
    personaname: Optional[str] = None
    name: Optional[str] = None
    plus: Optional[bool] = None
    cheese: Optional[int] = None
    steamid: Optional[str] = None
    avatar: Optional[str] = None
    avatarmedium: Optional[str] = None
    avatarfull: Optional[str] = None
    profileurl: Optional[str] = None
    last_login: Optional[int] = None
    loccountrycode: Optional[str] = None
    status: Optional[str] = None
    fh_unavailable: Optional[bool] = None
    is_contributor: Optional[bool] = None
    is_subscriber: Optional[bool] = None


class PlayerProfile(BaseModel):
    """Player profile data."""
    profile: Profile
    rank_tier: Optional[int] = None
    leaderboard_rank: Optional[int] = None
    computed_rating: Optional[float] = None

    @property
    def last_login_datetime(self) -> Optional[datetime]:
        """Convert last_login to datetime object."""
        if self.profile.last_login:
            return datetime.fromtimestamp(self.profile.last_login)
        return None


class PlayerMatch(BaseModel):
    """Player match history entry."""
    match_id: int
    player_slot: int
    radiant_win: bool
    duration: int
    game_mode: int
    lobby_type: int
    hero_id: int
    start_time: int
    version: Optional[int] = None
    kills: int
    deaths: int
    assists: int
    skill: Optional[int] = None
    average_rank: Optional[int] = None
    xp_per_min: Optional[int] = None
    gold_per_min: Optional[int] = None
    hero_damage: Optional[int] = None
    tower_damage: Optional[int] = None
    hero_healing: Optional[int] = None
    last_hits: Optional[int] = None
    lane: Optional[int] = None
    lane_role: Optional[int] = None
    is_roaming: Optional[bool] = None
    cluster: Optional[int] = None
    leaver_status: int
    party_size: Optional[int] = None
    hero_variant: Optional[int] = None

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)
