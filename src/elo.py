
def update_elo(elo, correct, difficulty_index, base_K=30):

    difficulty_multiplier = 1 + 0.25 * difficulty_index  # Easy=1, Medium=1.25, Hard=1.5, Expert=1.75

    if elo < 500:
        gain_multiplier = 1.5
        loss_multiplier = 0.5
    elif elo < 1000:
        gain_multiplier = 1.0
        loss_multiplier = 1.0
    else:
        gain_multiplier = 0.5
        loss_multiplier = 1.5

    K = base_K * difficulty_multiplier

    if correct:
        elo += K * gain_multiplier
    else:
        elo -= K * loss_multiplier

    return max(elo, 0)

def get_difficulty(elo):
    if elo < 500:
        return 0  # Easy
    elif elo < 1000:
        return 1  # Medium
    elif elo < 1500:
        return 2  # Hard
    else:
        return 3  # Expert