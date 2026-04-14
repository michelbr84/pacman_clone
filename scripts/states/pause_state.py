import pygame

from scripts import config
from scripts.game_state import GameState


def run(screen, clock, sm):
    font_big = pygame.font.Font(config.FONT_PATH, 48)
    font_small = pygame.font.Font(config.FONT_PATH, 20)
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(140)
    overlay.fill((0, 0, 0))

    while sm.current == GameState.PAUSED:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sm.transition(GameState.MENU)
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_p, pygame.K_RETURN):
                    sm.pop()
                    return
                if ev.key == pygame.K_ESCAPE:
                    sm.transition(GameState.MENU)
                    return

        screen.blit(overlay, (0, 0))
        text = font_big.render("PAUSED", True, config.YELLOW)
        screen.blit(text, text.get_rect(center=(config.SCREEN_WIDTH // 2, 240)))
        hint = font_small.render(
            "Press P or Enter to resume  -  Esc to quit to menu", True, config.WHITE
        )
        screen.blit(hint, hint.get_rect(center=(config.SCREEN_WIDTH // 2, 320)))
        pygame.display.flip()
        clock.tick(30)
