def update_elo(elo, correct, difficulty_index, quantum_k=None, base_K=30):
    difficulty_multiplier = 1 + 0.25 * difficulty_index
    if elo < 500:
        gain_multiplier = 1.5
        loss_multiplier = 0.5
    elif elo < 1000:
        gain_multiplier = 1.0
        loss_multiplier = 1.0
    else:
        gain_multiplier = 0.5
        loss_multiplier = 1.5
    k_base = base_K if quantum_k is None else quantum_k
    K = k_base * difficulty_multiplier
    if correct:
        elo += K * gain_multiplier
    else:
        elo -= K * loss_multiplier
    return max(elo, 0)


def get_difficulty(elo):
    if elo < 500:
        return 0
    elif elo < 1000:
        return 1
    elif elo < 1500:
        return 2
    else:
        return 3
