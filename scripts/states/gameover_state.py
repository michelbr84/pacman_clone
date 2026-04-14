import pygame

from scripts import config, persistence
from scripts.game_state import GameState


def run(screen, clock, sm):
    font_big = pygame.font.Font(config.FONT_PATH, 56)
    font = pygame.font.Font(config.FONT_PATH, 22)
    font_small = pygame.font.Font(config.FONT_PATH, 16)
    score = sm.context.get("score", 0)
    persistence.save_score("PLAYER", score)

    while sm.current == GameState.GAME_OVER:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sm.transition(GameState.MENU)
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    sm.context["score"] = 0
                    sm.transition(GameState.PLAYING)
                    return
                if ev.key in (pygame.K_ESCAPE, pygame.K_m):
                    sm.transition(GameState.MENU)
                    return

        screen.fill(config.BLACK)
        t = font_big.render("GAME OVER", True, config.RED)
        screen.blit(t, t.get_rect(center=(config.SCREEN_WIDTH // 2, 220)))
        s = font.render(f"Score: {score}", True, config.WHITE)
        screen.blit(s, s.get_rect(center=(config.SCREEN_WIDTH // 2, 300)))
        hint = font_small.render(
            "Enter: play again  -  M / Esc: main menu", True, (160, 160, 160)
        )
        screen.blit(hint, hint.get_rect(center=(config.SCREEN_WIDTH // 2, 380)))
        pygame.display.flip()
        clock.tick(30)
