import pygame

from scripts import config
from scripts.game_state import GameState

CREDITS = [
    "PAC-MAN  —  AAA EDITION",
    "",
    "Original clone:  michelbr84",
    "AAA upgrade:     ClaudeMaxPower agent team",
    "Framework:       Pygame 2.6.1",
    "",
    "Powered by superpowers skills",
    "and the Claude Code agent harness.",
]


def run(screen, clock, sm):
    font_big = pygame.font.Font(config.FONT_PATH, 30)
    font = pygame.font.Font(config.FONT_PATH, 20)
    font_small = pygame.font.Font(config.FONT_PATH, 16)

    while sm.current == GameState.CREDITS:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sm.transition(GameState.MENU)
                return
            if ev.type == pygame.KEYDOWN and ev.key in (
                pygame.K_ESCAPE,
                pygame.K_RETURN,
            ):
                sm.transition(GameState.MENU)
                return

        screen.fill(config.BLACK)
        y = 120
        for i, line in enumerate(CREDITS):
            f = font_big if i == 0 else font
            color = config.YELLOW if i == 0 else config.WHITE
            surf = f.render(line, True, color)
            screen.blit(surf, surf.get_rect(center=(config.SCREEN_WIDTH // 2, y)))
            y += 42 if i == 0 else 30

        hint = font_small.render("Enter / Esc: back", True, (150, 150, 150))
        screen.blit(
            hint,
            hint.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 24)),
        )
        pygame.display.flip()
        clock.tick(60)
