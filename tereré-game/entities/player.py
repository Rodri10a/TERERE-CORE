"""Personaje controlado por el jugador - el capiateño."""

import os
import pygame
from entities.character import Character
from core.input_handler import InputHandler
from core.settings import JUMP_FORCE, PLAYER_SPEED, ATTACK_COOLDOWN, SPECIAL_COOLDOWN, COMBO_WINDOW


class Player(Character):
    """El capiateño protagonista, controlado por teclado con combos de ataque."""

    def __init__(self, x: float, y: float, input_handler: InputHandler,
                 character_file: str = "personaje_principal.jpg") -> None:
        super().__init__(x, y, 150, 250, color=(60, 140, 60), health=100,
                         speed=PLAYER_SPEED, damage=15)
        self.input_handler = input_handler

        # Cargar sprite del personaje seleccionado
        self.sprite: pygame.Surface | None = None
        self.sprite_flipped: pygame.Surface | None = None
        sprite_path = os.path.join(os.path.dirname(__file__), "..",
                                   "assets", "images", "characters",
                                   character_file)
        if os.path.exists(sprite_path):
            img = pygame.image.load(sprite_path).convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            # Quitar fondo blanco/gris claro
            clean = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            for px in range(img.get_width()):
                for py in range(img.get_height()):
                    pixel = img.get_at((px, py))
                    r, g, b, a = pixel[0], pixel[1], pixel[2], pixel[3] if len(pixel) > 3 else 255
                    if a < 30 or (r > 230 and g > 230 and b > 230):
                        continue
                    clean.set_at((px, py), (r, g, b, 255))
            self.sprite = clean
            self.sprite_flipped = pygame.transform.flip(self.sprite, True, False)
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

    def attack(self) -> None:
        """Ejecuta un ataque normal con sistema de combo."""
        self.is_attacking = True
        self.attack_active_frames = 8
        self.state = "attacking"

        if self.combo_timer > 0 and self.combo_count < 2:
            self.combo_count += 1
            self.attack_cooldown = ATTACK_COOLDOWN // 2
        else:
            self.combo_count = 1
            self.attack_cooldown = ATTACK_COOLDOWN

        self.combo_timer = COMBO_WINDOW

    def special_attack(self) -> None:
        """Ejecuta un ataque especial (tereré splash) con más daño y cooldown."""
        self.is_attacking = True
        self.attack_active_frames = 12
        self.state = "attacking"
        self.special_cooldown = SPECIAL_COOLDOWN
        self.combo_count = 0

    def get_current_damage(self) -> int:
        """Retorna el daño del ataque actual."""
        if self.special_cooldown >= SPECIAL_COOLDOWN - 5:
            return self.damage * 3  # Especial hace triple daño
        if self.combo_count >= 2:
            return int(self.damage * 1.5)  # Segundo golpe de combo
        return self.damage

    def update(self) -> None:
        """Actualiza al jugador cada frame."""
        self.handle_input()
        super().update()

        # Timers de combate
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0

        if self.special_cooldown > 0:
            self.special_cooldown -= 1

        if self.attack_active_frames > 0:
            self.attack_active_frames -= 1
        else:
            self.is_attacking = False
            if self.state == "attacking":
                self.state = "idle"

        if self.on_ground and self.state == "jumping":
            self.state = "idle"

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja al capiateño con sprite o fallback a rectángulo."""
        if self.sprite:
            # Parpadeo blanco al recibir daño
            if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
                flash = self.sprite.copy()
                flash.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
                if self.direction == -1:
                    flash = pygame.transform.flip(flash, True, False)
                screen.blit(flash, (int(self.x), int(self.y)))
            else:
                if self.direction == -1:
                    screen.blit(self.sprite_flipped, (int(self.x), int(self.y)))
                else:
                    screen.blit(self.sprite, (int(self.x), int(self.y)))

            # Barra de vida sobre el personaje
            bar_width = self.width
            bar_y = int(self.y - 10)
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (60, 60, 60), (int(self.x), bar_y, bar_width, 5))
            bar_color = (50, 200, 50) if health_ratio > 0.5 else (200, 200, 0) if health_ratio > 0.25 else (200, 50, 50)
            pygame.draw.rect(screen, bar_color, (int(self.x), bar_y, int(bar_width * health_ratio), 5))
        else:
            super().draw(screen)

        # Indicador de ataque
        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            s = pygame.Surface((attack_rect.width, attack_rect.height), pygame.SRCALPHA)
            if self.special_cooldown >= SPECIAL_COOLDOWN - 10:
                s.fill((100, 200, 255, 120))
            else:
                s.fill((255, 255, 100, 100))
            screen.blit(s, (attack_rect.x, attack_rect.y))

        # Indicador de especial listo
        if self.special_cooldown <= 0:
            indicator_x = int(self.x + self.width // 2)
            indicator_y = int(self.y - 18)
            pygame.draw.circle(screen, (100, 200, 255), (indicator_x, indicator_y), 4)
