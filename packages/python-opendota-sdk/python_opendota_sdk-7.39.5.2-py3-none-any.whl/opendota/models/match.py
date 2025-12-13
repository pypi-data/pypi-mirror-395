"""Pydantic models for match-related data."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Player(BaseModel):
    """Player data within a match."""
    account_id: Optional[int] = None
    player_slot: int
    hero_id: int
    item_0: Optional[int] = None
    item_1: Optional[int] = None
    item_2: Optional[int] = None
    item_3: Optional[int] = None
    item_4: Optional[int] = None
    item_5: Optional[int] = None
    backpack_0: Optional[int] = None
    backpack_1: Optional[int] = None
    backpack_2: Optional[int] = None
    item_neutral: Optional[int] = None
    kills: int
    deaths: int
    assists: int
    leaver_status: int
    last_hits: int
    denies: int
    gold_per_min: int
    xp_per_min: int
    level: int
    net_worth: Optional[int] = None
    aghanims_scepter: Optional[int] = None
    aghanims_shard: Optional[int] = None
    moonshard: Optional[int] = None
    hero_damage: Optional[int] = None
    tower_damage: Optional[int] = None
    hero_healing: Optional[int] = None
    gold: Optional[int] = None
    gold_spent: Optional[int] = None
    scaled_hero_damage: Optional[int] = None
    scaled_tower_damage: Optional[int] = None
    scaled_hero_healing: Optional[int] = None


class Team(BaseModel):
    """Team data within a match."""
    name: Optional[str] = None
    tag: Optional[str] = None
    logo_url: Optional[str] = None


class League(BaseModel):
    """League information for a match."""
    leagueid: int
    name: str
    tier: str


class PickBan(BaseModel):
    """Pick/ban data for a match."""
    is_pick: bool
    hero_id: int
    team: int
    order: int


class Match(BaseModel):
    """Complete match data model."""
    match_id: int
    barracks_status_dire: Optional[int] = None
    barracks_status_radiant: Optional[int] = None
    cluster: Optional[int] = None
    dire_score: int
    duration: int
    engine: Optional[int] = None
    first_blood_time: Optional[int] = None
    game_mode: int
    human_players: Optional[int] = None
    leagueid: Optional[int] = None
    lobby_type: int
    match_seq_num: Optional[int] = None
    negative_votes: Optional[int] = None
    objectives: Optional[List[Dict[str, Any]]] = None
    picks_bans: Optional[List[PickBan]] = None
    positive_votes: Optional[int] = None
    radiant_gold_adv: Optional[List[int]] = None
    radiant_score: int
    radiant_win: bool
    radiant_xp_adv: Optional[List[int]] = None
    start_time: int
    teamfights: Optional[List[Dict[str, Any]]] = None
    tower_status_dire: Optional[int] = None
    tower_status_radiant: Optional[int] = None
    version: Optional[int] = None
    replay_salt: Optional[int] = None
    series_id: Optional[int] = None
    series_type: Optional[int] = None
    players: List[Player]
    patch: Optional[int] = None
    region: Optional[int] = None
    replay_url: Optional[str] = None

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)


class PublicMatch(BaseModel):
    """Public match data model (simplified)."""
    match_id: int
    match_seq_num: int
    radiant_win: bool
    start_time: int
    duration: int
    avg_mmr: Optional[int] = None
    num_mmr: Optional[int] = None
    lobby_type: int
    game_mode: int
    avg_rank_tier: Optional[float] = None
    num_rank_tier: Optional[int] = None
    cluster: Optional[int] = None

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)


class ProMatch(BaseModel):
    """Professional match data model."""
    match_id: int
    duration: int
    start_time: int
    radiant_team_id: Optional[int] = None
    radiant_name: Optional[str] = None
    dire_team_id: Optional[int] = None
    dire_name: Optional[str] = None
    leagueid: Optional[int] = None
    league_name: Optional[str] = None
    series_id: Optional[int] = None
    series_type: Optional[int] = None
    radiant_score: int
    dire_score: int
    radiant_win: bool

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)
