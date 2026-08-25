from src.analytics import calculate_pass_difficulty, calculate_decision_quality_score, calculate_expected_pass_completion

def test_pass_difficulty_basic():
    # A short 5-meter pass with zero pressure should be very easy (low difficulty)
    difficulty = calculate_pass_difficulty(pass_distance=5.0, nearest_defender_distance=10.0)
    assert difficulty < 0.2

def test_pass_difficulty_high_pressure():
    # A pass under heavy pressure (defender 0.5 meters away) should have high difficulty
    difficulty = calculate_pass_difficulty(pass_distance=15.0, nearest_defender_distance=0.5)
    assert difficulty > 0.7

def test_decision_quality_score_poor_choice():
    # If a player chooses a high difficulty option (0.8) when a low difficulty option (0.2) exists, score should be low
    dqs = calculate_decision_quality_score(chosen_option_difficulty=0.8, best_available_difficulty=0.2)
    assert dqs < 0.5

def test_decision_quality_score_good_choice():
    # If a player chooses an optimal or near-optimal low-difficulty option, score should be high
    dqs = calculate_decision_quality_score(chosen_option_difficulty=0.25, best_available_difficulty=0.2)
    assert dqs > 0.9

def test_decision_quality_score_best_choice():
    # If a player chooses the absolute best option available, score should be a perfect 1.0
    dqs = calculate_decision_quality_score(chosen_option_difficulty=0.2, best_available_difficulty=0.2)
    assert dqs == 1.0

def test_expected_pass_completion_high_probability():
    # A short pass with no defenders nearby should have a very high xPC
    xpc = calculate_expected_pass_completion(pass_distance=5.0, nearest_defender_distance=10.0)
    assert xpc > 0.9

def test_expected_pass_completion_medium_probability():
    # A moderate-distance pass with moderate pressure should yield a mid-range xPC
    xpc = calculate_expected_pass_completion(pass_distance=20.0, nearest_defender_distance=2.0)
    assert 0.3 <= xpc <= 0.7

def test_expected_pass_completion_low_probability():
    # A long-distance pass under heavy defensive pressure should have a low xPC
    xpc = calculate_expected_pass_completion(pass_distance=35.0, nearest_defender_distance=0.5)
    assert xpc < 0.3