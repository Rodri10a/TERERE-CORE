"""Enemigo controlado por IA - el cheto de Asunción."""

import os
import pygame
import random
from entities.character import Character
from core.settings import SCREEN_WIDTH


class Enemy(Character):
    """El cheto antagonista con IA básica de estados: patrullar, perseguir, atacar, retroceder."""

    def __init__(self, x: float, y: float, speed: float = 3.0,
                 health: int = 130, damage: int = 10,
                 sprite_folder: str = "Luqueño") -> None:
        super().__init__(x, y, 150, 250, color=(180, 50, 180), health=health,
                         speed=speed, damage=damage)

        # Cargar sprites
        self.idle_frames: list[pygame.Surface] = []
        self.idle_frames_flipped: list[pygame.Surface] = []
        self.sprite: pygame.Surface | None = None
        self.sprite_flipped: pygame.Surface | None = None
        self.current_frame: int = 0
        self.anim_speed: int = 8
        self.anim_counter: int = 0
        self._load_sprites(sprite_folder)

        self.ai_state: str = "patrol"
        self.ai_timer: int = 0
        self.patrol_direction: int = 1
        self.attack_range: float = 120.0
        self.chase_range: float = 500.0
        self.retreat_timer: int = 0
        self.target_x: float = 0.0
        self.target_y: float = 0.0
        self.is_attacking: bool = False
        self.attack_active_frames: int = 0

    def _load_sprites(self, sprite_folder: str) -> None:
        """Carga los frames idle desde la carpeta del enemigo."""
        base = os.path.join(os.path.dirname(__file__), "..",
                            "assets", "images", "characters", "capiateno", sprite_folder)
        if not os.path.isdir(base):
            return
        files = sorted(f for f in os.listdir(base) if f.endswith(".png"))
        for f in files:
            img = pygame.image.load(os.path.join(base, f)).convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            self.idle_frames.append(img)
            self.idle_frames_flipped.append(pygame.transform.flip(img, True, False))
        if self.idle_frames:
            self.sprite = self.idle_frames[0]
            self.sprite_flipped = self.idle_frames_flipped[0]

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
        """Dibuja al enemigo con sprite o fallback a rectángulo."""
        if self.idle_frames:
            # Animación
            self.anim_counter += 1
            if self.anim_counter >= self.anim_speed:
                self.anim_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.sprite = self.idle_frames[self.current_frame]
                self.sprite_flipped = self.idle_frames_flipped[self.current_frame]

            # Flash blanco al recibir daño
            if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
                frame = self.sprite if self.direction == 1 else self.sprite_flipped
                white = frame.copy()
                white.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
                screen.blit(white, (int(self.x), int(self.y)))
            else:
                if self.direction == 1:
                    screen.blit(self.sprite, (int(self.x), int(self.y)))
                else:
                    screen.blit(self.sprite_flipped, (int(self.x), int(self.y)))

            # Barra de vida
            bar_width = self.width
            bar_y = int(self.y - 10)
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (60, 60, 60), (int(self.x), bar_y, bar_width, 5))
            bar_color = (50, 200, 50) if health_ratio > 0.5 else (200, 200, 0) if health_ratio > 0.25 else (200, 50, 50)
            pygame.draw.rect(screen, bar_color, (int(self.x), bar_y, int(bar_width * health_ratio), 5))
        else:
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
