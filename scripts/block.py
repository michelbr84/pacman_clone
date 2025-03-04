# block.py
import pygame
from .config import WHITE

class Block(pygame.sprite.Sprite):
    """
    Representa um bloco (pelota) do jogo.
    Este bloco é desenhado como uma elipse com a cor especificada.
    """
    def __init__(self, color, width, height):
        # Inicializa o Sprite pai
        super().__init__()

        # Cria uma superfície com as dimensões passadas
        self.image = pygame.Surface([width, height])
        # Preenche a superfície com a cor branca para posteriormente definir a colorkey
        self.image.fill(WHITE)
        # Define a cor branca como transparente
        self.image.set_colorkey(WHITE)
        # Desenha uma elipse com a cor desejada na superfície
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        
        # Obtém o retângulo que delimita a superfície
        self.rect = self.image.get_rect()
