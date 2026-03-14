"""Proyectiles para ataques a distancia."""

import pygame
from core.settings import SCREEN_WIDTH


class Projectile:
    """Proyectil que viaja en línea recta y causa daño al impactar."""

    def __init__(self, x: float, y: float, direction: int,
                 speed: float = 8.0, damage: int = 15,
                 color: tuple = (100, 200, 255)) -> None:
        self.x: float = x
        self.y: float = y
        self.width: int = 20
        self.height: int = 10
        self.direction: int = direction
        self.speed: float = speed
        self.damage: int = damage
        self.color: tuple = color
        self.active: bool = True

    def get_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de colisión."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
