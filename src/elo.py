def update_elo(elo, correct, K=30):
    if correct:
        elo += K
    else:
        elo -= K

    if elo < 0:
        elo = 0

    return elo


def get_difficulty(elo):
    if elo < 500:
        return 0  # Easy
    elif elo < 1000:
        return 1  # Medium
    elif elo < 1500:
        return 2  # Hard
    else:
        return 3  # Expert