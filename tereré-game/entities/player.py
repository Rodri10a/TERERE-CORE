"""Personaje controlado por el jugador - el capiateño."""

import os
import pygame
from entities.character import Character
from core.input_handler import InputHandler
from core.settings import JUMP_FORCE, PLAYER_SPEED, ATTACK_COOLDOWN, SPECIAL_COOLDOWN, COMBO_WINDOW


def _remove_bg(img: pygame.Surface) -> pygame.Surface:
    """Quita fondo blanco/gris claro de una imagen."""
    w, h = img.get_size()
    clean = pygame.Surface((w, h), pygame.SRCALPHA)
    for px in range(w):
        for py in range(h):
            pixel = img.get_at((px, py))
            r, g, b = pixel[0], pixel[1], pixel[2]
            a = pixel[3] if len(pixel) > 3 else 255
            if a < 30 or (r > 230 and g > 230 and b > 230):
                continue
            clean.set_at((px, py), (r, g, b, 255))
    return clean


class Player(Character):
    """El capiateño protagonista, controlado por teclado con combos de ataque."""

    def __init__(self, x: float, y: float, input_handler: InputHandler,
                 character_file: str = "capiateno") -> None:
        super().__init__(x, y, 150, 250, color=(60, 140, 60), health=100,
                         speed=PLAYER_SPEED, damage=15)
        self.input_handler = input_handler

        # Animacion
        self.idle_frames: list[pygame.Surface] = []
        self.idle_frames_flipped: list[pygame.Surface] = []
        self.walk_frames: list[pygame.Surface] = []
        self.walk_frames_flipped: list[pygame.Surface] = []
        self.attack_frames: list[pygame.Surface] = []
        self.attack_frames_flipped: list[pygame.Surface] = []
        self.current_frame: int = 0
        self.frame_speed: int = 10
        self.frame_counter: int = 0
        self.sprite: pygame.Surface | None = None
        self.sprite_flipped: pygame.Surface | None = None
        self.has_animation: bool = False
        self.prev_anim_state: str = ""
        self.damage_cooldown_max = 40
        self.damage_cooldown = 0

        self._load_sprites(character_file)

        self.combo_count: int = 0
        self.combo_timer: int = 0
        self.special_cooldown: int = 0
        self.is_attacking: bool = False
        self.is_blocking: bool = False
        self.attack_active_frames: int = 0

    def _load_sprites(self, character_file: str) -> None:
        """Carga sprites animados (carpeta con frames) o estatico (archivo)."""
        base = os.path.join(os.path.dirname(__file__), "..",
                            "assets", "images", "characters")

        # Intentar cargar como carpeta con frames
        frames_dir = os.path.join(base, character_file)
        if os.path.isdir(frames_dir):
            # Buscar frames en raiz o en subcarpeta "pegar"
            pegar_dir = os.path.join(frames_dir, "pegar")
            if os.path.isdir(pegar_dir):
                search_dir = pegar_dir
            else:
                search_dir = frames_dir

            frame_files = sorted([f for f in os.listdir(search_dir)
                                   if f.startswith("frame") and f.endswith(".png")])
            for ff in frame_files:
                path = os.path.join(search_dir, ff)
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                # Todos los frames de pegar/ son de ataque
                self.attack_frames.append(img)
                self.attack_frames_flipped.append(pygame.transform.flip(img, True, False))

            # Cargar frames de caminata desde subcarpeta "caminata"
            try:
                walk_dir = os.path.join(frames_dir, "caminata")
                if os.path.isdir(walk_dir):
                    walk_files = sorted([f for f in os.listdir(walk_dir)
                                          if f.endswith(".png") and f[0].isdigit()])
                    for wf in walk_files:
                        path = os.path.join(walk_dir, wf)
                        img = pygame.image.load(path).convert_alpha()
                        img = pygame.transform.scale(img, (self.width, self.height))
                        self.walk_frames.append(img)
                        self.walk_frames_flipped.append(pygame.transform.flip(img, True, False))
            except Exception:
                self.walk_frames.clear()
                self.walk_frames_flipped.clear()

            # Idle = primer frame de caminata (pose quieto)
            if self.walk_frames:
                self.idle_frames.append(self.walk_frames[0])
                self.idle_frames_flipped.append(self.walk_frames_flipped[0])

            if self.idle_frames or self.attack_frames:
                self.has_animation = True
                if self.idle_frames:
                    self.sprite = self.idle_frames[0]
                    self.sprite_flipped = self.idle_frames_flipped[0]
                else:
                    self.sprite = self.attack_frames[0]
                    self.sprite_flipped = self.attack_frames_flipped[0]

            return

        # Sprite estatico (archivo individual)
        sprite_path = os.path.join(base, character_file)
        if os.path.exists(sprite_path):
            img = pygame.image.load(sprite_path).convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            self.sprite = _remove_bg(img)
            self.sprite_flipped = pygame.transform.flip(self.sprite, True, False)

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

        # Ataque normal 
        if (
            self.input_handler.was_just_pressed("ATTACK")
            and self.attack_cooldown <= 0
            and not self.is_attacking
        ):
            self.attack()

        # Ataque especial
        if self.input_handler.was_just_pressed("SPECIAL") and self.special_cooldown <= 0:
            self.special_attack()

    def attack(self) -> None:
        """Ejecuta un ataque normal con sistema de combo."""
        self.is_attacking = True
        self.attack_active_frames = 12
        self.attack_cooldown = ATTACK_COOLDOWN
        self.state = "attacking"

        if self.combo_timer > 0 and self.combo_count < 2:
            self.combo_count += 1
            self.attack_cooldown = ATTACK_COOLDOWN
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
            return self.damage * 3
        if self.combo_count >= 2:
            return int(self.damage * 1.5)
        return self.damage

    def update(self) -> None:
        """Actualiza al jugador cada frame."""
        self.handle_input()
        super().update()

        # Animacion de frames
        if self.has_animation:
            # Detectar cambio de estado de animacion para resetear frame
            if self.is_attacking:
                anim_state = "attacking"
            elif self.state == "running" and self.walk_frames:
                anim_state = "walking"
            else:
                anim_state = "idle"

            if anim_state != self.prev_anim_state:
                self.current_frame = 0
                self.frame_counter = 0
                self.prev_anim_state = anim_state
                # Asignar sprite correcto inmediatamente
                if anim_state == "attacking" and self.attack_frames:
                    self.sprite = self.attack_frames[0]
                    self.sprite_flipped = self.attack_frames_flipped[0]
                elif anim_state == "walking" and self.walk_frames:
                    self.sprite = self.walk_frames[0]
                    self.sprite_flipped = self.walk_frames_flipped[0]
                elif self.idle_frames:
                    self.sprite = self.idle_frames[0]
                    self.sprite_flipped = self.idle_frames_flipped[0]

            self.frame_counter += 1
            if self.is_attacking and self.attack_frames:
                # Ciclar frames de ataque rapido
                if self.frame_counter >= 5:
                    self.frame_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
                    self.sprite = self.attack_frames[self.current_frame]
                    self.sprite_flipped = self.attack_frames_flipped[self.current_frame]
            elif self.state == "running" and self.walk_frames:
                # Ciclar frames de caminata
                if self.frame_counter >= 6:
                    self.frame_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                    self.sprite = self.walk_frames[self.current_frame]
                    self.sprite_flipped = self.walk_frames_flipped[self.current_frame]
            elif self.idle_frames:
                # Ciclar frames idle
                if self.frame_counter >= self.frame_speed:
                    self.frame_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                    self.sprite = self.idle_frames[self.current_frame]
                    self.sprite_flipped = self.idle_frames_flipped[self.current_frame]

        # Timers de combate
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0

        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.attack_active_frames > 0:
            self.attack_active_frames -= 1
        else:
            self.is_attacking = False
            if self.state == "attacking":
                self.state = "idle"
        
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.on_ground and self.state == "jumping":
            self.state = "idle"

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja al capiateño con sprite o fallback a rectángulo."""
        if self.sprite:
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

            bar_width = self.width
            bar_y = int(self.y - 10)
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (60, 60, 60), (int(self.x), bar_y, bar_width, 5))
            bar_color = (50, 200, 50) if health_ratio > 0.5 else (200, 200, 0) if health_ratio > 0.25 else (200, 50, 50)
            pygame.draw.rect(screen, bar_color, (int(self.x), bar_y, int(bar_width * health_ratio), 5))
        else:
            super().draw(screen)

        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            s = pygame.Surface((attack_rect.width, attack_rect.height), pygame.SRCALPHA)
            if self.special_cooldown >= SPECIAL_COOLDOWN - 10:
                s.fill((100, 200, 255, 120))
            else:
                s.fill((255, 255, 100, 100))
            screen.blit(s, (attack_rect.x, attack_rect.y))

        if self.special_cooldown <= 0:
            indicator_x = int(self.x + self.width // 2)
            indicator_y = int(self.y - 18)
            pygame.draw.circle(screen, (100, 200, 255), (indicator_x, indicator_y), 4)
