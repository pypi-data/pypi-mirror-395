# Changelog

??? info "🤖 AI Summary"

    Version scheme: `{dota_major}.{dota_minor}.{dota_letter}.{sdk_release}` (e.g., 7.39.5.1 = Dota patch 7.39e, first SDK release). Current version adds: async httpx client, Pydantic models, matches/players/heroes/teams/leagues/pro_players endpoints, error handling, rate limiting, API key support, caching.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.39.5.1.dev2] - 2025-12-03

### Added
- Teams endpoints:
  - `get_teams()` - Get all teams sorted by rating
  - `get_team(team_id)` - Get team details
  - `get_team_players(team_id)` - Get team roster
  - `get_team_matches(team_id)` - Get team match history
- Pro Players endpoints:
  - `get_pro_players()` - Get all professional players
- Leagues endpoints:
  - `get_leagues()` - Get all leagues/tournaments
  - `get_league(league_id)` - Get league details
  - `get_league_matches(league_id)` - Get league matches
  - `get_league_teams(league_id)` - Get teams in a league
- New Pydantic models: `Team`, `TeamPlayer`, `TeamMatch`, `ProPlayer`, `League`
- Comprehensive test suite for new endpoints

## [7.39.5.1] - 2025-12-02

Version scheme: `{dota_major}.{dota_minor}.{dota_letter}.{sdk_release}`
- `7.39.5` = Dota 2 patch 7.39e (a=1, b=2, c=3, d=4, e=5)
- `.1` = First SDK release for this patch

### Added
- Full async/await support with httpx
- Complete type safety with Pydantic models
- Matches endpoints:
  - `get_match()` - Get detailed match data
  - `get_public_matches()` - Get public matches with filters
  - `get_pro_matches()` - Get professional matches
  - `get_parsed_matches()` - Get parsed match data
- Players endpoints:
  - `get_player()` - Get player profile
  - `get_player_matches()` - Get player match history with extensive filtering
- Heroes endpoints:
  - `get_heroes()` - Get all heroes data
  - `get_hero_stats()` - Get hero statistics
- Comprehensive error handling with custom exceptions
- Rate limiting awareness and proper HTTP status handling
- Optional API key support for higher rate limits
- Context manager support for automatic cleanup
- Built-in response caching
- Extensive test suite with real API integration tests
- Full documentation with MkDocs Material theme

### Technical Details
- Python 3.9+ support
- Built with httpx for modern async HTTP
- Pydantic v2 for data validation and parsing
- Comprehensive type hints throughout
- CI/CD with GitHub Actions
- TestPyPI and PyPI publishing support
