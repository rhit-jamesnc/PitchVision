def calculate_pass_difficulty(pass_distance, nearest_defender_distance):
    pressure_factor = max(0.0, 1.0 - (nearest_defender_distance / 5.0))
    distance_factor = min(1.0, pass_distance / 40.0)
    
    difficulty = (0.3 * distance_factor) + (0.7 * pressure_factor)
    return min(1.0, max(0.0, difficulty))