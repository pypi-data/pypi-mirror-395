"""Main OpenDota API client."""

import asyncio
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union, cast

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

import httpx

from .exceptions import OpenDotaAPIError, OpenDotaNotFoundError, OpenDotaRateLimitError
from .fantasy import FANTASY
from .models.hero import Hero, HeroStats
from .models.league import League, LeagueTeam
from .models.match import Match, ProMatch, PublicMatch
from .models.player import PlayerMatch, PlayerProfile
from .models.pro_player import ProPlayer
from .models.team import Team, TeamMatch, TeamPlayer

# Type aliases for response formats - Easy to extend with new formats (e.g., add XML, MessagePack, etc.)
MatchResponse: TypeAlias = Union[Match, dict]
PublicMatchesResponse: TypeAlias = Union[List[PublicMatch], List[dict]]
ProMatchesResponse: TypeAlias = Union[List[ProMatch], List[dict]]
PlayerResponse: TypeAlias = Union[PlayerProfile, dict]
PlayerMatchesResponse: TypeAlias = Union[List[PlayerMatch], List[dict]]
HeroesResponse: TypeAlias = Union[List[Hero], List[dict]]
HeroStatsResponse: TypeAlias = Union[List[HeroStats], List[dict]]

# Team type aliases
TeamsResponse: TypeAlias = Union[List[Team], List[dict]]
TeamResponse: TypeAlias = Union[Team, dict]
TeamPlayersResponse: TypeAlias = Union[List[TeamPlayer], List[dict]]
TeamMatchesResponse: TypeAlias = Union[List[TeamMatch], List[dict]]

# Pro player type aliases
ProPlayersResponse: TypeAlias = Union[List[ProPlayer], List[dict]]

# League type aliases
LeaguesResponse: TypeAlias = Union[List[League], List[dict]]
LeagueResponse: TypeAlias = Union[League, dict]
LeagueTeamsResponse: TypeAlias = Union[List[LeagueTeam], List[dict]]


class OpenDota:
    """Main client for interacting with the OpenDota API."""

    BASE_URL = "https://api.opendota.com/api"

    def __init__(
        self,
        data_dir: Optional[str] = None,
        api_key: Optional[str] = None,
        delay: int = 3,
        fantasy: Optional[Dict[str, float]] = None,
        api_url: Optional[str] = None,
        timeout: float = 30.0,
        format: Literal['pydantic', 'json'] = 'pydantic',
        auth_method: Literal['header', 'query'] = 'header'
    ):
        """Initialize the OpenDota client.

        Args:
            data_dir: Path to data directory for storing responses to API calls.
                     The default is ~/dota2.
            api_key: If you have an OpenDota API key. The default is None.
            delay: Delay in seconds between two consecutive API calls.
                  It is recommended to keep this at least 3 seconds, to
                  prevent hitting the daily API limit.
                  If you have an API key, this value is ignored.
                  The default is 3.
            fantasy: Fantasy DotA2 Configuration. Utility constant FANTASY holds
                    the standard values and is used as default.
                    Keys of the fantasy will override the default values.
                    They must be a subset of the keys of FANTASY.
                    Parameters ending with '_base' are used as base values,
                    while others are used as multipliers.
            api_url: URL to OpenDota API. It is recommended to not change this value.
            timeout: Request timeout in seconds
            format: Output format - 'pydantic' for typed models, 'json' for dicts
            auth_method: Authentication method - 'header' for Bearer token (default),
                        'query' for query parameter
        """
        # Set up data directory for caching
        if data_dir is None:
            self.data_dir = Path.home() / "dota2"
        else:
            self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # API configuration
        self.api_key = api_key or os.getenv("OPENDOTA_API_KEY")
        self.delay = delay
        self.timeout = timeout
        self.format = format
        self.auth_method = auth_method

        # Set API URL
        if api_url:
            self.BASE_URL = api_url

        # Set up fantasy configuration
        self.fantasy = FANTASY.copy()
        if fantasy is not None:
            # Update default fantasy values with user-provided ones
            for key, value in fantasy.items():
                if key in self.fantasy:
                    self.fantasy[key] = value
                else:
                    raise ValueError(f"Invalid fantasy key: {key}. Must be one of {list(FANTASY.keys())}")

        # Track last request time for rate limiting
        self._last_request_time: float = 0.0
        self._client = None

    async def _ensure_client(self):
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)

    async def __aenter__(self):
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _format_response(self, response: Any) -> Any:
        """Format response based on format setting.

        Args:
            response: Pydantic model or list of models

        Returns:
            Formatted response (Pydantic models or dicts)
        """
        if self.format == 'json':
            if hasattr(response, 'model_dump'):
                return response.model_dump()
            elif isinstance(response, list):
                return [item.model_dump() if hasattr(item, 'model_dump') else item for item in response]
        return response

    def _get_cache_filename(self, url: str, params: Optional[Dict[str, Any]] = None) -> Path:
        """Generate a cache filename for the request."""
        # Create a unique hash from URL and params
        cache_key = f"{url}"
        if params:
            # Sort params for consistent hashing
            sorted_params = sorted(params.items())
            cache_key += str(sorted_params)

        # Create hash for filename
        hash_digest = hashlib.md5(cache_key.encode()).hexdigest()

        # Extract endpoint name for readable directory structure
        endpoint_parts = url.replace(self.BASE_URL, "").strip("/").split("/")
        endpoint_dir = "_".join(endpoint_parts[:2]) if len(endpoint_parts) > 1 else endpoint_parts[0]

        # Create subdirectory for endpoint type
        cache_dir = self.data_dir / "cache" / endpoint_dir
        cache_dir.mkdir(parents=True, exist_ok=True)

        return cache_dir / f"{hash_digest}.json"

    def _load_from_cache(self, cache_file: Path) -> Optional[Any]:
        """Load data from cache file if it exists."""
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # Cache file is corrupted, will re-fetch
                pass
        return None

    def _save_to_cache(self, cache_file: Path, data: Any) -> None:
        """Save data to cache file."""
        try:
            with open(cache_file, "w") as f:
                json.dump(data, f, indent=2)
        except (IOError, TypeError):
            # Failed to cache, but don't fail the request
            pass

    async def _apply_rate_limit(self) -> None:
        """Apply rate limiting if no API key is provided."""
        if not self.api_key and self.delay > 0:
            # Calculate time since last request
            current_time = time.time()
            time_since_last = current_time - self._last_request_time

            # If not enough time has passed, sleep
            if time_since_last < self.delay:
                sleep_time = self.delay - time_since_last
                await asyncio.sleep(sleep_time)

            # Update last request time
            self._last_request_time = time.time()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
        force: bool = False,
        **kwargs
    ) -> Any:
        """Make an HTTP request to the OpenDota API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            use_cache: Whether to use cached responses (default: True)
            force: Force refresh, bypassing cache (default: False)
            **kwargs: Additional arguments passed to httpx

        Returns:
            Parsed JSON response

        Raises:
            OpenDotaAPIError: For API errors
            OpenDotaRateLimitError: For rate limit errors
            OpenDotaNotFoundError: For 404 errors
        """
        await self._ensure_client()
        assert self._client is not None  # Ensure client is initialized

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"

        # Try to load from cache if enabled and not forcing
        cache_file = None
        if use_cache and method == "GET":
            cache_file = self._get_cache_filename(url, params)
            if not force:
                cached_data = self._load_from_cache(cache_file)
                if cached_data is not None:
                    return cached_data

        # Apply rate limiting
        await self._apply_rate_limit()

        # Add API key based on auth_method
        headers = kwargs.get('headers', {})

        if self.api_key:
            if self.auth_method == 'header':
                # Use Bearer token in Authorization header
                headers['Authorization'] = f'Bearer {self.api_key}'
                kwargs['headers'] = headers
            else:  # auth_method == 'query'
                # Use query parameter
                params = params or {}
                params["api_key"] = self.api_key

        response = await self._client.request(
            method=method,
            url=url,
            params=params,
            **kwargs
        )

        # Handle different status codes
        if response.status_code == 200:
            data = response.json()
            # Save to cache if enabled
            if cache_file and use_cache:
                self._save_to_cache(cache_file, data)
            return data
        elif response.status_code == 404:
            raise OpenDotaNotFoundError("Resource not found", response.status_code)
        elif response.status_code == 429:
            raise OpenDotaRateLimitError("Rate limit exceeded", response.status_code)
        else:
            raise OpenDotaAPIError(
                f"API request failed: {response.text}",
                response.status_code
            )

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True, force: bool = False
    ) -> Any:
        """Make a GET request to the API.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            use_cache: Whether to use cached responses (default: True)
            force: Force refresh, bypassing cache (default: False)

        Returns:
            Parsed JSON response
        """
        return await self._request("GET", endpoint, params=params, use_cache=use_cache, force=force)

    # Match Methods
    async def get_match(self, match_id: int) -> MatchResponse:
        """Get match data by match ID.

        Args:
            match_id: The match ID to retrieve

        Returns:
            Match data (Match if format='pydantic', dict if format='json')
        """
        data = await self.get(f"matches/{match_id}")
        match = Match(**data)
        return cast(MatchResponse, self._format_response(match))

    async def get_public_matches(
        self,
        mmr_ascending: Optional[int] = None,
        mmr_descending: Optional[int] = None,
        less_than_match_id: Optional[int] = None
    ) -> PublicMatchesResponse:
        """Get public matches with optional filters.

        Args:
            mmr_ascending: Return matches with average MMR ascending from this value
            mmr_descending: Return matches with average MMR descending from this value
            less_than_match_id: Return matches with a match ID lower than this value

        Returns:
            List of public matches (List[PublicMatch] if format='pydantic', List[dict] if format='json')
        """
        params: Dict[str, Any] = {}
        if mmr_ascending is not None:
            params["mmr_ascending"] = mmr_ascending
        if mmr_descending is not None:
            params["mmr_descending"] = mmr_descending
        if less_than_match_id is not None:
            params["less_than_match_id"] = less_than_match_id

        data = await self.get("publicMatches", params=params)
        matches = [PublicMatch(**match) for match in data]
        return cast(PublicMatchesResponse, self._format_response(matches))

    async def get_pro_matches(self, less_than_match_id: Optional[int] = None) -> ProMatchesResponse:
        """Get professional matches.

        Args:
            less_than_match_id: Return matches with a match ID lower than this value

        Returns:
            List of professional matches (List[ProMatch] if format='pydantic', List[dict] if format='json')
        """
        params: Dict[str, Any] = {}
        if less_than_match_id is not None:
            params["less_than_match_id"] = less_than_match_id

        data = await self.get("proMatches", params=params, use_cache=False)
        matches = [ProMatch(**match) for match in data]
        return cast(ProMatchesResponse, self._format_response(matches))

    async def get_parsed_matches(self, less_than_match_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get parsed matches.

        Args:
            less_than_match_id: Return matches with a match ID lower than this value

        Returns:
            List of parsed match data
        """
        params: Dict[str, Any] = {}
        if less_than_match_id is not None:
            params["less_than_match_id"] = less_than_match_id

        result: List[Dict[str, Any]] = await self.get("parsedMatches", params=params)
        return result

    # Player Methods
    async def get_player(self, account_id: int) -> PlayerResponse:
        """Get player data by account ID.

        Args:
            account_id: The player's account ID

        Returns:
            Player profile data (PlayerProfile if format='pydantic', dict if format='json')
        """
        data = await self.get(f"players/{account_id}")
        player = PlayerProfile(**data)
        return cast(PlayerResponse, self._format_response(player))

    async def get_player_matches(
        self,
        account_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        win: Optional[int] = None,
        patch: Optional[int] = None,
        game_mode: Optional[int] = None,
        lobby_type: Optional[int] = None,
        region: Optional[int] = None,
        date: Optional[int] = None,
        lane_role: Optional[int] = None,
        hero_id: Optional[int] = None,
        is_radiant: Optional[int] = None,
        included_account_id: Optional[List[int]] = None,
        excluded_account_id: Optional[List[int]] = None,
        with_hero_id: Optional[List[int]] = None,
        against_hero_id: Optional[List[int]] = None,
        significant: Optional[int] = None,
        having: Optional[int] = None,
        sort: Optional[str] = None
    ) -> PlayerMatchesResponse:
        """Get matches for a player.

        Args:
            account_id: Player's account ID
            limit: Number of matches to return (default 20)
            offset: Number of matches to offset start by
            win: Filter by wins (0=loss, 1=win)
            patch: Filter by patch version
            game_mode: Filter by game mode
            lobby_type: Filter by lobby type
            region: Filter by region
            date: Filter by date (days since epoch)
            lane_role: Filter by lane role
            hero_id: Filter by hero ID
            is_radiant: Filter by team (0=dire, 1=radiant)
            included_account_id: Array of account IDs to include
            excluded_account_id: Array of account IDs to exclude
            with_hero_id: Array of hero IDs on the same team
            against_hero_id: Array of hero IDs on the opposing team
            significant: Filter by significant matches (0=false, 1=true)
            having: Filter by having at least this value
            sort: Sort matches by this field

        Returns:
            List of player matches (List[PlayerMatch] if format='pydantic', List[dict] if format='json')
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if win is not None:
            params["win"] = win
        if patch is not None:
            params["patch"] = patch
        if game_mode is not None:
            params["game_mode"] = game_mode
        if lobby_type is not None:
            params["lobby_type"] = lobby_type
        if region is not None:
            params["region"] = region
        if date is not None:
            params["date"] = date
        if lane_role is not None:
            params["lane_role"] = lane_role
        if hero_id is not None:
            params["hero_id"] = hero_id
        if is_radiant is not None:
            params["is_radiant"] = is_radiant
        if included_account_id is not None:
            params["included_account_id"] = included_account_id
        if excluded_account_id is not None:
            params["excluded_account_id"] = excluded_account_id
        if with_hero_id is not None:
            params["with_hero_id"] = with_hero_id
        if against_hero_id is not None:
            params["against_hero_id"] = against_hero_id
        if significant is not None:
            params["significant"] = significant
        if having is not None:
            params["having"] = having
        if sort is not None:
            params["sort"] = sort

        data = await self.get(f"players/{account_id}/matches", params=params)
        matches = [PlayerMatch(**match) for match in data]
        return cast(PlayerMatchesResponse, self._format_response(matches))

    # Hero Methods
    async def get_heroes(self) -> HeroesResponse:
        """Get all heroes data.

        Returns:
            List of all heroes (List[Hero] if format='pydantic', List[dict] if format='json')
        """
        data = await self.get("heroes")
        heroes = [Hero(**hero) for hero in data]
        return cast(HeroesResponse, self._format_response(heroes))

    async def get_hero_stats(self) -> HeroStatsResponse:
        """Get hero statistics.

        Returns:
            List of hero statistics (List[HeroStats] if format='pydantic', List[dict] if format='json')
        """
        data = await self.get("heroStats")
        hero_stats = [HeroStats(**hero) for hero in data]
        return cast(HeroStatsResponse, self._format_response(hero_stats))

    # Team Methods
    async def get_teams(self) -> TeamsResponse:
        """Get all teams.

        Returns:
            List of all teams (List[Team] if format='pydantic', List[dict] if format='json')
        """
        data = await self.get("teams")
        teams = [Team(**team) for team in data]
        return cast(TeamsResponse, self._format_response(teams))

    async def get_team(self, team_id: int) -> TeamResponse:
        """Get team data by team ID.

        Args:
            team_id: The team ID to retrieve

        Returns:
            Team data (Team if format='pydantic', dict if format='json')
        """
        data = await self.get(f"teams/{team_id}")
        team = Team(**data)
        return cast(TeamResponse, self._format_response(team))

    async def get_team_players(self, team_id: int) -> TeamPlayersResponse:
        """Get team roster (current and historical players).

        Args:
            team_id: The team ID

        Returns:
            List of team players (List[TeamPlayer] if format='pydantic', List[dict] if format='json')
        """
        data = await self.get(f"teams/{team_id}/players")
        players = [TeamPlayer(**p) for p in data]
        return cast(TeamPlayersResponse, self._format_response(players))

    async def get_team_matches(
        self,
        team_id: int,
        limit: Optional[int] = None
    ) -> TeamMatchesResponse:
        """Get team match history.

        Args:
            team_id: The team ID
            limit: Maximum number of matches to return

        Returns:
            List of team matches (List[TeamMatch] if format='pydantic', List[dict] if format='json')
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit

        data = await self.get(f"teams/{team_id}/matches", params=params or None)
        matches = [TeamMatch(**m) for m in data]
        return cast(TeamMatchesResponse, self._format_response(matches))

    # Pro Player Methods
    async def get_pro_players(self) -> ProPlayersResponse:
        """Get all professional players.

        Returns:
            List of pro players (List[ProPlayer] if format='pydantic', List[dict] if format='json')
        """
        data = await self.get("proPlayers")
        players = [ProPlayer(**p) for p in data]
        return cast(ProPlayersResponse, self._format_response(players))

    # League Methods
    async def get_leagues(self) -> LeaguesResponse:
        """Get all leagues/tournaments.

        Returns:
            List of leagues (List[League] if format='pydantic', List[dict] if format='json')
        """
        data = await self.get("leagues")
        leagues = [League(**league) for league in data]
        return cast(LeaguesResponse, self._format_response(leagues))

    async def get_league(self, league_id: int) -> LeagueResponse:
        """Get league data by league ID.

        Args:
            league_id: The league ID to retrieve

        Returns:
            League data (League if format='pydantic', dict if format='json')
        """
        data = await self.get(f"leagues/{league_id}")
        league = League(**data)
        return cast(LeagueResponse, self._format_response(league))

    async def get_league_matches(
        self,
        league_id: int,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get matches in a league.

        Args:
            league_id: The league ID
            limit: Maximum number of matches to return

        Returns:
            List of match data
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit

        result: List[Dict[str, Any]] = await self.get(
            f"leagues/{league_id}/matches",
            params=params or None
        )
        return result

    async def get_league_teams(self, league_id: int) -> LeagueTeamsResponse:
        """Get teams participating in a league.

        Args:
            league_id: The league ID

        Returns:
            List of teams (List[LeagueTeam] if format='pydantic', List[dict] if format='json')
        """
        data = await self.get(f"leagues/{league_id}/teams")
        teams = [LeagueTeam(**t) for t in data]
        return cast(LeagueTeamsResponse, self._format_response(teams))
