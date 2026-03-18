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

    def check_ground_collision(self, character, platforms: list[dict]) -> bool:
        """Verifica si un personaje está sobre una plataforma."""
        char_rect = character.get_rect()
        foot_rect = pygame.Rect(char_rect.x + 5, char_rect.bottom - 2,
                                char_rect.width - 10, 4)
        for plat in platforms:
            plat_rect = pygame.Rect(plat["x"], plat["y"], plat["width"], plat["height"])
            if foot_rect.colliderect(plat_rect) and character.vel_y >= 0:
                character.y = plat["y"] - character.height
                character.vel_y = 0
                character.on_ground = True
                return True
        return False
