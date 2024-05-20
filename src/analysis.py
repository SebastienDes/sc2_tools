"""Core functionalities to calculate qualifications."""
import pandas as pd
from src.data_loader import load_players_entries, load_mu_probabilities, load_players_standings

players_df = load_players_entries('data/players.json')
probabilities_df = load_mu_probabilities('data/probabilities.csv')
standings_df = load_players_standings('data/standings.csv')

def simulate_match(player1_id, player2_id, format):
    match_probs = probabilities_df[(probabilities_df['player_id1'] == player1_id) &
                                   (probabilities_df['player_id2'] == player2_id) &
                                   (probabilities_df['format'] == format)]['outcomes'].iloc[0]

    outcomes = []
    for score, prob in match_probs.items():
        outcomes.append((score, prob))
    
    outcomes.sort(key=lambda x: x[1], reverse=True)
    winning_score = outcomes[0][0]
    return winning_score

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
