"""Pydantic models for team-related data."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Team(BaseModel):
    """Team data from OpenDota API."""

    team_id: int
    rating: Optional[float] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    last_match_time: Optional[int] = None
    name: Optional[str] = None
    tag: Optional[str] = None
    logo_url: Optional[str] = None

    @property
    def last_match_datetime(self) -> Optional[datetime]:
        """Convert last_match_time to datetime object."""
        if self.last_match_time:
            return datetime.fromtimestamp(self.last_match_time)
        return None


class TeamPlayer(BaseModel):
    """Player in a team roster from OpenDota API."""

    account_id: int
    name: Optional[str] = None
    games_played: Optional[int] = None
    wins: Optional[int] = None
    is_current_team_member: Optional[bool] = None


class TeamMatch(BaseModel):
    """Match played by a team from OpenDota API."""

    match_id: int
    radiant_win: Optional[bool] = None
    radiant: Optional[bool] = None
    duration: Optional[int] = None
    start_time: Optional[int] = None
    leagueid: Optional[int] = None
    league_name: Optional[str] = None
    cluster: Optional[int] = None
    opposing_team_id: Optional[int] = None
    opposing_team_name: Optional[str] = None
    opposing_team_logo: Optional[str] = None

    @property
    def start_datetime(self) -> Optional[datetime]:
        """Convert start_time to datetime object."""
        if self.start_time:
            return datetime.fromtimestamp(self.start_time)
        return None
