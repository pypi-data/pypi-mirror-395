#!/usr/bin/env python3
"""
Quick Start: Basic Paircraft API usage examples.
"""

from paircraft import ChessTournamentClient

# Initialize with your API key
client = ChessTournamentClient(api_key="test-api-key-full-access")

# List all tournaments
print("Listing tournaments...")
tournaments = client.tournaments.list()
for tournament in tournaments.items:
    print(f"  - {tournament.name} ({tournament.status})")

# Create a simple tournament
print("\nCreating tournament...")
tournament = client.tournaments.create(
    name="Quick Start Example",
    rounds=3,
    time_control="G/15+10"
)
print(f"Created: {tournament.name} (ID: {tournament.id})")

# Add some players
print("\nAdding players...")
client.players.import_players(tournament.id, [
    {"name": "Alice", "rating": 1800},
    {"name": "Bob", "rating": 1750},
    {"name": "Charlie", "rating": 1700},
    {"name": "Diana", "rating": 1650},
])
print("Added 4 players")

# Generate round 1 pairings
print("\nGenerating pairings...")
pairings = client.pairings.generate(tournament.id, round=1)
for p in pairings:
    print(f"  Board {p.board}: {p.white_name} vs {p.black_name}")

# Enter results
print("\nEntering results...")
for p in pairings:
    client.pairings.set_result(tournament.id, p.id, "1-0")
print("All results entered")

# Get standings
print("\nStandings:")
standings = client.tournaments.standings(tournament.id)
for section, players in standings.items():
    for player in players:
        print(f"  {player.rank}. {player.name}: {player.total_points} pts")

# Cleanup
print("\nCleaning up...")
client.tournaments.delete(tournament.id)
print("Done!")
