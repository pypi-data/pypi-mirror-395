# Paircraft - Chess Tournament API SDK

A Python library for interacting with the Paircraft API. Manage chess tournaments, players, pairings, and results programmatically.

## Installation

```bash
pip install paircraft
```

## Quick Start

```python
from paircraft import ChessTournamentClient

# Initialize the client
client = ChessTournamentClient(api_key="your-api-key")

# Create a tournament
tournament = client.tournaments.create(
    name="Spring Open 2024",
    date="2024-03-15",
    rounds=5,
    time_control="G/60+5"
)

# Add players
client.players.add(tournament.id, [
    {"name": "Magnus Carlsen", "rating": 2830},
    {"name": "Hikaru Nakamura", "rating": 2780},
    {"name": "Fabiano Caruana", "rating": 2766},
    {"name": "Wesley So", "rating": 2750},
])

# Generate pairings for round 1
pairings = client.pairings.generate(tournament.id, round=1)

# Enter results
for pairing in pairings:
    client.pairings.set_result(tournament.id, pairing.id, result="1-0")

# Get standings
standings = client.tournaments.standings(tournament.id)
for player in standings:
    print(f"{player.rank}. {player.name}: {player.total_points} points")

# Get prize winners
prizes = client.tournaments.prizes(tournament.id)
for section in prizes.sections:
    print(f"\n{section.name} Section:")
    for winner in section.winners:
        print(f"  {winner.position}. {winner.player_name} - {winner.prize_name}")
```

## Features

- **Tournament Management**: Create, update, delete, and list tournaments
- **Player Management**: Add, import, update, and remove players
- **Pairing Generation**: Swiss system pairings with configurable options
- **Result Entry**: Single and batch result submission
- **Standings**: Real-time standings with tiebreakers
- **Prize Calculation**: Automatic prize distribution by section

## API Reference

### ChessTournamentClient

The main client for interacting with the API.

```python
client = ChessTournamentClient(
    api_key="your-api-key",
    base_url="https://chess-tournament-director-6ce5e76147d7.herokuapp.com"
)
```

### Tournaments

```python
# List all tournaments
tournaments = client.tournaments.list()

# Get a specific tournament
tournament = client.tournaments.get(tournament_id)

# Create a tournament
tournament = client.tournaments.create(
    name="Tournament Name",
    date="2024-03-15",
    rounds=5,
    time_control="G/60+5",
    location="Chess Club",
    format="swiss"  # or "round_robin"
)

# Update a tournament
client.tournaments.update(tournament_id, name="New Name")

# Delete a tournament
client.tournaments.delete(tournament_id)

# Get standings
standings = client.tournaments.standings(tournament_id, section="Open")

# Get prizes/winners
prizes = client.tournaments.prizes(tournament_id)
```

### Players

```python
# List players in a tournament
players = client.players.list(tournament_id)

# Get a specific player
player = client.players.get(tournament_id, player_id)

# Add a single player
player = client.players.add(tournament_id, {
    "name": "John Doe",
    "rating": 1500,
    "uscf_id": "12345678"
})

# Import multiple players
result = client.players.import_players(tournament_id, [
    {"name": "Player 1", "rating": 1500},
    {"name": "Player 2", "rating": 1600},
])

# Update a player
client.players.update(tournament_id, player_id, rating=1550)

# Remove a player
client.players.delete(tournament_id, player_id)

# Withdraw a player
client.players.withdraw(tournament_id, player_id)
```

### Pairings

```python
# Get pairings for a round
pairings = client.pairings.list(tournament_id, round=1)

# Generate pairings
pairings = client.pairings.generate(tournament_id, round=1)

# Set a result
client.pairings.set_result(tournament_id, pairing_id, result="1-0")

# Batch results
client.pairings.set_results(tournament_id, [
    {"pairing_id": "id1", "result": "1-0"},
    {"pairing_id": "id2", "result": "0-1"},
    {"pairing_id": "id3", "result": "1/2-1/2"},
])

# Check round status
status = client.pairings.round_status(tournament_id, round=1)
```

## Result Formats

The API accepts the following result formats:

| Result | Meaning |
|--------|---------|
| `"1-0"` | White wins |
| `"0-1"` | Black wins |
| `"1/2-1/2"` or `"0.5-0.5"` | Draw |
| `"1F-0F"` | White wins by forfeit |
| `"0F-1F"` | Black wins by forfeit |
| `"0F-0F"` | Double forfeit |
| `"1-0 bye"` | Full-point bye |
| `"0.5-0.5 bye"` | Half-point bye |

## Error Handling

```python
from paircraft import ChessTournamentClient
from paircraft.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError
)

client = ChessTournamentClient(api_key="your-api-key")

try:
    tournament = client.tournaments.get("invalid-id")
except NotFoundError:
    print("Tournament not found")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except RateLimitError:
    print("Rate limit exceeded, try again later")
except APIError as e:
    print(f"API error: {e}")
```

## Testing

For testing, use the test API key:

```python
client = ChessTournamentClient(api_key="test-api-key-full-access")
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- **Website**: https://paircraft.io
- **API Docs**: https://paircraft.io/api/docs
- **GitHub**: https://github.com/chughjug/ratings
