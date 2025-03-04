# maze.py
import pygame
from .config import BLUE, WHITE

class Wall(pygame.sprite.Sprite):
    """
    Representa uma parede do labirinto.
    """
    def __init__(self, x, y, width, height, color):
        super().__init__()
        # Cria uma superfície com as dimensões passadas e a preenche com a cor
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Define o retângulo da imagem e posiciona a parede
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

def setupRoomOne(all_sprites_list):
    """
    Cria as paredes do labirinto para a sala 1 e as adiciona à lista de sprites.
    """
    wall_list = pygame.sprite.RenderPlain()
    
    # Lista de paredes no formato [x, y, largura, altura]
    walls = [
        [0, 0, 6, 600],
        [0, 0, 600, 6],
        [0, 600, 606, 6],
        [600, 0, 6, 606],
        [300, 0, 6, 66],
        [60, 60, 186, 6],
        [360, 60, 186, 6],
        [60, 120, 66, 6],
        [60, 120, 6, 126],
        [180, 120, 246, 6],
        [300, 120, 6, 66],
        [480, 120, 66, 6],
        [540, 120, 6, 126],
        [120, 180, 126, 6],
        [120, 180, 6, 126],
        [360, 180, 126, 6],
        [480, 180, 6, 126],
        [180, 240, 6, 126],
        [180, 360, 246, 6],
        [420, 240, 6, 126],
        [240, 240, 42, 6],
        [324, 240, 42, 6],
        [240, 240, 6, 66],
        [240, 300, 126, 6],
        [360, 240, 6, 66],
        [0, 300, 66, 6],
        [540, 300, 66, 6],
        [60, 360, 66, 6],
        [60, 360, 6, 186],
        [480, 360, 66, 6],
        [540, 360, 6, 186],
        [120, 420, 366, 6],
        [120, 420, 6, 66],
        [480, 420, 6, 66],
        [180, 480, 246, 6],
        [300, 480, 6, 66],
        [120, 540, 126, 6],
        [360, 540, 126, 6]
    ]
    
    # Cria cada parede e as adiciona tanto à lista de paredes quanto à lista geral de sprites
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], BLUE)
        wall_list.add(wall)
        all_sprites_list.add(wall)
    
    return wall_list

def setupGate(all_sprites_list):
    """
    Cria a porta do labirinto e a adiciona à lista de sprites.
    """
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, WHITE))
    all_sprites_list.add(gate)
    return gate
