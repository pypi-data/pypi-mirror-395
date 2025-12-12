import pytest
from utils import normalize_data, calculate_simulation_score, summarize_simulation

def test_normalize_data():
    data = [10, 20, 30]
    normalized = normalize_data(data)
    assert min(normalized) == 0
    assert max(normalized) == 1

def test_calculate_simulation_score():
    metrics = {"accuracy": 0.9, "efficiency": 0.8, "stability": 0.7}
    score = calculate_simulation_score(metrics)
    assert 0 <= score <= 1

def test_summarize_simulation():
    metrics = {"accuracy": 0.9, "efficiency": 0.8, "stability": 0.7}
    summary = summarize_simulation(metrics)
    assert "Simulation Score" in summary