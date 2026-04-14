import json
import os

import pytest

from scripts import persistence


@pytest.fixture(autouse=True)
def tmp_save_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(persistence, "SAVE_DIR", str(tmp_path))
    monkeypatch.setattr(
        persistence, "SETTINGS_PATH", str(tmp_path / "settings.json")
    )
    monkeypatch.setattr(
        persistence, "SCORES_PATH", str(tmp_path / "highscores.json")
    )
    yield tmp_path


def test_load_settings_missing_returns_defaults():
    s = persistence.load_settings()
    assert s == persistence.DEFAULT_SETTINGS


def test_save_then_load_settings():
    persistence.save_settings(
        {"master_volume": 0.3, "music_volume": 0.2, "sfx_volume": 1.0, "difficulty": "Hard"}
    )
    s = persistence.load_settings()
    assert s["master_volume"] == 0.3
    assert s["difficulty"] == "Hard"


def test_load_settings_ignores_unknown_keys():
    persistence.save_settings({"master_volume": 0.5, "rogue": "bad"})
    s = persistence.load_settings()
    assert "rogue" not in s
    assert s["master_volume"] == 0.5


def test_load_settings_corrupt_file_returns_defaults(tmp_save_dir):
    (tmp_save_dir / "settings.json").write_text("not json")
    assert persistence.load_settings() == persistence.DEFAULT_SETTINGS


def test_sanitise_name_rejects_path_chars():
    assert persistence.sanitise_name("../../etc/passwd") == "ETCPASSW"
    assert persistence.sanitise_name("") == "PLAYER"
    assert persistence.sanitise_name("abc DEF") == "ABCDEF"


def test_save_score_sorts_and_truncates():
    for i in range(15):
        persistence.save_score(f"p{i}", i * 10)
    scores = persistence.load_scores()
    assert len(scores) == 10
    assert scores[0]["score"] == 140
    assert scores[-1]["score"] == 50


def test_save_score_sanitises_name(tmp_save_dir):
    persistence.save_score("../evil", 42)
    data = json.loads((tmp_save_dir / "highscores.json").read_text())
    assert data[0]["name"] == "EVIL"


def test_load_scores_corrupt_returns_empty(tmp_save_dir):
    (tmp_save_dir / "highscores.json").write_text("{not: a list}")
    assert persistence.load_scores() == []
