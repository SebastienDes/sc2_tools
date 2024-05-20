"""Core functionalities to calculate qualifications."""
import pandas as pd
from data_loader import load_players_entries, load_mu_probabilities, load_players_standings

# Load data at module level so it can be reused across different functions without reloading
players_df = load_players_entries('data/players.json')
probabilities_df = load_mu_probabilities('data/probabilities.csv')
standings_df = load_players_standings('data/standings.csv')

# MATCH PREDICTION
def simulate_match(player1_id, player2_id, format):
    # Filter the probabilities dataframe for the match
    match_probs = probabilities_df[(probabilities_df['player_id1'] == player1_id) &
                                   (probabilities_df['player_id2'] == player2_id) &
                                   (probabilities_df['format'] == format)]['outcomes'].iloc[0]

    # Determine match outcome based on probabilities
    outcomes = []
    for score, prob in match_probs.items():
        outcomes.append((score, prob))
    
    # Select a match outcome based on weighted probabilities
    outcomes.sort(key=lambda x: x[1], reverse=True)  # Sort by probability in descending order
    winning_score = outcomes[0][0]  # Most probable outcome
    return winning_score


# UPDATE STANDINGS
def update_standings(player1_id, player2_id, winning_score):
    player1_games, player2_games = map(int, winning_score.split('-'))
    if player1_games > player2_games:
        winner_id = player1_id
    else:
        winner_id = player2_id
    
    # Assuming a simplistic points update: +3 points for a win
    standings_df.loc[standings_df['player_id'] == winner_id, 'ept_points'] += 3


# QUALIFICATION SCENARIOS
def calculate_qualification_scenarios():
    # Assuming top 2 players from each region qualify
    qualified_players = standings_df.groupby('region').apply(
        lambda x: x.nlargest(2, 'ept_points')['name'].tolist()
    )
    return qualified_players.to_dict()
