import pygame

from scripts import config, persistence
from scripts.game_state import GameState


def run(screen, clock, sm):
    font_big = pygame.font.Font(config.FONT_PATH, 36)
    font = pygame.font.Font(config.FONT_PATH, 22)
    font_small = pygame.font.Font(config.FONT_PATH, 16)
    scores = persistence.load_scores()

    while sm.current == GameState.HIGHSCORES:
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
        t = font_big.render("HIGH SCORES", True, config.YELLOW)
        screen.blit(t, t.get_rect(center=(config.SCREEN_WIDTH // 2, 80)))

        if not scores:
            empty = font.render("No scores yet — go play!", True, config.WHITE)
            screen.blit(
                empty, empty.get_rect(center=(config.SCREEN_WIDTH // 2, 280))
            )
        else:
            y = 160
            for i, s in enumerate(scores[:10]):
                name = s.get("name", "????")
                score = s.get("score", 0)
                line = font.render(f"{i + 1:2d}.  {name:<8}  {score:>5d}", True, config.WHITE)
                screen.blit(line, line.get_rect(center=(config.SCREEN_WIDTH // 2, y)))
                y += 34

        hint = font_small.render("Enter / Esc: back", True, (150, 150, 150))
        screen.blit(
            hint,
            hint.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 24)),
        )
        pygame.display.flip()
        clock.tick(60)
