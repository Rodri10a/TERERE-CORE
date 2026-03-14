"""Sistema de detección de colisiones."""

import pygame


class CollisionSystem:
    """Maneja colisiones entre entidades: rectángulos, ataques y plataformas."""

    def check_collision(self, rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        """Verifica colisión entre dos rectángulos."""
        return rect1.colliderect(rect2)

    def check_attack_hit(self, attacker, defender) -> bool:
        """Verifica si el ataque de un personaje golpea a otro."""
        if defender.hurt_timer > 0:
            return False
        attack_rect = attacker.get_attack_rect()
        defender_rect = defender.get_rect()
        return attack_rect.colliderect(defender_rect)
