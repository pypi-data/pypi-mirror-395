#!/usr/bin/env python3
"""
Example: Run a complete chess tournament using the Paircraft API.

This script demonstrates the full tournament lifecycle:
1. Create a tournament
2. Add players
3. Generate pairings for each round
4. Enter results
5. Get final standings and prizes
"""

from paircraft import ChessTournamentClient

# Use the test API key for demonstration
API_KEY = "test-api-key-full-access"


def main():
    # Initialize the client
    client = ChessTournamentClient(api_key=API_KEY)
    
    print("=" * 60)
    print("Chess Tournament API - Full Tournament Example")
    print("=" * 60)
    
    # 1. Create a tournament
    print("\n1. Creating tournament...")
    tournament = client.tournaments.create(
        name="API Example Tournament",
        date="2024-12-15",
        rounds=4,
        time_control="G/30+5",
        location="Online",
        format="swiss"
    )
    print(f"   Created: {tournament.name} (ID: {tournament.id})")
    
    # 2. Add players
    print("\n2. Adding players...")
    players_data = [
        {"name": "Magnus Carlsen", "rating": 2830},
        {"name": "Hikaru Nakamura", "rating": 2780},
        {"name": "Fabiano Caruana", "rating": 2766},
        {"name": "Wesley So", "rating": 2750},
        {"name": "Anish Giri", "rating": 2740},
        {"name": "Levon Aronian", "rating": 2735},
        {"name": "Ding Liren", "rating": 2760},
        {"name": "Ian Nepomniachtchi", "rating": 2775},
    ]
    
    result = client.players.import_players(tournament.id, players_data)
    print(f"   Imported {result.get('imported', len(players_data))} players")
    
    # 3. Run each round
    for round_num in range(1, tournament.rounds + 1):
        print(f"\n{'='*60}")
        print(f"ROUND {round_num}")
        print("=" * 60)
        
        # Generate pairings
        print(f"\n3.{round_num}a. Generating pairings for round {round_num}...")
        pairings = client.pairings.generate(tournament.id, round=round_num)
        
        print(f"   Generated {len(pairings)} pairings:")
        for pairing in pairings:
            if pairing.is_bye:
                print(f"     Board {pairing.board}: {pairing.white_name} (BYE)")
            else:
                print(f"     Board {pairing.board}: {pairing.white_name} ({pairing.white_rating}) vs "
                      f"{pairing.black_name} ({pairing.black_rating})")
        
        # Simulate results (alternating patterns for variety)
        print(f"\n3.{round_num}b. Entering results...")
        results = []
        result_patterns = ["1-0", "0-1", "1/2-1/2", "1-0", "0-1"]
        
        for i, pairing in enumerate(pairings):
            if not pairing.is_bye:
                result_val = result_patterns[(round_num + i) % len(result_patterns)]
                results.append({
                    "pairing_id": pairing.id,
                    "result": result_val
                })
        
        if results:
            batch_result = client.pairings.set_results(tournament.id, results)
            print(f"   Entered {batch_result.get('processed', len(results))} results")
        
        # Check round status
        status = client.pairings.round_status(tournament.id, round_num)
        print(f"   Round {round_num} complete: {status.is_complete} "
              f"({status.completion_percentage}% complete)")
    
    # 4. Get final standings
    print(f"\n{'='*60}")
    print("FINAL STANDINGS")
    print("=" * 60)
    
    standings = client.tournaments.standings(tournament.id)
    for section_name, players in standings.items():
        print(f"\n{section_name} Section:")
        print("-" * 40)
        for player in players[:10]:  # Top 10
            print(f"  {player.rank:2}. {player.name:<25} {player.total_points:>5.1f} pts "
                  f"({player.games_played} games)")
    
    # 5. Get prizes/winners
    print(f"\n{'='*60}")
    print("PRIZE WINNERS")
    print("=" * 60)
    
    prizes = client.tournaments.prizes(tournament.id)
    for section in prizes["sections"]:
        print(f"\n{section.name} Section:")
        print("-" * 40)
        for winner in section.winners[:5]:  # Top 5 prizes
            if winner.amount:
                print(f"  {winner.position}. {winner.player_name:<25} ${winner.amount:.2f} "
                      f"({winner.prize_name})")
            else:
                print(f"  {winner.position}. {winner.player_name:<25} {winner.prize_name}")
    
    print(f"\nTournament Summary:")
    print(f"  Total prize money: ${prizes['summary'].get('total_prize_money', 0):.2f}")
    print(f"  Total winners: {prizes['summary'].get('total_winners', 0)}")
    
    # Cleanup - delete the test tournament
    print(f"\n{'='*60}")
    print("Cleaning up...")
    client.tournaments.delete(tournament.id)
    print(f"Deleted tournament: {tournament.id}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
