"""Pydantic models for hero-related data."""

from typing import List, Optional

from pydantic import BaseModel, Field


class Hero(BaseModel):
    """Hero data model."""
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str
    roles: List[str]
    legs: int
    img: Optional[str] = None
    icon: Optional[str] = None
    base_health: Optional[int] = None
    base_health_regen: Optional[float] = None
    base_mana: Optional[int] = None
    base_mana_regen: Optional[float] = None
    base_armor: Optional[float] = None
    base_mr: Optional[int] = None
    base_attack_min: Optional[int] = None
    base_attack_max: Optional[int] = None
    base_str: Optional[int] = None
    base_agi: Optional[int] = None
    base_int: Optional[int] = None
    str_gain: Optional[float] = None
    agi_gain: Optional[float] = None
    int_gain: Optional[float] = None
    attack_range: Optional[int] = None
    projectile_speed: Optional[int] = None
    attack_rate: Optional[float] = None
    move_speed: Optional[int] = None
    cm_enabled: Optional[bool] = None
    day_vision: Optional[int] = None
    night_vision: Optional[int] = None


class HeroStats(BaseModel):
    """Hero statistics data."""
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str
    roles: List[str]
    img: Optional[str] = None
    icon: Optional[str] = None
    base_health: Optional[int] = None
    base_health_regen: Optional[float] = None
    base_mana: Optional[int] = None
    base_mana_regen: Optional[float] = None
    base_armor: Optional[float] = None
    base_mr: Optional[int] = None
    base_attack_min: Optional[int] = None
    base_attack_max: Optional[int] = None
    base_str: Optional[int] = None
    base_agi: Optional[int] = None
    base_int: Optional[int] = None
    str_gain: Optional[float] = None
    agi_gain: Optional[float] = None
    int_gain: Optional[float] = None
    attack_range: Optional[int] = None
    projectile_speed: Optional[int] = None
    attack_rate: Optional[float] = None
    base_attack_time: Optional[int] = None
    attack_point: Optional[float] = None
    move_speed: Optional[int] = None
    turn_rate: Optional[float] = None
    cm_enabled: Optional[bool] = None
    legs: Optional[int] = None
    day_vision: Optional[int] = None
    night_vision: Optional[int] = None

    # Statistics fields
    pro_win: Optional[int] = None
    pro_pick: Optional[int] = None
    pro_ban: Optional[int] = None
    pub_pick: Optional[int] = None
    pub_win: Optional[int] = None
    turbo_picks: Optional[int] = None
    turbo_wins: Optional[int] = None

    # Bracket-specific stats (1-8 represent skill brackets)
    field_1_pick: Optional[int] = Field(None, alias="1_pick")
    field_1_win: Optional[int] = Field(None, alias="1_win")
    field_2_pick: Optional[int] = Field(None, alias="2_pick")
    field_2_win: Optional[int] = Field(None, alias="2_win")
    field_3_pick: Optional[int] = Field(None, alias="3_pick")
    field_3_win: Optional[int] = Field(None, alias="3_win")
    field_4_pick: Optional[int] = Field(None, alias="4_pick")
    field_4_win: Optional[int] = Field(None, alias="4_win")
    field_5_pick: Optional[int] = Field(None, alias="5_pick")
    field_5_win: Optional[int] = Field(None, alias="5_win")
    field_6_pick: Optional[int] = Field(None, alias="6_pick")
    field_6_win: Optional[int] = Field(None, alias="6_win")
    field_7_pick: Optional[int] = Field(None, alias="7_pick")
    field_7_win: Optional[int] = Field(None, alias="7_win")
    field_8_pick: Optional[int] = Field(None, alias="8_pick")
    field_8_win: Optional[int] = Field(None, alias="8_win")

    # Trend data (lists of recent statistics)
    pub_pick_trend: Optional[List[int]] = None
    pub_win_trend: Optional[List[int]] = None
    turbo_picks_trend: Optional[List[int]] = None
    turbo_wins_trend: Optional[List[int]] = None
