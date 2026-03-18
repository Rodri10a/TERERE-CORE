"""Minijuego: Machete Rush - Esquiva los machetes que caen del avion narco. 3 vidas, 20 segundos."""

import os
import pygame
import random
from minigames.base_minigame import BaseMinigame
from core.input_handler import InputHandler
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, TERERE_GREEN, RED


class FallingMachete:
    """Un machete cayendo desde el avion."""

    _image: pygame.Surface | None = None

    @classmethod
    def _load_image(cls) -> None:
        if cls._image is not None:
            return
        path = os.path.join(os.path.dirname(__file__), "..",
                            "assets", "images", "ui", "machete.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            cls._image = pygame.transform.scale(img, (35, 45))

    def __init__(self, x: float, y: float, min_speed: float = 3.0) -> None:
        FallingMachete._load_image()
        self.x: float = x + random.randint(-20, 20)
        self.y: float = y
        self.width: int = 35
        self.height: int = 45
        self.speed: float = random.uniform(min_speed, min_speed + 2.5)
        self.active: bool = True

    def update(self) -> None:
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        if FallingMachete._image:
            screen.blit(FallingMachete._image, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(screen, (180, 180, 200),
                             (int(self.x), int(self.y), self.width, self.height))


MACHETES_PER_DROP = 4


class NarcoPlane:
    """Avion narco que cruza la pantalla y tira machetes."""

    def __init__(self, image: pygame.Surface | None, direction: int = 1) -> None:
        self.image = image
        self.direction = direction
        self.width = 120
        self.height = 60
        self.speed = 4.0
        self.y = random.randint(40, 120)
        if direction == 1:
            self.x: float = -self.width
        else:
            self.x = float(SCREEN_WIDTH)
        self.active: bool = True
        self.dropped: bool = False
        self.drop_x: float = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)

    def update(self) -> None:
        self.x += self.speed * self.direction
        if self.direction == 1 and self.x > SCREEN_WIDTH + 50:
            self.active = False
        elif self.direction == -1 and self.x < -self.width - 50:
            self.active = False

    def should_drop(self) -> bool:
        if self.dropped:
            return False
        if self.direction == 1 and self.x >= self.drop_x:
            self.dropped = True
            return True
        if self.direction == -1 and self.x <= self.drop_x:
            self.dropped = True
            return True
        return False

    def get_drop_position(self) -> tuple[float, float]:
        return self.x + self.width // 2, self.y + self.height

    def draw(self, screen: pygame.Surface) -> None:
        if self.image:
            img = self.image
            if self.direction == -1:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (int(self.x), int(self.y)))
        else:
            body = pygame.Rect(int(self.x), int(self.y), self.width, self.height // 2)
            pygame.draw.ellipse(screen, (100, 100, 100), body)


class MacheteRush(BaseMinigame):
    """Esquiva los machetes que tira el avion narco. 3 vidas, 20 segundos."""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler) -> None:
        super().__init__(screen, input_handler, duration=1200)  # 20 seg
        from ui.text_renderer import TextRenderer
        self.text = TextRenderer()

        # Fondo del minijuego
        self.bg_image: pygame.Surface | None = None
        bg_path = os.path.join(os.path.dirname(__file__), "..",
                               "assets", "images", "backgrounds", "minijuego1", "mini1.png")
        if os.path.exists(bg_path):
            img = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Limites de movimiento
        self.move_left_limit: int = int(SCREEN_WIDTH * 0.18)
        self.move_right_limit: int = int(SCREEN_WIDTH * 0.82)

        # Personaje (vacabolt_2)
        self.player_image: pygame.Surface | None = None
        vaca_path = os.path.join(os.path.dirname(__file__), "..",
                                 "assets", "images", "ui", "vacabolt_2.png")
        if os.path.exists(vaca_path):
            img = pygame.image.load(vaca_path).convert_alpha()
            self.player_image = pygame.transform.scale(img, (110, 130))

        self.player_x: float = SCREEN_WIDTH // 2 - 55
        self.player_y: int = SCREEN_HEIGHT - 150
        self.player_width: int = 110
        self.player_height: int = 130
        self.player_speed: float = 7.0

        self.machetes: list[FallingMachete] = []
        self.lives: int = 3
        self.dodged: int = 0
        self.hurt_timer: int = 0

        # Avion narco
        self.plane_image: pygame.Surface | None = None
        plane_path = os.path.join(os.path.dirname(__file__), "..",
                                  "assets", "images", "ui", "hud", "avion_narco.png")
        if os.path.exists(plane_path):
            img = pygame.image.load(plane_path).convert_alpha()
            self.plane_image = pygame.transform.scale(img, (120, 60))

        self.planes: list[NarcoPlane] = []
        self.plane_spawn_timer: int = 240  # primer avion inmediato
        self.plane_spawn_interval: int = 180  # cada 3 seg
        self.next_direction: int = 1

        # Intro de 2 segundos
        self.intro_timer: int = 120
        self.showing_intro: bool = True

    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        if self.completed:
            return

        # Intro
        if self.showing_intro:
            self.intro_timer -= 1
            if self.intro_timer <= 0:
                self.showing_intro = False
            return

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        self.timer -= 1

        # Perdes si te quedas sin vidas
        if self.lives <= 0:
            self.completed = True
            self.failed = True
            self.score_earned = 0
            return

        # Sobreviviste 20 segundos = victoria
        if self.timer <= 0:
            self.completed = True
            self.score_earned = self.dodged * 30 + self.lives * 100
            return

        # Mover personaje
        if self.input_handler.is_pressed("MOVE_LEFT"):
            self.player_x -= self.player_speed
        if self.input_handler.is_pressed("MOVE_RIGHT"):
            self.player_x += self.player_speed
        self.player_x = max(self.move_left_limit,
                            min(self.move_right_limit - self.player_width, self.player_x))

        # Spawn aviones
        self.plane_spawn_timer += 1
        if self.plane_spawn_timer >= self.plane_spawn_interval:
            self.plane_spawn_timer = 0
            plane = NarcoPlane(self.plane_image, self.next_direction)
            self.planes.append(plane)
            self.next_direction *= -1

        # Actualizar aviones y soltar machetes
        for plane in self.planes:
            plane.update()
            if plane.should_drop():
                drop_x, drop_y = plane.get_drop_position()
                for i in range(MACHETES_PER_DROP):
                    cx = random.uniform(self.move_left_limit, self.move_right_limit - 35)
                    delay_y = drop_y - random.randint(0, 60)
                    self.machetes.append(FallingMachete(cx, delay_y))

        self.planes = [p for p in self.planes if p.active]

        # Colision machetes con jugador
        player_rect = pygame.Rect(int(self.player_x + 20), int(self.player_y + 20),
                                  self.player_width - 40, self.player_height - 30)
        for m in self.machetes:
            m.update()
            if m.active and m.get_rect().colliderect(player_rect) and self.hurt_timer <= 0:
                m.active = False
                self.lives -= 1
                self.hurt_timer = 40

        # Contar machetes esquivados (cayeron sin tocar)
        for m in self.machetes:
            if not m.active and m.y > SCREEN_HEIGHT - 10:
                self.dodged += 1

        self.machetes = [m for m in self.machetes if m.active]

    def draw(self) -> None:
        # Fondo
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((30, 30, 50))

        # Pantalla de intro
        if self.showing_intro:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            self.text.render_title_centered(self.screen, "MACHETE RUSH", 160, 28, YELLOW)
            self.text.render_centered(self.screen,
                                      "Esquiva los machetes del avion narco!",
                                      240, 14, WHITE)
            self.text.render_centered(self.screen,
                                      "Tenes 3 vidas, sobrevivi 20 segundos!",
                                      290, 10, (180, 180, 150))
            self.text.render_centered(self.screen,
                                      "A y D para moverse",
                                      330, 10, (180, 180, 150))
            return

        # Aviones
        for plane in self.planes:
            plane.draw(self.screen)

        # Machetes
        for m in self.machetes:
            m.draw(self.screen)

        # Personaje
        if self.player_image:
            img = self.player_image
            if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
                img = img.copy()
                img.fill((255, 100, 100, 100), special_flags=pygame.BLEND_ADD)
            self.screen.blit(img, (int(self.player_x), self.player_y))
        else:
            color = (60, 140, 60)
            if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
                color = (255, 100, 100)
            pygame.draw.rect(self.screen, color,
                             (int(self.player_x), self.player_y,
                              self.player_width, self.player_height))

        # HUD
        self.text.render_title_centered(self.screen, "MACHETE RUSH", 15, 20, YELLOW)
        self.text.render(self.screen, f"Vidas: {self.lives}", 20, 65, 10, RED)
        self.text.render(self.screen, f"Tiempo: {self.get_time_remaining():.0f}s",
                         SCREEN_WIDTH - 160, 65, 10, WHITE)

        # Corazones de vida
        for i in range(self.lives):
            hx = 120 + i * 30
            pygame.draw.polygon(self.screen, RED,
                                [(hx, 72), (hx - 8, 64), (hx - 8, 58),
                                 (hx - 4, 54), (hx, 58), (hx + 4, 54),
                                 (hx + 8, 58), (hx + 8, 64)])

        # Instrucciones
        self.text.render_centered(self.screen, "A y D para moverse",
                                  SCREEN_HEIGHT - 25, 10, (150, 150, 120))
