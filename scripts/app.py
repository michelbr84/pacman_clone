"""Application entrypoint. Owns the Pygame display, clock and state machine."""
import pygame

from scripts import config
from scripts.game_state import GameState, StateManager


def run():
    pygame.init()
    screen = pygame.display.set_mode([config.SCREEN_WIDTH, config.SCREEN_HEIGHT])
    pygame.display.set_caption("Pac-Man — AAA Edition")
    config.init_assets()

    from scripts import audio
    audio.load()

    clock = pygame.time.Clock()
    sm = StateManager(initial=GameState.MENU)

    # Imports are local to keep pygame initialised before sub-modules load assets.
    from scripts.states import (
        credits_state,
        gameover_state,
        highscores_state,
        menu_state,
        pause_state,
        playing_state,
        settings_state,
        win_state,
    )

    handlers = {
        GameState.MENU: menu_state,
        GameState.PLAYING: playing_state,
        GameState.PAUSED: pause_state,
        GameState.GAME_OVER: gameover_state,
        GameState.WIN: win_state,
        GameState.SETTINGS: settings_state,
        GameState.HIGHSCORES: highscores_state,
        GameState.CREDITS: credits_state,
    }

    while True:
        handler = handlers.get(sm.current)
        if handler is None:
            break
        handler.run(screen, clock, sm)

    pygame.quit()
