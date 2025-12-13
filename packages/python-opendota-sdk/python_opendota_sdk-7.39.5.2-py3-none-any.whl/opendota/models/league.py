"""Pydantic models for league/tournament data."""

from typing import Optional

from pydantic import BaseModel


class League(BaseModel):
    """League/tournament data from OpenDota API."""

    leagueid: int
    ticket: Optional[str] = None
    banner: Optional[str] = None
    tier: Optional[str] = None
    name: Optional[str] = None


class LeagueTeam(BaseModel):
    """Team participating in a league."""

    team_id: int
    name: Optional[str] = None
    tag: Optional[str] = None
    logo_url: Optional[str] = None
