"""Enemigo controlado por IA - el cheto de Asunción."""

import pygame
import random
from entities.character import Character
from core.settings import SCREEN_WIDTH


class Enemy(Character):
    """El cheto antagonista con IA básica de estados: patrullar, perseguir, atacar, retroceder."""

    def __init__(self, x: float, y: float, speed: float = 3.0,
                 health: int = 100, damage: int = 10) -> None:
        super().__init__(x, y, 50, 70, color=(180, 50, 180), health=health,
                         speed=speed, damage=damage)
        self.ai_state: str = "patrol"
        self.ai_timer: int = 0
        self.patrol_direction: int = 1
        self.attack_range: float = 80.0
        self.chase_range: float = 300.0
        self.retreat_timer: int = 0
        self.target_x: float = 0.0
        self.target_y: float = 0.0
        self.is_attacking: bool = False
        self.attack_active_frames: int = 0

    def _do_patrol(self) -> None:
        """Patrulla de un lado a otro."""
        self.vel_x = self.patrol_direction * self.speed * 0.5
        self.direction = self.patrol_direction
        self.ai_timer += 1
        if self.ai_timer > 120:
            self.patrol_direction *= -1
            self.ai_timer = 0

    def _do_chase(self) -> None:
        """Persigue al jugador."""
        if self.target_x > self.x:
            self.vel_x = self.speed
            self.direction = 1
        else:
            self.vel_x = -self.speed
            self.direction = -1

    def _do_attack(self) -> None:
        """Ataca al jugador."""
        # Mirar hacia el jugador
        self.direction = 1 if self.target_x > self.x else -1

        if self.attack_cooldown <= 0 and random.random() < 0.05:
            self.is_attacking = True
            self.attack_active_frames = 10
            self.attack_cooldown = 40
            # Retroceder después de atacar
            self.retreat_timer = 30

    def _do_retreat(self) -> None:
        """Se aleja del jugador tras atacar."""
        if self.target_x > self.x:
            self.vel_x = -self.speed * 0.7
        else:
            self.vel_x = self.speed * 0.7

    def update_ai(self, player_x: float, player_y: float) -> None:
        """Actualiza la IA del enemigo basándose en la posición del jugador."""
        self.target_x = player_x
        self.target_y = player_y
        distance = abs(self.x - player_x)

        if self.hurt_timer > 0:
            self.ai_state = "hurt"
            return

        if self.retreat_timer > 0:
            self.retreat_timer -= 1
            self.ai_state = "retreat"
            return

        # Decidir estado
        if distance < self.attack_range:
            self.ai_state = "attack"
        elif distance < self.chase_range:
            self.ai_state = "chase"
        else:
            self.ai_state = "patrol"

    def update(self) -> None:
        """Actualiza al enemigo cada frame."""
        if self.ai_state == "patrol":
            self._do_patrol()
        elif self.ai_state == "chase":
            self._do_chase()
        elif self.ai_state == "attack":
            self._do_attack()
        elif self.ai_state == "retreat":
            self._do_retreat()

        if self.attack_active_frames > 0:
            self.attack_active_frames -= 1
        else:
            self.is_attacking = False

        super().update()

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja al cheto con detalles visuales."""
        super().draw(screen)

        # Lentes de sol (accesorio del cheto)
        glasses_y = int(self.y + 14)
        glasses_x = int(self.x + 8)
        pygame.draw.rect(screen, (40, 40, 40),
                         (glasses_x, glasses_y, self.width - 16, 8))
        pygame.draw.rect(screen, (20, 20, 80),
                         (glasses_x + 2, glasses_y + 1, 12, 6))
        pygame.draw.rect(screen, (20, 20, 80),
                         (glasses_x + self.width - 30, glasses_y + 1, 12, 6))

        # Cadena de oro
        chain_y = int(self.y + 30)
        pygame.draw.arc(screen, (255, 215, 0),
                        (int(self.x + 10), chain_y, 30, 15), 3.14, 6.28, 2)

        # Indicador de ataque
        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            s = pygame.Surface((attack_rect.width, attack_rect.height), pygame.SRCALPHA)
            s.fill((255, 100, 100, 100))
            screen.blit(s, (attack_rect.x, attack_rect.y))
