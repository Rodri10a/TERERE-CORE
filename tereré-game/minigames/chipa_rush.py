"""Minijuego: Chipa Rush - Un avion narco pasa y tira chipas, recolecta 15 para pasar."""

import os
import pygame
import random
from minigames.base_minigame import BaseMinigame
from core.input_handler import InputHandler
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, TERERE_GREEN, RED


class FallingChipa:
    """Una chipa cayendo desde el avion."""

    _image: pygame.Surface | None = None

    @classmethod
    def _load_image(cls) -> None:
        if cls._image is not None:
            return
        path = os.path.join(os.path.dirname(__file__), "..",
                            "assets", "images", "ui", "hud", "chipa.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            cls._image = pygame.transform.scale(img, (40, 40))

    def __init__(self, x: float, y: float, min_speed: float = 2.5) -> None:
        FallingChipa._load_image()
        self.x: float = x + random.randint(-20, 20)
        self.y: float = y
        self.width: int = 40
        self.height: int = 40
        self.speed: float = random.uniform(min_speed, min_speed + 2.0)
        self.active: bool = True
        self.caught: bool = False

    def update(self) -> None:
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        if FallingChipa._image:
            screen.blit(FallingChipa._image, (int(self.x), int(self.y)))
        else:
            pygame.draw.ellipse(screen, (220, 180, 80),
                                (int(self.x), int(self.y), self.width, self.height))


CHIPAS_NEEDED = 15
CHIPAS_PER_DROP = 5


class NarcoPlane:
    """Avion narco que cruza la pantalla y tira chipas."""

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
        # Salio de pantalla
        if self.direction == 1 and self.x > SCREEN_WIDTH + 50:
            self.active = False
        elif self.direction == -1 and self.x < -self.width - 50:
            self.active = False

    def should_drop(self) -> bool:
        """Retorna True una sola vez cuando el avion pasa por la zona de drop."""
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
        """Posicion desde donde caen las chipas."""
        return self.x + self.width // 2, self.y + self.height

    def draw(self, screen: pygame.Surface) -> None:
        if self.image:
            img = self.image
            if self.direction == -1:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (int(self.x), int(self.y)))
        else:
            # Fallback si no hay imagen
            body = pygame.Rect(int(self.x), int(self.y), self.width, self.height // 2)
            pygame.draw.ellipse(screen, (100, 100, 100), body)
            wing = pygame.Rect(int(self.x + 20), int(self.y - 10), self.width - 40, self.height)
            pygame.draw.ellipse(screen, (80, 80, 80), wing)


class ChipaRush(BaseMinigame):
    """Un avion narco pasa y tira chipas. Recolecta 15 para pasar!"""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler) -> None:
        super().__init__(screen, input_handler, duration=2400)  # 40 seg
        from ui.text_renderer import TextRenderer
        self.text = TextRenderer()

        # Fondo del minijuego
        self.bg_image: pygame.Surface | None = None
        bg_path = os.path.join(os.path.dirname(__file__), "..",
                               "assets", "images", "backgrounds", "minijuego1", "mini1.png")
        if os.path.exists(bg_path):
            img = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Limites de movimiento (zona amarilla del camino)
        self.move_left_limit: int = int(SCREEN_WIDTH * 0.18)
        self.move_right_limit: int = int(SCREEN_WIDTH * 0.82)

        # Canasta
        self.basket_x: float = SCREEN_WIDTH // 2 - 40
        self.basket_y: int = SCREEN_HEIGHT - 80
        self.basket_width: int = 80
        self.basket_height: int = 30
        self.basket_speed: float = 7.0

        self.chipas: list[FallingChipa] = []
        self.caught: int = 0
        self.missed: int = 0

        # Avion narco
        self.plane_image: pygame.Surface | None = None
        plane_path = os.path.join(os.path.dirname(__file__), "..",
                                  "assets", "images", "ui", "hud", "avion_narco.png")
        if os.path.exists(plane_path):
            img = pygame.image.load(plane_path).convert_alpha()
            self.plane_image = pygame.transform.scale(img, (120, 60))

        self.planes: list[NarcoPlane] = []
        self.plane_spawn_timer: int = 240  # empieza al maximo para que salga el primer avion ya
        self.plane_spawn_interval: int = 240  # cada 4 seg
        self.next_direction: int = 1

        # Audio chipa barrero
        self.chipa_sound: pygame.mixer.Sound | None = None
        sound_path = os.path.join(os.path.dirname(__file__), "..",
                                  "assets", "sounds", "music", "Chipa_Barreeero.wav")
        if os.path.exists(sound_path):
            self.chipa_sound = pygame.mixer.Sound(sound_path)
            self.chipa_sound.set_volume(0.6)
            self.chipa_sound.play(-1)

        # Intro de 2 segundos
        self.intro_timer: int = 120
        self.showing_intro: bool = True

        # Pantalla de victoria
        self.victory_timer: int = 0
        self.showing_victory: bool = False

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

        # Pantalla de victoria antes de completar
        if self.showing_victory:
            self.victory_timer -= 1
            if self.victory_timer <= 0:
                self.completed = True
                self.score_earned = self.caught * 60
                if self.chipa_sound:
                    self.chipa_sound.stop()
            return

        self.timer -= 1

        # Victoria
        if self.caught >= CHIPAS_NEEDED:
            self.showing_victory = True
            self.victory_timer = 180  # 3 seg mostrando mensaje
            return

        # Tiempo agotado
        if self.timer <= 0:
            self.completed = True
            self.failed = True
            self.score_earned = self.caught * 30
            if self.chipa_sound:
                self.chipa_sound.stop()
            return

        # Mover canasta (solo en la zona amarilla del camino)
        if self.input_handler.is_pressed("MOVE_LEFT"):
            self.basket_x -= self.basket_speed
        if self.input_handler.is_pressed("MOVE_RIGHT"):
            self.basket_x += self.basket_speed
        self.basket_x = max(self.move_left_limit,
                            min(self.move_right_limit - self.basket_width, self.basket_x))

        # Spawn aviones
        self.plane_spawn_timer += 1
        if self.plane_spawn_timer >= self.plane_spawn_interval:
            self.plane_spawn_timer = 0
            plane = NarcoPlane(self.plane_image, self.next_direction)
            self.planes.append(plane)
            self.next_direction *= -1

        # Actualizar aviones y soltar chipas
        for plane in self.planes:
            plane.update()
            if plane.should_drop():
                drop_x, drop_y = plane.get_drop_position()
                for i in range(CHIPAS_PER_DROP):
                    cx = random.uniform(self.move_left_limit, self.move_right_limit - 40)
                    delay_y = drop_y - random.randint(0, 60)
                    self.chipas.append(FallingChipa(cx, delay_y))

        self.planes = [p for p in self.planes if p.active]

        # Actualizar chipas
        basket_rect = pygame.Rect(int(self.basket_x), self.basket_y,
                                  self.basket_width, self.basket_height)
        for c in self.chipas:
            c.update()
            if c.active and c.get_rect().colliderect(basket_rect):
                c.active = False
                c.caught = True
                self.caught += 1

        for c in self.chipas:
            if not c.active and not c.caught:
                self.missed += 1

        self.chipas = [c for c in self.chipas if c.active]

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
            self.text.render_title_centered(self.screen, "CHIPA RUSH", 160, 28, YELLOW)
            self.text.render_centered(self.screen,
                                      f"Recolecta {CHIPAS_NEEDED} chipas para pasar!",
                                      240, 14, WHITE)
            self.text.render_centered(self.screen,
                                      "El avion narco tira chipas desde el cielo",
                                      290, 10, (180, 180, 150))
            self.text.render_centered(self.screen,
                                      "Usa las flechas para mover la canasta",
                                      330, 10, (180, 180, 150))
            return

        # Pantalla de victoria
        if self.showing_victory:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            self.text.render_title_centered(self.screen, "MINIJUEGO COMPLETO!", 200, 26, YELLOW)
            self.text.render_centered(self.screen,
                                      f"Recolectaste {self.caught} chipas!",
                                      270, 14, TERERE_GREEN)
            self.text.render_centered(self.screen,
                                      "Preparate para el siguiente nivel...",
                                      330, 10, (180, 180, 180))
            return

        # Aviones
        for plane in self.planes:
            plane.draw(self.screen)

        # Chipas
        for c in self.chipas:
            c.draw(self.screen)

        # Canasta
        basket_rect = pygame.Rect(int(self.basket_x), self.basket_y,
                                  self.basket_width, self.basket_height)
        pygame.draw.rect(self.screen, (180, 130, 60), basket_rect)
        pygame.draw.rect(self.screen, (140, 100, 40), basket_rect, 3)

        # HUD
        self.text.render_title_centered(self.screen, "CHIPA RUSH", 15, 20, YELLOW)
        self.text.render(self.screen, f"Chipas: {self.caught}/{CHIPAS_NEEDED}",
                         20, 65, 10, WHITE)
        self.text.render(self.screen, f"Perdidas: {self.missed}", 20, 80, 10, RED)
        self.text.render(self.screen, f"Tiempo: {self.get_time_remaining():.0f}s",
                         SCREEN_WIDTH - 160, 65, 10, WHITE)

        # Barra de progreso
        bar_x, bar_y, bar_w, bar_h = SCREEN_WIDTH // 2 - 100, 70, 200, 12
        pygame.draw.rect(self.screen, (80, 60, 30), (bar_x, bar_y, bar_w, bar_h))
        fill_w = int(bar_w * min(self.caught / CHIPAS_NEEDED, 1.0))
        pygame.draw.rect(self.screen, TERERE_GREEN, (bar_x, bar_y, fill_w, bar_h))
        pygame.draw.rect(self.screen, (120, 90, 40), (bar_x, bar_y, bar_w, bar_h), 2)

        # Instrucciones
        self.text.render_centered(self.screen, "Flechas y WASD para mover la canasta",
                                  SCREEN_HEIGHT - 25, 10, (150, 150, 120))
