"""Tiny particle system — spawns short-lived coloured rectangles."""
import random

import pygame

from scripts import config


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "color", "size")

    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-2.0, 2.0)
        self.life = 8
        self.color = color or config.YELLOW
        self.size = 3

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def alive(self):
        return self.life > 0

    def draw(self, screen):
        alpha = max(0, min(255, self.life * 32))
        c = (self.color[0], self.color[1], self.color[2])
        pygame.draw.rect(
            screen, c, pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        )
        _ = alpha  # reserved for per-surface blending if needed


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn_burst(self, x, y, n=6, color=None):
        for _ in range(n):
            self.particles.append(Particle(x, y, color))

    def update(self):
        self.particles = [p for p in self.particles if p.alive()]
        for p in self.particles:
            p.update()

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
