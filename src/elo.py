def get_difficulty(elo):
    if elo < 500:
        return 0
    elif elo < 1000:
        return 1
    elif elo < 1500:
        return 2
    else:
        return 3

def update_elo(curr_elo, correct, q_diff_elo, hist, save_elo, save_history):
    K = 32
    expected = 1 / (1 + 10 ** ((q_diff_elo - curr_elo) / 400))
    score = 1 if correct else 0
    new_elo = curr_elo + K * (score - expected)
    save_elo(new_elo)
    hist.append(new_elo)
    save_history(hist)
    return new_elo
