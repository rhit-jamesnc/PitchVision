from src.analytics import calculate_pass_difficulty

def test_pass_difficulty_basic():
    # A short 5-meter pass with zero pressure should be very easy (low difficulty)
    difficulty = calculate_pass_difficulty(pass_distance=5.0, nearest_defender_distance=10.0)
    assert difficulty < 0.2

def test_pass_difficulty_high_pressure():
    # A pass under heavy pressure (defender 0.5 meters away) should have high difficulty
    difficulty = calculate_pass_difficulty(pass_distance=15.0, nearest_defender_distance=0.5)
    assert difficulty > 0.7