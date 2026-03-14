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

    def update(self) -> None:
        """Mueve el proyectil y desactiva si sale de pantalla."""
        self.x += self.speed * self.direction
        if self.x < -self.width or self.x > SCREEN_WIDTH + self.width:
            self.active = False

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el proyectil."""
        if self.active:
            pygame.draw.ellipse(screen, self.color, self.get_rect())
            # Estela
            trail_x = self.x - self.direction * 10
            trail_rect = pygame.Rect(int(trail_x), int(self.y + 2), 10, 6)
            s = pygame.Surface((10, 6), pygame.SRCALPHA)
            s.fill((*self.color, 100))
            screen.blit(s, (trail_rect.x, trail_rect.y))
