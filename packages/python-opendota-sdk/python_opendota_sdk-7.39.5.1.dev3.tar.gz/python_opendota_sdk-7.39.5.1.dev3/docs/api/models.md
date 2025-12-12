# Data Models

??? info "🤖 AI Summary"

    Pydantic models for API responses. **Match models**: `Match` (full data with players list), `PublicMatch` (summary with avg_mmr), `ProMatch` (with team/league names). **Player models**: `PlayerProfile` (profile + rank_tier), `PlayerMatch` (hero_id, KDA, player_slot). **Hero models**: `Hero` (name, roles, primary_attr), `HeroStats` (pro_pick/win/ban, rank-specific picks). Access via typed properties: `match.radiant_win`, `player.kills`.

All API responses are parsed into Pydantic models with full type safety.

## Match Models

### Match

Detailed match data returned by `get_match()`.

```python
class Match(BaseModel):
    match_id: int
    duration: int
    radiant_win: bool
    radiant_score: int
    dire_score: int
    players: List[MatchPlayer]
    # ... and many more fields
```

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `match_id` | `int` | Unique match identifier |
| `duration` | `int` | Match duration in seconds |
| `radiant_win` | `bool` | Whether Radiant won |
| `radiant_score` | `int` | Radiant kill score |
| `dire_score` | `int` | Dire kill score |
| `players` | `List[MatchPlayer]` | List of player data |

### PublicMatch

Summary data for public matches.

```python
class PublicMatch(BaseModel):
    match_id: int
    duration: int
    radiant_win: bool
    avg_mmr: Optional[int]
```

### ProMatch

Professional match data.

```python
class ProMatch(BaseModel):
    match_id: int
    duration: int
    radiant_win: bool
    radiant_name: Optional[str]
    dire_name: Optional[str]
    league_name: Optional[str]
```

## Player Models

### PlayerProfile

Player profile and ranking data.

```python
class PlayerProfile(BaseModel):
    profile: Profile
    rank_tier: Optional[int]
    leaderboard_rank: Optional[int]
```

**Profile Sub-model:**

```python
class Profile(BaseModel):
    account_id: int
    personaname: str
    name: Optional[str]
    steamid: str
    avatar: str
    loccountrycode: Optional[str]
```

### PlayerMatch

Match data from player's perspective.

```python
class PlayerMatch(BaseModel):
    match_id: int
    hero_id: int
    kills: int
    deaths: int
    assists: int
    player_slot: int
    radiant_win: bool
```

## Hero Models

### Hero

Basic hero information.

```python
class Hero(BaseModel):
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str
    roles: List[str]
```

### HeroStats

Hero statistics with pick/win rates.

```python
class HeroStats(BaseModel):
    id: int
    localized_name: str
    pro_pick: Optional[int]
    pro_win: Optional[int]
    pro_ban: Optional[int]
    # Per-rank pick rates
    herald_picks: Optional[int]
    guardian_picks: Optional[int]
    # ... etc
```

## Using Models

```python
from opendota import OpenDota

async with OpenDota() as client:
    # Access typed properties
    match = await client.get_match(8461956309)
    print(f"Duration: {match.duration}s")
    print(f"Winner: {'Radiant' if match.radiant_win else 'Dire'}")

    for player in match.players:
        team = "Radiant" if player.player_slot < 128 else "Dire"
        print(f"{team}: {player.kills}/{player.deaths}/{player.assists}")
```
