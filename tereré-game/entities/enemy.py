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
