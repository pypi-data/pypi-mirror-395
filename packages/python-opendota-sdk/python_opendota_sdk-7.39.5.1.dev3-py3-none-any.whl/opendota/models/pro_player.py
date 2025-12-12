"""Pydantic models for professional player data."""

from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class ProPlayer(BaseModel):
    """Professional player data from OpenDota API."""

    account_id: int
    steamid: Optional[str] = None
    avatar: Optional[str] = None
    avatarmedium: Optional[str] = None
    avatarfull: Optional[str] = None
    profileurl: Optional[str] = None
    personaname: Optional[str] = None
    last_login: Optional[Union[str, int]] = None
    full_history_time: Optional[Union[str, int]] = None
    cheese: Optional[int] = None
    fh_unavailable: Optional[bool] = None
    loccountrycode: Optional[str] = None
    last_match_time: Optional[Union[str, int]] = None
    name: Optional[str] = None
    country_code: Optional[str] = None
    fantasy_role: Optional[int] = None
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    team_tag: Optional[str] = None
    is_locked: Optional[bool] = None
    is_pro: Optional[bool] = None
    locked_until: Optional[int] = None

    @property
    def last_login_datetime(self) -> Optional[datetime]:
        """Convert last_login to datetime object."""
        if self.last_login:
            if isinstance(self.last_login, str):
                return datetime.fromisoformat(self.last_login.replace("Z", "+00:00"))
            return datetime.fromtimestamp(self.last_login)
        return None

    @property
    def last_match_datetime(self) -> Optional[datetime]:
        """Convert last_match_time to datetime object."""
        if self.last_match_time:
            if isinstance(self.last_match_time, str):
                return datetime.fromisoformat(self.last_match_time.replace("Z", "+00:00"))
            return datetime.fromtimestamp(self.last_match_time)
        return None
