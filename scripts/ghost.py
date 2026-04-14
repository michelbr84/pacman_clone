# ghost.py
import pygame
from .player import Player

class Ghost(Player):
    """
    Representa um fantasma no jogo, herdando as propriedades e métodos de Player.
    Implementa a lógica de movimentação baseada em uma lista de direções.
    """

    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)
        self.frightened = False
        self.frightened_until = 0  # pygame ticks ms

    def set_frightened(self, duration_ms, now_ms):
        self.frightened = True
        self.frightened_until = now_ms + duration_ms
        # Tint blue.
        tinted = self.original_image.copy()
        tinted.fill((0, 0, 180), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = tinted

    def update_frightened(self, now_ms):
        if self.frightened and now_ms >= self.frightened_until:
            self.frightened = False
            self.image = self.original_image

    def reset_to(self, x, y):
        self.rect.left = x
        self.rect.top = y
        self.frightened = False
        self.image = self.original_image

    def changespeed(self, direction_list, ghost, turn, steps, max_turn):
        """
        Atualiza a velocidade do fantasma com base na direção atual da lista.

        :param direction_list: Lista de direções, onde cada item tem o formato [dx, dy, quantidade_de_passos]
        :param ghost: Nome do fantasma (ex.: "clyde") para lógica específica
        :param turn: Índice atual na lista de direções
        :param steps: Número de passos já dados na direção atual
        :param max_turn: Valor máximo para o índice (geralmente len(direction_list)-1)
        :return: Lista contendo [novo_turn, novos_steps]
        """
        try:
            required_steps = direction_list[turn][2]
            if steps < required_steps:
                self.change_x = direction_list[turn][0]
                self.change_y = direction_list[turn][1]
                steps += 1
            else:
                if turn < max_turn:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = direction_list[turn][0]
                self.change_y = direction_list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]
