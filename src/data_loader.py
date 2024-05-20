"""Scripts to load and preprocess data."""
import json
import pandas as pd


EXPECTED_FORMATS = {'bo3', 'bo5', 'bo7'}
EXPECTED_REGIONS = {'Korea', 'Europe', 'Americas', 'Asia'}

def load_players_entries(json_filepath):
    """Load players json and returns it as list of dict."""
    required_keys = {'player_id', 'name', 'team', 'status'}
    
    with open(json_filepath, 'r') as f:
        players_entries = json.load(f)
    
    for entry in players_entries:
        if not required_keys.issubset(entry.keys()):
            missing_keys = required_keys - entry.keys()
            raise ValueError(f"Missing keys in entry: {missing_keys}")
    
    return players_entries


def parse_outcomes(outcome_str):
    outcomes = {}
    try:
        for outcome in outcome_str.split(','):
            score, probability = outcome.split(':')
            outcomes[score] = float(probability)
    except ValueError:
        raise ValueError(f"Error parsing outcomes string: '{outcome_str}'")
    return outcomes


def load_mu_probabilities(csv_filepath):
    """Load match-up probabilities and returns it as pandas df."""
    try:
        mu_probabilities = pd.read_csv(csv_filepath)
    except Exception as e:
        raise ValueError(f"Failed to load CSV file: {e}")
    
    required_columns = ['player_id1', 'player_id2', 'format', 'outcomes']
    missing_columns = set(required_columns) - set(mu_probabilities.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")
    
    if not pd.api.types.is_integer_dtype(mu_probabilities['player_id1']):
        raise ValueError("Column 'player_id1' should contain only integer values.")
    if not pd.api.types.is_integer_dtype(mu_probabilities['player_id2']):
        raise ValueError("Column 'player_id2' should contain only integer values.")
    
    if not set(mu_probabilities['format']).issubset(EXPECTED_FORMATS):
        raise ValueError("Format column contains unexpected values.")
    
    try:
        mu_probabilities['outcomes'] = mu_probabilities['outcomes'].apply(parse_outcomes)
    except Exception as e:
        raise ValueError(f"Error processing outcomes data: {e}")
    
    return mu_probabilities


def load_players_standings(csv_filepath):
    """Loads the standings from a CSV file into a pandas DataFrame with validity checks."""
    try:
        standings = pd.read_csv(csv_filepath)
    except Exception as e:
        raise ValueError(f"Failed to load CSV file: {e}")
    
    required_columns = ['player_id', 'name', 'region', 'ept_points']
    
    missing_columns = set(required_columns) - set(standings.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if not pd.api.types.is_integer_dtype(standings['player_id']):
        raise ValueError("Column 'player_id' should contain only integer values.")
    if not pd.api.types.is_integer_dtype(standings['ept_points']):
        raise ValueError("Column 'ept_points' should contain only integer values.")
    
    if not set(standings['region']).issubset(EXPECTED_REGIONS):
        raise ValueError("Region column contains unexpected values.")
    
    return standings