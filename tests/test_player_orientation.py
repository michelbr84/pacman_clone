import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

from scripts.player import Player  # noqa: E402


def _make():
    return Player(0, 0, "images/pacman.png")


def _step(p):
    walls = pygame.sprite.Group()
    gate = pygame.sprite.Group()
    p.update(walls, gate)


def test_initial_angle_is_right():
    p = _make()
    assert p.last_angle == 0


def test_moving_left_sets_180():
    p = _make()
    p.change_x, p.change_y = -30, 0
    _step(p)
    assert p.last_angle == 180


def test_idle_keeps_last_angle():
    p = _make()
    p.change_x, p.change_y = -30, 0
    _step(p)
    assert p.last_angle == 180
    p.change_x, p.change_y = 0, 0  # player stops
    _step(p)
    assert p.last_angle == 180  # still facing left


def test_up_and_down():
    p = _make()
    p.change_x, p.change_y = 0, -30
    _step(p)
    assert p.last_angle == 90
    p.change_x, p.change_y = 0, 30
    _step(p)
    assert p.last_angle == -90
