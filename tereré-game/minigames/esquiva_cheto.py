"""Minijuego 2: Esquivar baches en San Lorenzo."""

import os
import pygame
import random
from minigames.base_minigame import BaseMinigame
from core.input_handler import InputHandler
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, RED, GRAY
from ui.text_renderer import TextRenderer


class Bache:
    """Bache que el jugador debe esquivar."""

    _image: pygame.Surface | None = None
    _loaded: bool = False

    @classmethod
    def _load_image(cls) -> None:
        if cls._loaded:
            return
        cls._loaded = True
        path = os.path.join(os.path.dirname(__file__), "..",
                            "assets", "images", "ui", "hud", "bache.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            cls._image = pygame.transform.scale(img, (60, 50))

    def __init__(self, lane: int) -> None:
        Bache._load_image()
        self.x: float = SCREEN_WIDTH + 10
        self.y: float = 150 + lane * 170
        self.width: int = 60
        self.height: int = 50
        self.speed: float = random.uniform(5, 9)
        self.active: bool = True

    def update(self) -> None:
        self.x -= self.speed
        if self.x < -70:
            self.active = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        if Bache._image:
            screen.blit(Bache._image, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(screen, (80, 50, 20), self.get_rect())
            pygame.draw.rect(screen, WHITE, self.get_rect(), 1)


class AutoRojo:
    """Auto rojo que el jugador debe esquivar."""

    _image: pygame.Surface | None = None
    _loaded: bool = False

    @classmethod
    def _load_image(cls) -> None:
        if cls._loaded:
            return
        cls._loaded = True
        path = os.path.join(os.path.dirname(__file__), "..",
                            "assets", "images", "ui", "auto_1.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            cls._image = pygame.transform.scale(img, (100, 70))

    def __init__(self, lane: int) -> None:
        AutoRojo._load_image()
        self.x: float = SCREEN_WIDTH + 10
        self.y: float = 150 + lane * 170
        self.width: int = 100
        self.height: int = 70
        self.speed: float = random.uniform(6, 11)
        self.active: bool = True

    def update(self) -> None:
        self.x -= self.speed
        if self.x < -110:
            self.active = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        if AutoRojo._image:
            screen.blit(AutoRojo._image, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(screen, (200, 30, 30), self.get_rect())
            pygame.draw.rect(screen, WHITE, self.get_rect(), 1)


class EsquivaCheto(BaseMinigame):
    """Esquiva baches moviéndote entre 3 carriles. 3 vidas."""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler) -> None:
        super().__init__(screen, input_handler, duration=900)  # 15 seg
        self.text = TextRenderer()

        # Imagen de fondo (asfaltado)
        self.bg_image: pygame.Surface | None = None
        bg_path = os.path.join(os.path.dirname(__file__), "..",
                               "assets", "images", "backgrounds",
                               "Imagen_asfaltado_minijuego.png")
        if os.path.exists(bg_path):
            img = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Imagen del jugador (vacabolt)
        self.player_image: pygame.Surface | None = None
        vaca_path = os.path.join(os.path.dirname(__file__), "..",
                                 "assets", "images", "ui", "vacabolt.png")
        if os.path.exists(vaca_path):
            img = pygame.image.load(vaca_path).convert_alpha()
            self.player_image = pygame.transform.scale(img, (120, 150))

        self.player_lane: int = 1  # 0, 1, 2
        self.player_x: int = 100
        self.player_width: int = 120
        self.player_height: int = 150
        self.lives: int = 3
        self.objects: list[Bache | AutoRojo] = []
        self.spawn_timer: int = 0
        self.dodged: int = 0
        self.hurt_timer: int = 0

        # Sonido de "y volo"
        self.volo_sound: pygame.mixer.Sound | None = None
        volo_path = os.path.join(os.path.dirname(__file__), "..",
                                 "assets", "sounds", "music", "Y_volo.wav")
        if os.path.exists(volo_path):
            self.volo_sound = pygame.mixer.Sound(volo_path)

    def _get_player_y(self) -> int:
        return 140 + self.player_lane * 170

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

        # Spawn baches
        self.spawn_timer += 1
        spawn_rate = max(20, 50 - self.timer // 100)
        if self.spawn_timer >= spawn_rate:
            lane = random.randint(0, 2)
            if random.random() < 0.4:
                self.objects.append(AutoRojo(lane))
            else:
                self.objects.append(Bache(lane))
            self.spawn_timer = 0

        # Actualizar baches
        player_rect = self._get_player_rect()
        for obj in self.objects:
            obj.update()
            if obj.active and obj.get_rect().colliderect(player_rect) and self.hurt_timer <= 0:
                obj.active = False
                self.lives -= 1
                self.hurt_timer = 30
                if self.volo_sound:
                    self.volo_sound.play()
            elif not obj.active and obj.x < 0:
                self.dodged += 1

        self.objects = [o for o in self.objects if o.active]

    def draw(self) -> None:
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((50, 40, 60))

        self.text.render_title_centered(self.screen, "ESQUIVA LOS BACHES", 15, 18, YELLOW)

        # Baches
        for obj in self.objects:
            obj.draw(self.screen)

        # Jugador
        if self.player_image:
            img = self.player_image
            if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
                img = img.copy()
                img.fill((255, 100, 100, 100), special_flags=pygame.BLEND_ADD)
            self.screen.blit(img, (self.player_x, self._get_player_y()))
        else:
            player_rect = self._get_player_rect()
            color = (60, 140, 60)
            if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
                color = (255, 100, 100)
            pygame.draw.rect(self.screen, color, player_rect)

        # UI
        self.text.render(self.screen, f"Vidas: {self.lives}",
                         20, 65, 10, RED)
        self.text.render(self.screen, f"Tiempo: {self.get_time_remaining():.0f}s",
                         SCREEN_WIDTH - 160, 65, 10, WHITE)

        self.text.render_centered(self.screen, "Flechas y WASD para cambiar de carril",
                                  SCREEN_HEIGHT - 25, 10, GRAY)
