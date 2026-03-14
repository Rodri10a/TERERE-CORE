"""Sistema de detección de colisiones."""

import pygame


class CollisionSystem:
    """Maneja colisiones entre entidades: rectángulos, ataques y plataformas."""

    def check_collision(self, rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        """Verifica colisión entre dos rectángulos."""
        return rect1.colliderect(rect2)
