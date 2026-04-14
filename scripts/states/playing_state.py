"""The PLAYING state — the original game loop, extracted verbatim from main.py.

Load-bearing quirks preserved per CLAUDE.md:
- 10 FPS clock tick (ghost direction lists and 30px movement deltas depend on it).
- Each ghost has `.changespeed(...)` called twice per frame; the second call is dead
  code but affects internal (turn, steps) state progression — do not remove.
- Pinky/Blinky/Inky/Clyde direction lists and `pl/bl/il/cl` max-turn values are fixed
  scripted AI, not pathfinding.
"""
import pygame

from scripts import audio, config, persistence
from scripts.block import Block
from scripts.directions import (
    Blinky_directions,
    Clyde_directions,
    Inky_directions,
    Pinky_directions,
    bl,
    cl,
    il,
    pl,
)
from scripts.game_state import GameState
from scripts.ghost import Ghost
from scripts.maze import setupGate, setupRoomOne
from scripts.particles import ParticleSystem
from scripts.player import Player

FRIGHTENED_MS = 7000
POWER_PELLET_POSITIONS = [(1, 1), (1, 17), (17, 1), (17, 17)]  # grid rows/cols
DIFFICULTY_SPEED = {"Easy": 0.8, "Normal": 1.0, "Hard": 1.3}

# Initial positions (from the original main.py).
w = 303 - 16
p_h = (7 * 60) + 19
m_h = (4 * 60) + 19
b_h = (3 * 60) + 19
i_w = 303 - 16 - 32
c_w = 303 + (32 - 16)


def run(screen, clock, sm):
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)
    gate = setupGate(all_sprites_list)

    p_turn, p_steps = 0, 0
    b_turn, b_steps = 0, 0
    i_turn, i_steps = 0, 0
    c_turn, c_steps = 0, 0

    Pacman = Player(w, p_h, "images/pacman.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    Blinky = Ghost(w, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(w, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(i_w, m_h, "images/Inky.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(c_w, m_h, "images/Clyde.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    power_pellets = pygame.sprite.RenderPlain()
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            is_power = (row, column) in POWER_PELLET_POSITIONS
            if is_power:
                block = Block(config.WHITE, 12, 12)
                block.rect.x = (30 * column + 6) + 22
                block.rect.y = (30 * row + 6) + 22
            else:
                block = Block(config.YELLOW, 4, 4)
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26
            if pygame.sprite.spritecollide(
                block, wall_list, False
            ) or pygame.sprite.spritecollide(block, pacman_collide, False):
                continue
            if is_power:
                power_pellets.add(block)
                all_sprites_list.add(block)
            else:
                block_list.add(block)
                all_sprites_list.add(block)

    bll = len(block_list) + len(power_pellets)
    score = 0
    particles = ParticleSystem()
    ghosts = [Pinky, Blinky, Inky, Clyde]

    settings = persistence.load_settings()
    speed_mul = DIFFICULTY_SPEED.get(settings.get("difficulty", "Normal"), 1.0)

    level = sm.context.get("level", 1)
    font_hud = pygame.font.Font(config.FONT_PATH, 18)

    # Frame counter for chomp animation.
    frame = 0
    pacman_open = Pacman.original_image
    pacman_closed = pygame.transform.scale(
        pacman_open, (pacman_open.get_width(), pacman_open.get_height())
    ).copy()
    pygame.draw.rect(
        pacman_closed,
        config.BLACK,
        pygame.Rect(0, pacman_closed.get_height() // 2 - 2, pacman_closed.get_width(), 4),
    )

    while sm.current == GameState.PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.transition(GameState.MENU)
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_ESCAPE:
                    sm.transition(GameState.MENU)
                    return
                if event.key == pygame.K_p:
                    sm.push(GameState.PAUSED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)

        Pacman.update(wall_list, gate)

        # Chomp animation: alternate mouth every 2 frames unless idle.
        moving = Pacman.change_x != 0 or Pacman.change_y != 0
        if moving:
            base = pacman_open if (frame // 2) % 2 == 0 else pacman_closed
            Pacman.original_image = base
        else:
            Pacman.original_image = pacman_open

        now_ms = pygame.time.get_ticks()
        for g in ghosts:
            g.update_frightened(now_ms)

        # Difficulty speed scaling: run ghost changespeed an extra tick
        # when speed_mul > 1, skip every Nth when < 1.
        should_move_ghosts = True
        if speed_mul < 1.0:
            should_move_ghosts = (frame % 5) != 0  # skip ~20% of frames on Easy
        extra_tick = speed_mul > 1.1

        def _tick_ghosts():
            nonlocal p_turn, p_steps, b_turn, b_steps, i_turn, i_steps, c_turn, c_steps
            returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
            p_turn, p_steps = returned[0], returned[1]
            Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
            Pinky.update(wall_list, False)

            returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
            b_turn, b_steps = returned[0], returned[1]
            Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
            Blinky.update(wall_list, False)

            returned = Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
            i_turn, i_steps = returned[0], returned[1]
            Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
            Inky.update(wall_list, False)

            returned = Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
            c_turn, c_steps = returned[0], returned[1]
            Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
            Clyde.update(wall_list, False)

        if should_move_ghosts:
            _tick_ghosts()
            if extra_tick and frame % 3 == 0:
                _tick_ghosts()

        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
        if blocks_hit_list:
            score += len(blocks_hit_list)
            particles.spawn_burst(Pacman.rect.centerx, Pacman.rect.centery, 4)
            audio.play("chomp")

        power_hit = pygame.sprite.spritecollide(Pacman, power_pellets, True)
        if power_hit:
            score += len(power_hit) * 5
            for g in ghosts:
                g.set_frightened(FRIGHTENED_MS, now_ms)
            particles.spawn_burst(
                Pacman.rect.centerx, Pacman.rect.centery, 12, config.WHITE
            )
            audio.play("power")

        # Pacman/ghost collision handling (frightened = eat, otherwise die).
        hit_ghosts = pygame.sprite.spritecollide(Pacman, monsta_list, False)
        if hit_ghosts:
            frightened_eaten = [g for g in hit_ghosts if getattr(g, "frightened", False)]
            killers = [g for g in hit_ghosts if not getattr(g, "frightened", False)]
            for g in frightened_eaten:
                score += 200
                g.reset_to(w, (4 * 60) + 19)
                audio.play("eat_ghost")
            if killers:
                audio.play("death")
                sm.context["score"] = score
                sm.context["level"] = 1
                sm.transition(GameState.GAME_OVER)
                return

        particles.update()

        screen.fill(config.BLACK)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)
        particles.draw(screen)

        text = config.FONT.render(
            f"Score: {score}/{bll}", True, config.RED
        )
        screen.blit(text, [10, 10])
        lvl_text = font_hud.render(
            f"Level {level}  -  {settings.get('difficulty', 'Normal')}",
            True,
            config.WHITE,
        )
        screen.blit(lvl_text, [config.SCREEN_WIDTH - lvl_text.get_width() - 10, 14])

        if score >= bll:
            sm.context["score"] = score
            sm.transition(GameState.WIN)
            return

        pygame.display.flip()
        clock.tick(10)
        frame += 1
