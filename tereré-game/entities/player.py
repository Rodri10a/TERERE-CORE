"""Personaje controlado por el jugador - el capiateño."""

import pygame
from entities.character import Character
from core.input_handler import InputHandler
from core.settings import JUMP_FORCE, PLAYER_SPEED, ATTACK_COOLDOWN, SPECIAL_COOLDOWN, COMBO_WINDOW


class Player(Character):
    """El capiateño protagonista, controlado por teclado con combos de ataque."""

    def __init__(self, x: float, y: float, input_handler: InputHandler) -> None:
        super().__init__(x, y, 50, 70, color=(60, 140, 60), health=100,
                         speed=PLAYER_SPEED, damage=10)
        self.input_handler = input_handler
        self.combo_count: int = 0
        self.combo_timer: int = 0
        self.special_cooldown: int = 0
        self.is_attacking: bool = False
        self.is_blocking: bool = False
        self.attack_active_frames: int = 0

    def handle_input(self) -> None:
        """Procesa el input del jugador."""
        if self.hurt_timer > 0:
            return

        # Movimiento
        if self.input_handler.is_pressed("MOVE_LEFT"):
            self.vel_x = -self.speed
            self.direction = -1
            if self.state not in ("attacking", "jumping"):
                self.state = "running"
        elif self.input_handler.is_pressed("MOVE_RIGHT"):
            self.vel_x = self.speed
            self.direction = 1
            if self.state not in ("attacking", "jumping"):
                self.state = "running"
        else:
            if self.state == "running":
                self.state = "idle"

        # Saltar
        if self.input_handler.was_just_pressed("JUMP") and self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False
            self.state = "jumping"

        # Ataque normal (combo de 2 golpes)
        if self.input_handler.was_just_pressed("ATTACK") and self.attack_cooldown <= 0:
            self.attack()

        # Ataque especial
        if self.input_handler.was_just_pressed("SPECIAL") and self.special_cooldown <= 0:
            self.special_attack()
