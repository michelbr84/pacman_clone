# player.py
import pygame

class Player(pygame.sprite.Sprite):
    """
    Representa o jogador (Pacman) do jogo.
    """
    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):
        """
        Inicializa o jogador, carregando a imagem e definindo a posição inicial.
        """
        super().__init__()
        self.image = pygame.image.load(filename).convert()
        # Armazena a imagem original para evitar perda de qualidade nas rotações
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    def prevdirection(self):
        """
        Armazena as velocidades atuais para referência futura.
        """
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def changespeed(self, x, y):
        """
        Altera a velocidade do jogador.
        """
        self.change_x += x
        self.change_y += y

    def update(self, walls, gate):
        """
        Atualiza a posição do jogador e trata colisões com as paredes e a porta.
        Após atualizar a posição, rotaciona a imagem conforme a direção.
        """
        old_x = self.rect.left
        old_y = self.rect.top

        # Atualiza a posição horizontal
        new_x = old_x + self.change_x
        self.rect.left = new_x

        # Verifica colisão horizontal com as paredes
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.left = old_x
        else:
            # Atualiza a posição vertical
            new_y = old_y + self.change_y
            self.rect.top = new_y
            # Verifica colisão vertical
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.top = old_y

        # Verifica colisão com a porta, se existir
        if gate and pygame.sprite.spritecollide(self, gate, False):
            self.rect.left = old_x
            self.rect.top = old_y

        # Atualiza a rotação da imagem conforme a direção do movimento
        # Prioriza movimento horizontal; caso não haja, usa vertical
        if self.change_x > 0:
            angle = 0
        elif self.change_x < 0:
            angle = 180
        elif self.change_y < 0:
            angle = 90
        elif self.change_y > 0:
            angle = -90
        else:
            angle = 0  # Sem movimento, mantém a rotação atual

        # Rotaciona a imagem com base no ângulo calculado
        self.image = pygame.transform.rotate(self.original_image, angle)
