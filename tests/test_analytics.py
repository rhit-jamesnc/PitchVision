from src.analytics import calculate_pass_difficulty

def test_pass_difficulty_basic():
    # A short 5-meter pass with zero pressure should be very easy (low difficulty)
    difficulty = calculate_pass_difficulty(pass_distance=5.0, nearest_defender_distance=10.0)
    assert difficulty < 0.2