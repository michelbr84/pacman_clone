"""JSON persistence for settings and highscores.

Paths are hard-coded under `savegame/` and names are sanitised — external input
(player initials) must be cleansed to a-z/A-Z/0-9 before being written.
"""
import json
import os
import re

SAVE_DIR = "savegame"
SETTINGS_PATH = os.path.join(SAVE_DIR, "settings.json")
SCORES_PATH = os.path.join(SAVE_DIR, "highscores.json")

DEFAULT_SETTINGS = {
    "master_volume": 0.8,
    "music_volume": 0.6,
    "sfx_volume": 0.9,
    "difficulty": "Normal",
}

_SAFE_NAME = re.compile(r"[^A-Za-z0-9]")


def _ensure_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_SETTINGS)
    merged = dict(DEFAULT_SETTINGS)
    for k, v in data.items():
        if k in merged:
            merged[k] = v
    return merged


def save_settings(settings):
    _ensure_dir()
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def sanitise_name(name):
    cleaned = _SAFE_NAME.sub("", name or "")[:8].upper()
    return cleaned or "PLAYER"


def load_scores():
    if not os.path.exists(SCORES_PATH):
        return []
    try:
        with open(SCORES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    return data


def save_score(name, score):
    _ensure_dir()
    scores = load_scores()
    scores.append({"name": sanitise_name(name), "score": int(score)})
    scores.sort(key=lambda s: s.get("score", 0), reverse=True)
    scores[:] = scores[:10]
    with open(SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
    return scores
