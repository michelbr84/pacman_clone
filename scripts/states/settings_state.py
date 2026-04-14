import pygame

from scripts import config, persistence
from scripts.game_state import GameState
from scripts.ui.widgets import Button, Menu, Slider, Toggle


def run(screen, clock, sm):
    settings = persistence.load_settings()
    font_big = pygame.font.Font(config.FONT_PATH, 36)

    def on_master(v):
        settings["master_volume"] = round(v, 2)
        pygame.mixer.music.set_volume(
            settings["master_volume"] * settings["music_volume"]
        )

    def on_music(v):
        settings["music_volume"] = round(v, 2)
        pygame.mixer.music.set_volume(
            settings["master_volume"] * settings["music_volume"]
        )

    def on_sfx(v):
        settings["sfx_volume"] = round(v, 2)

    difficulties = ["Easy", "Normal", "Hard"]
    diff_idx = (
        difficulties.index(settings["difficulty"])
        if settings["difficulty"] in difficulties
        else 1
    )

    def on_diff(value):
        settings["difficulty"] = value

    def back():
        persistence.save_settings(settings)
        sm.transition(GameState.MENU)

    cx = config.SCREEN_WIDTH // 2
    widgets = [
        Slider((cx - 160, 170, 320, 18), "Master Volume", settings["master_volume"], on_master),
        Slider((cx - 160, 230, 320, 18), "Music Volume", settings["music_volume"], on_music),
        Slider((cx - 160, 290, 320, 18), "SFX Volume", settings["sfx_volume"], on_sfx),
        Toggle((cx - 110, 340, 220, 36), "Difficulty", difficulties, diff_idx, on_diff),
        Button((cx - 60, 420, 120, 40), "Back", back),
    ]
    menu = Menu(widgets)
    pygame.mixer.music.set_volume(settings["master_volume"] * settings["music_volume"])

    while sm.current == GameState.SETTINGS:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                back()
                return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                back()
                return
            menu.handle_event(ev)

        screen.fill(config.BLACK)
        t = font_big.render("SETTINGS", True, config.YELLOW)
        screen.blit(t, t.get_rect(center=(cx, 100)))
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)
