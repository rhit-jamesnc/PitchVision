import numpy as np
from src.analytics import (
    calculate_pass_difficulty, 
    calculate_decision_quality_score, 
    calculate_expected_pass_completion,
    calculate_expected_goals,
    calculate_dribble_space_score
)

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

def test_expected_pass_completion_extreme_boundaries():
    # Extreme edge cases: zero distance with maximum defender distance, and max distance with zero defender distance
    xpc_easy = calculate_expected_pass_completion(pass_distance=0.0, nearest_defender_distance=20.0)
    xpc_hard = calculate_expected_pass_completion(pass_distance=50.0, nearest_defender_distance=0.0)
    
    assert 0.0 <= xpc_easy <= 1.0
    assert 0.0 <= xpc_hard <= 1.0
    assert xpc_easy > xpc_hard

def test_expected_goals_tap_in():
    # Extremely high value: 3 meters out, central angle, 0 defenders, strong foot, tap-in/rebound
    xg = calculate_expected_goals(
        distance_to_goal=3.0, 
        angle_to_goal_degrees=60.0, 
        defenders_in_lane=0, 
        gk_distance=2.0, 
        body_part="strong_foot", 
        play_type="rebound"
    )
    assert xg > 0.75

def test_expected_goals_high_value_shot():
    # Ideal shot: close range, central angle, 0 blocking defenders, normal pass assist, strong foot
    xg = calculate_expected_goals(
        distance_to_goal=8.0, 
        angle_to_goal_degrees=45.0, 
        defenders_in_lane=0, 
        gk_distance=8.0, 
        body_part="strong_foot", 
        play_type="normal_pass"
    )
    assert xg > 0.45

def test_expected_goals_medium_value():
    # Moderate value: 16 meters out (around top of the box), decent angle, 1 defender in lane
    xg = calculate_expected_goals(
        distance_to_goal=16.0, 
        angle_to_goal_degrees=30.0, 
        defenders_in_lane=1, 
        gk_distance=12.0, 
        body_part="strong_foot", 
        play_type="normal_pass"
    )
    assert 0.4 <= xg <= 0.6

def test_expected_goals_low_value():
    # Low value: Long distance (28 meters), tight angle, 2 defenders blocking
    xg = calculate_expected_goals(
        distance_to_goal=28.0, 
        angle_to_goal_degrees=10.0, 
        defenders_in_lane=2, 
        gk_distance=20.0, 
        body_part="weak_foot", 
        play_type="dribble"
    )
    assert xg < 0.08

def test_expected_goals_halfway_line_stationed_gk():
    # Halfway line shot (50m) with the keeper back on the line (gk_distance = 0) should be near zero
    xg = calculate_expected_goals(
        distance_to_goal=50.0,
        angle_to_goal_degrees=5.0,
        defenders_in_lane=0,
        gk_distance=0.0,
        body_part="strong_foot",
        play_type="normal_pass"
    )
    assert xg < 0.01

def test_expected_goals_halfway_line_sweeper_keeper():
    # Halfway line shot (50m) with the keeper way off their line (gk_distance = 40) should be higher
    xg = calculate_expected_goals(
        distance_to_goal=50.0,
        angle_to_goal_degrees=5.0,
        defenders_in_lane=0,
        gk_distance=40.0,
        body_part="strong_foot",
        play_type="normal_pass"
    )
    assert xg > 0.05

def test_dribble_space_score_isolated_carrier():
    # Carrier is isolated with plenty of space around them (large Voronoi cell)
    carrier_pos = np.array([50.0, 34.0])
    opponent_positions = np.array([
        [70.0, 34.0],
        [40.0, 20.0],
        [40.0, 48.0]
    ])
    pitch_bounds = (105.0, 68.0) # Length, Width in meters

    score = calculate_dribble_space_score(carrier_pos, opponent_positions, pitch_bounds)
    # A large open cell should yield a high space/dribble viability score
    assert score > 0.7

def test_dribble_space_score_heavy_pressure():
    # Carrier is surrounded closely on all sides (tiny Voronoi cell)
    carrier_pos = np.array([50.0, 34.0])
    opponent_positions = np.array([
        [51.0, 34.0],
        [49.0, 34.0],
        [50.0, 35.0],
        [50.0, 33.0]
    ])
    pitch_bounds = (105.0, 68.0)

    score = calculate_dribble_space_score(carrier_pos, opponent_positions, pitch_bounds)
    assert score < 0.2