# main.py
import pygame
from scripts.config import BLACK, WHITE, BLUE, RED, YELLOW, FONT, SCREEN_WIDTH, SCREEN_HEIGHT
from scripts.maze import setupRoomOne, setupGate
from scripts.block import Block
from scripts.player import Player
from scripts.ghost import Ghost
from scripts.directions import Pinky_directions, Blinky_directions, Inky_directions, Clyde_directions, pl, bl, il, cl

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Pacman")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

clock = pygame.time.Clock()

# Posições iniciais
w   = 303 - 16       # Posição horizontal inicial do Pacman
p_h = (7 * 60) + 19   # Altura (posição vertical) do Pacman
m_h = (4 * 60) + 19   # Altura dos fantasmas (exceto ajustes individuais)
b_h = (3 * 60) + 19   # Altura para Blinky
i_w = 303 - 16 - 32   # Posição horizontal para Inky
c_w = 303 + (32 - 16) # Posição horizontal para Clyde

def startGame():
    # Grupos de sprites
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list       = pygame.sprite.RenderPlain()
    monsta_list      = pygame.sprite.RenderPlain()
    pacman_collide   = pygame.sprite.RenderPlain()
    
    # Monta o labirinto
    wall_list = setupRoomOne(all_sprites_list)
    gate      = setupGate(all_sprites_list)

    # Variáveis de controle para as direções dos fantasmas
    p_turn, p_steps = 0, 0
    b_turn, b_steps = 0, 0
    i_turn, i_steps = 0, 0
    c_turn, c_steps = 0, 0

    # Cria o Pacman
    Pacman = Player(w, p_h, "images/pacman.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    # Cria os fantasmas
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

    # Cria a grade de blocos (pelotas)
    for row in range(19):
        for column in range(19):
            # Pula a área da porta
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            block = Block(YELLOW, 4, 4)
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26

            # Evita colocar bloco sobre as paredes ou o Pacman
            if (pygame.sprite.spritecollide(block, wall_list, False) or
                pygame.sprite.spritecollide(block, pacman_collide, False)):
                continue
            block_list.add(block)
            all_sprites_list.add(block)

    bll = len(block_list)
    score = 0
    done = False

    # Loop principal do jogo
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)

        # Atualiza a posição do Pacman e trata colisões com paredes e porta
        Pacman.update(wall_list, gate)

        # Atualiza o movimento de cada fantasma usando as listas de direções
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

        # Verifica colisão do Pacman com blocos e atualiza a pontuação
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        # Desenha tudo na tela
        screen.fill(BLACK)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = FONT.render("Score: " + str(score) + "/" + str(bll), True, RED)
        screen.blit(text, [10, 10])

        # Se o jogador coletou todos os blocos ou colidiu com um fantasma, chama a função do próximo passo
        if score == bll:
            doNext("Congratulations, you won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate)
        if pygame.sprite.spritecollide(Pacman, monsta_list, False):
            doNext("Game Over", 235, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate)

        pygame.display.flip()
        clock.tick(10)

def doNext(message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate
                    startGame()
        w_surface = pygame.Surface((400, 200))
        w_surface.set_alpha(10)
        w_surface.fill((128, 128, 128))
        screen.blit(w_surface, (100, 200))
        text1 = FONT.render(message, True, WHITE)
        screen.blit(text1, [left, 233])
        text2 = FONT.render("To play again, press ENTER.", True, WHITE)
        screen.blit(text2, [135, 303])
        text3 = FONT.render("To quit, press ESCAPE.", True, WHITE)
        screen.blit(text3, [165, 333])
        pygame.display.flip()
        clock.tick(10)

startGame()
pygame.quit()
