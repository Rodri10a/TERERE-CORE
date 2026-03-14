"""Clase base para todos los personajes del juego."""

import pygame
from core.settings import GRAVITY, GROUND_Y, SCREEN_WIDTH


class Character:
    """Clase base con física, vida, animación y dibujo para personajes."""

    def __init__(self, x: float, y: float, width: int, height: int,
                 color: tuple, health: int = 100, speed: float = 5.0,
                 damage: int = 10) -> None:
        self.x: float = x
        self.y: float = y
        self.width: int = width
        self.height: int = height
        self.color: tuple = color
        self.health: int = health
        self.max_health: int = health
        self.speed: float = speed
        self.damage: int = damage
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.direction: int = 1  # 1 = derecha, -1 = izquierda
        self.on_ground: bool = True
        self.state: str = "idle"
        self.attack_cooldown: int = 0
        self.hurt_timer: int = 0
        self.attack_frame: int = 0
        self.animation_timer: int = 0
