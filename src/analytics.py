import numpy as np

def calculate_pass_difficulty(pass_distance, nearest_defender_distance):
    pressure_factor = max(0.0, 1.0 - (nearest_defender_distance / 5.0))
    distance_factor = min(1.0, pass_distance / 40.0)

    difficulty = (0.3 * distance_factor) + (0.7 * pressure_factor)
    return min(1.0, max(0.0, difficulty))

def calculate_decision_quality_score(chosen_option_difficulty, best_available_difficulty):
    if chosen_option_difficulty < best_available_difficulty:
        return 1.0
    penalty = chosen_option_difficulty - best_available_difficulty
    score = max(0.0, 1.0 - penalty)
    return score

def calculate_expected_pass_completion(pass_distance, nearest_defender_distance):
    difficulty = calculate_pass_difficulty(pass_distance, nearest_defender_distance)
    log_odds = 2.5 - (5.0 * difficulty)
    probability = 1.0 / (1.0 + np.exp(-log_odds))
    return float(probability)

def calculate_expected_goals(
    distance_to_goal, 
    angle_to_goal_degrees, 
    defenders_in_lane, 
    gk_distance, 
    body_part="strong_foot", 
    play_type="normal_pass"
):
    # Base distance decay (exponential drop-off as distance increases)
    # Beyond 35 meters, xG approaches 0
    distance_factor = max(0.0, 1.0 - (distance_to_goal / 35.0))
    
    # Angle factor: wider / central angles (around 40-50 degrees) are optimal; narrow angles reduce xG
    angle_factor = min(1.0, angle_to_goal_degrees / 50.0)
    
    # Defensive obstruction / goalkeeper pressure penalty
    defender_penalty = defenders_in_lane * 0.15
    gk_pressure_factor = min(1.0, gk_distance / 10.0)
    
    # Body part modifiers
    body_part_multipliers = {
        "strong_foot": 1.0,
        "weak_foot": 0.75,
        "header": 0.85,
        "other": 0.6
    }
    bp_multiplier = body_part_multipliers.get(body_part, 0.8)
    
    # Play type / assist modifiers (e.g., crosses or solo dribbles have different success profiles than normal passes)
    play_type_multipliers = {
        "normal_pass": 1.0,
        "cross": 0.8,
        "dribble": 0.9,
        "rebound": 1.2
    }
    pt_multiplier = play_type_multipliers.get(play_type, 0.9)
    
    # Core mathematical combination
    raw_xg = (0.5 * distance_factor) + (0.3 * angle_factor) + (0.2 * gk_pressure_factor)
    raw_xg -= defender_penalty
    
    final_xg = max(0.01, min(0.95, raw_xg * bp_multiplier * pt_multiplier))
    return float(final_xg)