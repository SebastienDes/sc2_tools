"""Unit tests for data loading functions."""
import json
import pandas as pd
import pytest

from io import StringIO
from unittest.mock import patch, mock_open

from src.data_loader import load_players_entries, load_mu_probabilities, load_players_standings

# TEST LOAD PLAYERS
# Test for successful load
def test_load_players_success():
    test_data = [
        {"player_id": 101, "name": "Maru", "team": "Team NV", "status": "Qualified"},
        {"player_id": 102, "name": "Serral", "team": "ENCE", "status": "Qualified"}
    ]
    # Mock the open function to return this test data as file content
    with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
        result = load_players_entries("dummy_path.json")
        assert result == test_data, "Failed to load player data correctly"

# Test for handling file not found error
def test_load_players_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_players_entries("nonexistent_path.json")

# Test for JSON decode error (corrupted file)
def test_load_players_corrupted_json():
    with patch('builtins.open', mock_open(read_data="{bad json")):
        with pytest.raises(json.JSONDecodeError):
            load_players_entries("dummy_path.json")

# TEST LOAD PROBABILITIES
def test_load_probabilities_success():
    # Mock data for a correctly formatted CSV
    data = """player_id1,player_id2,format,outcomes
              49,485,bo7,"3-0:1.58,3-1:4.09,3-2:6.59,2-3:8.51,1-3:15.48,0-3:21.82,0-4:24.60,1-4:17.34"
              101,102,bo5,"3-0:5.00,3-1:10.00,3-2:15.00,2-3:20.00,1-3:25.00,0-3:15.00" """
    df = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=df):
        result = load_mu_probabilities('dummy_path.csv')
        assert not result.empty
        assert 'outcomes' in result.columns
        assert isinstance(result.at[0, 'outcomes'], dict)

def test_missing_columns():
    # Data missing one required column
    data = """player_id1,player_id2,outcomes
              49,485,"3-0:1.58,3-1:4.09" """
    df = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=df):
        with pytest.raises(ValueError) as excinfo:
            load_mu_probabilities('dummy_path.csv')
        assert "Missing columns: {'format'}" in str(excinfo.value)

def test_incorrect_data_type():
    # Incorrect data type for player_id1
    data = """player_id1,player_id2,format,outcomes
              "one hundred",485,bo7,"3-0:1.58,3-1:4.09" """
    df = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=df):
        with pytest.raises(ValueError) as excinfo:
            load_mu_probabilities('dummy_path.csv')
        assert "Column 'player_id1' should contain only integer values." in str(excinfo.value)

def test_unexpected_format_values():
    # Unexpected value in the format column
    data = """player_id1,player_id2,format,outcomes
              49,485,bo9,"3-0:1.58,3-1:4.09" """
    df = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=df):
        with pytest.raises(ValueError) as excinfo:
            load_mu_probabilities('dummy_path.csv')
        assert "Format column contains unexpected values" in str(excinfo.value)

def test_outcomes_parsing_error():
    # Malformed outcomes string
    data = """player_id1,player_id2,format,outcomes
              49,485,bo7,"3-0:1.58,3-1" """
    df = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=df):
        with pytest.raises(ValueError) as excinfo:
            load_mu_probabilities('dummy_path.csv')
        assert "Error parsing outcomes string" in str(excinfo.value)

# TEST LOAD STANDINGS
def test_load_players_standings_success():
    # Mock data representing a correctly formatted CSV file
    data = """player_id,name,region,ept_points
              101,Maru,Korea,1500
              102,Serral,Europe,1400
              103,Reynor,Europe,1350"""
    mock_data = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=mock_data):
        result = load_players_standings('dummy_path.csv')
        assert not result.empty
        assert list(result.columns) == ['player_id', 'name', 'region', 'ept_points']
        assert result.iloc[0]['player_id'] == 101

def test_load_players_standings_missing_columns():
    # Data missing one column
    data = """player_id,name,ept_points
              101,Maru,1500
              102,Serral,1400"""
    mock_data = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=mock_data):
        with pytest.raises(ValueError) as excinfo:
            load_players_standings('dummy_path.csv')
        assert "Missing columns: {'region'}" in str(excinfo.value)

def test_load_players_standings_incorrect_data_type():
    # Incorrect data type for player_id
    data = """player_id,name,region,ept_points
              "one hundred",Maru,Korea,1500"""
    mock_data = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=mock_data):
        with pytest.raises(ValueError) as excinfo:
            load_players_standings('dummy_path.csv')
        assert "Column 'player_id' should contain only integer values" in str(excinfo.value)

def test_load_players_standings_unexpected_region():
    # Unexpected value in region
    data = """player_id,name,region,ept_points
              101,Maru,Space,1500"""
    mock_data = pd.read_csv(StringIO(data))
    
    with patch('pandas.read_csv', return_value=mock_data):
        with pytest.raises(ValueError) as excinfo:
            load_players_standings('dummy_path.csv')
        assert "Region column contains unexpected values" in str(excinfo.value)