"""The PLAYING state — the original game loop, extracted verbatim from main.py.

Load-bearing quirks preserved per CLAUDE.md:
- 10 FPS clock tick (ghost direction lists and 30px movement deltas depend on it).
- Each ghost has `.changespeed(...)` called twice per frame; the second call is dead
  code but affects internal (turn, steps) state progression — do not remove.
- Pinky/Blinky/Inky/Clyde direction lists and `pl/bl/il/cl` max-turn values are fixed
  scripted AI, not pathfinding.
"""
import pygame

from scripts import config
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
from scripts.player import Player

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

    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            block = Block(config.YELLOW, 4, 4)
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26
            if pygame.sprite.spritecollide(
                block, wall_list, False
            ) or pygame.sprite.spritecollide(block, pacman_collide, False):
                continue
            block_list.add(block)
            all_sprites_list.add(block)

    bll = len(block_list)
    score = 0

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

        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        screen.fill(config.BLACK)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = config.FONT.render(
            "Score: " + str(score) + "/" + str(bll), True, config.RED
        )
        screen.blit(text, [10, 10])

        if score == bll:
            sm.context["score"] = score
            sm.transition(GameState.WIN)
            return
        if pygame.sprite.spritecollide(Pacman, monsta_list, False):
            sm.context["score"] = score
            sm.transition(GameState.GAME_OVER)
            return

        pygame.display.flip()
        clock.tick(10)
