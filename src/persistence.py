
import json
from pathlib import Path

_STORE = Path("player.json")

def _init_store():
    if not _STORE.exists():
        with _STORE.open("w", encoding="utf-8") as f:
            json.dump({"elo": 1000.0, "history": [1000.0]}, f)

def load_elo():
    _init_store()
    with _STORE.open("r", encoding="utf-8") as f:
        return float(json.load(f)["elo"])

def load_history():
    _init_store()
    with _STORE.open("r", encoding="utf-8") as f:
        return list(json.load(f)["history"])

def save_elo(value):
    _init_store()
    with _STORE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data["elo"] = float(value)
    with _STORE.open("w", encoding="utf-8") as f:
        json.dump(data, f)

def save_history(hist):
    _init_store()
    with _STORE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data["history"] = list(hist)
    with _STORE.open("w", encoding="utf-8") as f:
        json.dump(data, f)


