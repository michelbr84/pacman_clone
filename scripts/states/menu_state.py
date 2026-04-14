import sys

import pygame

from scripts import config
from scripts.game_state import GameState
from scripts.ui.widgets import Button, Menu


def run(screen, clock, sm):
    def play():
        sm.context["score"] = 0
        sm.transition(GameState.PLAYING)

    def settings():
        sm.transition(GameState.SETTINGS)

    def scores():
        sm.transition(GameState.HIGHSCORES)

    def credits():
        sm.transition(GameState.CREDITS)

    def quit_():
        pygame.quit()
        sys.exit(0)

    cx = config.SCREEN_WIDTH // 2
    btn_w, btn_h = 220, 44
    x = cx - btn_w // 2
    menu = Menu(
        [
            Button((x, 220, btn_w, btn_h), "Play", play),
            Button((x, 274, btn_w, btn_h), "Settings", settings),
            Button((x, 328, btn_w, btn_h), "High Scores", scores),
            Button((x, 382, btn_w, btn_h), "Credits", credits),
            Button((x, 436, btn_w, btn_h), "Quit", quit_),
        ]
    )

    title_font = pygame.font.Font(config.FONT_PATH, 72)
    subtitle_font = pygame.font.Font(config.FONT_PATH, 16)
    t = 0

    while sm.current == GameState.MENU:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                quit_()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                quit_()
            menu.handle_event(ev)

        screen.fill(config.BLACK)
        # Pulsing yellow title.
        pulse = 200 + int(55 * abs(pygame.math.Vector2(1, 0).rotate(t).x))
        title = title_font.render("PAC-MAN", True, (pulse, pulse, 0))
        screen.blit(title, title.get_rect(center=(cx, 120)))
        subtitle = subtitle_font.render("AAA EDITION", True, config.WHITE)
        screen.blit(subtitle, subtitle.get_rect(center=(cx, 180)))

        menu.draw(screen)

        hint = subtitle_font.render(
            "Arrows / Mouse  -  Enter to select  -  Esc to quit", True, (120, 120, 120)
        )
        screen.blit(hint, hint.get_rect(center=(cx, config.SCREEN_HEIGHT - 24)))

        pygame.display.flip()
        clock.tick(60)
        t = (t + 6) % 360
