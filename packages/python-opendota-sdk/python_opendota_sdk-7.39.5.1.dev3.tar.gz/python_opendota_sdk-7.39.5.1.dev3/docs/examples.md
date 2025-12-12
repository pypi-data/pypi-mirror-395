# Examples

??? info "🤖 AI Summary"

    Code examples for common tasks: **Match analysis** - get KDA, GPM, winner. **Player tracking** - profile, recent matches, winrate, most played heroes. **Meta heroes** - filter by pro pick rates, sort by win rate. **Player comparison** - compare stats between two players. **Pro match monitor** - poll for new pro matches. **Batch collection** - paginate through high MMR matches with rate limiting.

## Analyze Match Performance

```python
from opendota import OpenDota

async def analyze_match(match_id: int):
    async with OpenDota() as client:
        match = await client.get_match(match_id)

        print(f"Match {match_id} Analysis:")
        print(f"Duration: {match.duration // 60}m {match.duration % 60}s")
        print(f"Winner: {'Radiant' if match.radiant_win else 'Dire'}")
        print(f"Score: {match.radiant_score} - {match.dire_score}")

        # Find MVP by KDA
        best_kda = max(
            match.players,
            key=lambda p: (p.kills + p.assists) / max(p.deaths, 1)
        )
        team = "Radiant" if best_kda.player_slot < 128 else "Dire"
        print(f"Best KDA: {best_kda.kills}/{best_kda.deaths}/{best_kda.assists} ({team})")

        # Team gold comparison
        radiant_gpm = sum(p.gold_per_min for p in match.players if p.player_slot < 128)
        dire_gpm = sum(p.gold_per_min for p in match.players if p.player_slot >= 128)
        print(f"Avg GPM - Radiant: {radiant_gpm/5:.0f}, Dire: {dire_gpm/5:.0f}")
```

## Track Player Progress

```python
from opendota import OpenDota

async def track_player(account_id: int):
    async with OpenDota() as client:
        # Get player profile
        player = await client.get_player(account_id)
        print(f"Player: {player.profile.personaname}")
        print(f"Rank: {player.rank_tier}")

        # Get recent matches
        matches = await client.get_player_matches(account_id, limit=20)

        wins = sum(1 for m in matches if (m.player_slot < 128) == m.radiant_win)
        total = len(matches)
        winrate = wins / total * 100

        avg_kills = sum(m.kills for m in matches) / total
        avg_deaths = sum(m.deaths for m in matches) / total
        avg_assists = sum(m.assists for m in matches) / total

        print(f"Last {total} matches:")
        print(f"Winrate: {winrate:.1f}% ({wins}/{total})")
        print(f"Avg KDA: {avg_kills:.1f}/{avg_deaths:.1f}/{avg_assists:.1f}")

        # Most played heroes
        hero_counts = {}
        for match in matches:
            hero_counts[match.hero_id] = hero_counts.get(match.hero_id, 0) + 1

        heroes = await client.get_heroes()
        hero_names = {h.id: h.localized_name for h in heroes}

        print("Most played heroes:")
        for hero_id, count in sorted(hero_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"  {hero_names.get(hero_id, 'Unknown')}: {count} games")
```

## Find Meta Heroes

```python
from opendota import OpenDota

async def find_meta_heroes():
    async with OpenDota() as client:
        hero_stats = await client.get_hero_stats()

        # Filter heroes with significant pick rates
        meta_heroes = [h for h in hero_stats if (h.pro_pick or 0) > 50]

        # Sort by win rate
        meta_heroes.sort(
            key=lambda h: (h.pro_win or 0) / max(h.pro_pick or 1, 1),
            reverse=True
        )

        print("Current meta heroes (high pick + win rate):")
        for hero in meta_heroes[:10]:
            if hero.pro_pick and hero.pro_win:
                winrate = hero.pro_win / hero.pro_pick * 100
                print(f"{hero.localized_name}: {winrate:.1f}% WR ({hero.pro_pick} picks)")
```

## Compare Two Players

```python
from opendota import OpenDota

async def compare_players(player1_id: int, player2_id: int):
    async with OpenDota() as client:
        p1 = await client.get_player(player1_id)
        p2 = await client.get_player(player2_id)

        p1_matches = await client.get_player_matches(player1_id, limit=50)
        p2_matches = await client.get_player_matches(player2_id, limit=50)

        def calc_stats(matches):
            wins = sum(1 for m in matches if (m.player_slot < 128) == m.radiant_win)
            avg_kda = sum(m.kills + m.assists for m in matches) / max(sum(m.deaths for m in matches), 1)
            return {"winrate": wins / len(matches) * 100, "kda": avg_kda}

        stats1 = calc_stats(p1_matches)
        stats2 = calc_stats(p2_matches)

        print(f"Comparison: {p1.profile.personaname} vs {p2.profile.personaname}")
        print(f"Winrate: {stats1['winrate']:.1f}% vs {stats2['winrate']:.1f}%")
        print(f"Avg KDA: {stats1['kda']:.2f} vs {stats2['kda']:.2f}")
```

## Pro Match Monitor

```python
from opendota import OpenDota
import asyncio

async def monitor_pro_matches():
    async with OpenDota() as client:
        last_match_id = None

        while True:
            pro_matches = await client.get_pro_matches()

            for match in pro_matches:
                if last_match_id and match.match_id <= last_match_id:
                    break

                if match.radiant_name and match.dire_name:
                    winner = match.radiant_name if match.radiant_win else match.dire_name
                    print(f"[{match.league_name}] {match.radiant_name} vs {match.dire_name}")
                    print(f"  Winner: {winner} ({match.duration // 60}m)")

            if pro_matches:
                last_match_id = pro_matches[0].match_id

            await asyncio.sleep(60)  # Check every minute
```

## Batch Data Collection

```python
from opendota import OpenDota
import asyncio

async def collect_high_mmr_matches(count: int = 100):
    async with OpenDota() as client:
        all_matches = []
        last_match_id = None

        while len(all_matches) < count:
            matches = await client.get_public_matches(
                mmr_descending=6000,
                less_than_match_id=last_match_id
            )

            if not matches:
                break

            all_matches.extend(matches)
            last_match_id = matches[-1].match_id

            # Respect rate limits
            await asyncio.sleep(1)

        print(f"Collected {len(all_matches)} high MMR matches")
        return all_matches[:count]
```
