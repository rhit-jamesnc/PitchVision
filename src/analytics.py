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