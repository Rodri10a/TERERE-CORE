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

    def get_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de colisión del personaje."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def get_attack_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de ataque frente al personaje."""
        attack_width = 40
        if self.direction == 1:
            return pygame.Rect(int(self.x + self.width), int(self.y + 10),
                               attack_width, self.height - 20)
        else:
            return pygame.Rect(int(self.x - attack_width), int(self.y + 10),
                               attack_width, self.height - 20)

    def take_damage(self, amount: int, knockback_dir: int = 0) -> None:
        """Recibe daño y aplica knockback."""
        if self.hurt_timer > 0:
            return
        self.health -= amount
        self.hurt_timer = 30
        self.vel_x = knockback_dir * 6
        if self.health < 0:
            self.health = 0

    def is_alive(self) -> bool:
        """Retorna True si el personaje tiene vida."""
        return self.health > 0

    def apply_gravity(self) -> None:
        """Aplica gravedad al personaje."""
        if not self.on_ground:
            self.vel_y += GRAVITY
        self.y += self.vel_y

        # Verificar suelo
        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True

    def update(self) -> None:
        """Actualiza física y timers del personaje."""
        self.apply_gravity()

        # Aplicar velocidad horizontal con fricción
        self.x += self.vel_x
        self.vel_x *= 0.85

        # Limitar a pantalla
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width

        # Timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        self.animation_timer += 1
