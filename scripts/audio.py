"""Thin audio wrapper — loads optional SFX and honours settings volumes.

Missing WAV files are fine: the game runs silently for that channel.
Real assets can be dropped into `assets/sfx/` later (see docs/assets-todo.md).
"""
import os

import pygame

from scripts import persistence

SFX_DIR = "assets/sfx"
SFX_NAMES = ["chomp", "power", "death", "eat_ghost", "menu_move", "menu_select"]
SFX_EXTS = (".mp3", ".wav", ".ogg")  # first match wins

_sounds = {}
_loaded = False


def load():
    global _loaded
    if _loaded:
        return
    for name in SFX_NAMES:
        _sounds[name] = None
        for ext in SFX_EXTS:
            path = os.path.join(SFX_DIR, f"{name}{ext}")
            if os.path.exists(path):
                try:
                    _sounds[name] = pygame.mixer.Sound(path)
                except pygame.error:
                    _sounds[name] = None
                break
    _loaded = True
    apply_volumes()


def apply_volumes():
    settings = persistence.load_settings()
    master = settings.get("master_volume", 0.8)
    sfx = settings.get("sfx_volume", 0.9)
    music = settings.get("music_volume", 0.6)
    try:
        pygame.mixer.music.set_volume(master * music)
    except pygame.error:
        pass
    for snd in _sounds.values():
        if snd is not None:
            snd.set_volume(master * sfx)


def play(name):
    snd = _sounds.get(name)
    if snd is not None:
        try:
            snd.play()
        except pygame.error:
            pass
