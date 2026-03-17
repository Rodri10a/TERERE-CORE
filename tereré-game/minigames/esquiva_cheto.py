"""Minijuego 2: Esquivar objetos lanzados por el cheto."""

import pygame
import random
from minigames.base_minigame import BaseMinigame
from core.input_handler import InputHandler
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, RED, GRAY
from ui.text_renderer import TextRenderer


class ChetoObject:
    """Objeto lanzado por el cheto que el jugador debe esquivar."""

    TYPES = [
        {"name": "celular", "color": (40, 40, 40), "w": 15, "h": 25},
        {"name": "billetera", "color": (100, 60, 30), "w": 25, "h": 15},
        {"name": "perfume", "color": (200, 100, 200), "w": 12, "h": 30},
    ]

    def __init__(self, lane: int) -> None:
        obj_type = random.choice(self.TYPES)
        self.x: float = SCREEN_WIDTH + 10
        self.y: float = 200 + lane * 120  # 3 carriles
        self.width: int = obj_type["w"]
        self.height: int = obj_type["h"]
        self.color: tuple = obj_type["color"]
        self.name: str = obj_type["name"]
        self.speed: float = random.uniform(5, 9)
        self.active: bool = True

    def update(self) -> None:
        self.x -= self.speed
        if self.x < -50:
            self.active = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.get_rect())
        pygame.draw.rect(screen, WHITE, self.get_rect(), 1)


class EsquivaCheto(BaseMinigame):
    """Esquiva objetos del cheto moviéndote entre 3 carriles. 3 vidas."""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler) -> None:
        super().__init__(screen, input_handler, duration=900)  # 15 seg
        self.text = TextRenderer()
        self.player_lane: int = 1  # 0, 1, 2
        self.player_x: int = 100
        self.player_width: int = 40
        self.player_height: int = 50
        self.lives: int = 3
        self.objects: list[ChetoObject] = []
        self.spawn_timer: int = 0
        self.dodged: int = 0
        self.hurt_timer: int = 0 

    def _get_player_y(self) -> int:
        return 185 + self.player_lane * 120

    def _get_player_rect(self) -> pygame.Rect:
        return pygame.Rect(self.player_x, self._get_player_y(),
                           self.player_width, self.player_height)

    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        if self.completed:
            return

        self.timer -= 1
        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        # Cambiar de carril con InputHandler (soporta flechas y WASD)
        if self.input_handler.was_just_pressed("UP") and self.player_lane > 0:
            self.player_lane -= 1
        if self.input_handler.was_just_pressed("DOWN") and self.player_lane < 2:
            self.player_lane += 1

        if self.lives <= 0:
            self.completed = True
            self.failed = True
            self.score_earned = 0
            return

        if self.timer <= 0:
            self.completed = True
            self.score_earned = self.dodged * 30 + self.lives * 100
            return

        # Spawn objetos
        self.spawn_timer += 1
        spawn_rate = max(20, 50 - self.timer // 100)
        if self.spawn_timer >= spawn_rate:
            lane = random.randint(0, 2)
            self.objects.append(ChetoObject(lane))
            self.spawn_timer = 0

        # Actualizar objetos
        player_rect = self._get_player_rect()
        for obj in self.objects:
            obj.update()
            if obj.active and obj.get_rect().colliderect(player_rect) and self.hurt_timer <= 0:
                obj.active = False
                self.lives -= 1
                self.hurt_timer = 30
            elif not obj.active and obj.x < 0:
                self.dodged += 1

        self.objects = [o for o in self.objects if o.active]

    def draw(self) -> None:
        self.screen.fill((50, 40, 60))

        self.text.render_title_centered(self.screen, "ESQUIVA AL CHETO", 15, 18, YELLOW)

        # Carriles
        for i in range(3):
            lane_y = 180 + i * 120
            pygame.draw.rect(self.screen, (60, 50, 70),
                             (0, lane_y, SCREEN_WIDTH, 60))
            pygame.draw.line(self.screen, (80, 70, 90),
                             (0, lane_y), (SCREEN_WIDTH, lane_y), 1)

        # Objetos
        for obj in self.objects:
            obj.draw(self.screen)

        # Jugador
        player_rect = self._get_player_rect()
        color = (60, 140, 60)
        if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
            color = (255, 100, 100)
        pygame.draw.rect(self.screen, color, player_rect)
        # Gorra
        pygame.draw.rect(self.screen, (180, 50, 50),
                         (self.player_x - 3, self._get_player_y() - 6,
                          self.player_width + 6, 8))

        # UI
        self.text.render(self.screen, f"Vidas: {self.lives}",
                         20, 65, 10, RED)
        self.text.render(self.screen, f"Tiempo: {self.get_time_remaining():.0f}s",
                         SCREEN_WIDTH - 160, 65, 10, WHITE)

        self.text.render_centered(self.screen, "Flechas y WASD para cambiar de carril",
                                  SCREEN_HEIGHT - 25, 10, GRAY)
