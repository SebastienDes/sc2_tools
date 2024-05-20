"""Unit tests for the analysis functions."""
import pytest
from src.analysis import simulate_match
from src.data_loader import load_mu_probabilities


@pytest.fixture
def mock_probabilities_df(monkeypatch):
    import pandas as pd
    # Create a mock DataFrame
    test_data = {
        'player_id1': [101, 101, 102],
        'player_id2': [102, 103, 103],
        'format': ['bo3', 'bo5', 'bo7'],
        'outcomes': [
            {'2-0': 30.00, '2-1': 70.00, '1-2': 0.00, '0-2': 0.00},
            {'3-0': 20.00, '3-1': 30.00, '3-2': 50.00, '2-3': 0.00, '1-3': 0.00, '0-3': 0.00},
            {'4-0': 10.00, '4-1': 20.00, '4-2': 30.00, '4-3': 40.00, '3-4': 0.00, '2-4': 0.00, '1-4': 0.00, '0-4': 0.00}
        ]
    }
    mock_df = pd.DataFrame(test_data)
    # Use monkeypatch to replace the DataFrame in your analysis module
    monkeypatch.setattr('src.analysis.probabilities_df', mock_df)

def test_simulate_match_bo3(mock_probabilities_df):
    assert simulate_match(101, 102, 'bo3') == '2-1', "BO3 match outcome is incorrect"

def test_simulate_match_bo5(mock_probabilities_df):
    assert simulate_match(101, 103, 'bo5') == '3-2', "BO5 match outcome is incorrect"

def test_simulate_match_bo7(mock_probabilities_df):
    assert simulate_match(102, 103, 'bo7') == '4-3', "BO7 match outcome is incorrect"

