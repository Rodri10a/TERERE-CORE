"""Minijuego 1: Atrapar guampas de tereré que caen del cielo."""

import pygame
import random
from minigames.base_minigame import BaseMinigame
from core.input_handler import InputHandler
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, TERERE_GREEN, RED
from ui.text_renderer import TextRenderer


class FallingGuampa:
    """Una guampa de tereré cayendo."""

    def __init__(self) -> None:
        self.x: float = random.randint(30, SCREEN_WIDTH - 60)
        self.y: float = -30
        self.width: int = 30
        self.height: int = 40
        self.speed: float = random.uniform(3, 6)
        self.active: bool = True

    def update(self) -> None:
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        # Guampa (vaso)
        pygame.draw.rect(screen, (139, 90, 43), self.get_rect())
        pygame.draw.rect(screen, (100, 70, 35), self.get_rect(), 2)
        # Bombilla
        pygame.draw.line(screen, (180, 180, 180),
                         (int(self.x + 15), int(self.y)),
                         (int(self.x + 20), int(self.y - 15)), 2)


class TerereRush(BaseMinigame):
    """Atrapa guampas de tereré cayendo con una canasta. Dura 30 segundos."""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler) -> None:
        super().__init__(screen, input_handler, duration=1800)  # 30 seg
        self.text = TextRenderer()
        self.basket_x: float = SCREEN_WIDTH // 2 - 40
        self.basket_y: int = SCREEN_HEIGHT - 80
        self.basket_width: int = 80
        self.basket_height: int = 30
        self.basket_speed: float = 7.0
        self.guampas: list[FallingGuampa] = []
        self.spawn_timer: int = 0
        self.caught: int = 0

    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        if self.completed:
            return

        self.timer -= 1
        if self.timer <= 0:
            self.completed = True
            self.score_earned = self.caught * 50
            return

        # Mover canasta
        if self.input_handler.is_pressed("MOVE_LEFT"):
            self.basket_x -= self.basket_speed
        if self.input_handler.is_pressed("MOVE_RIGHT"):
            self.basket_x += self.basket_speed
        self.basket_x = max(0, min(SCREEN_WIDTH - self.basket_width, self.basket_x))

        # Spawn guampas
        self.spawn_timer += 1
        if self.spawn_timer >= 30:
            self.guampas.append(FallingGuampa())
            self.spawn_timer = 0

        # Actualizar guampas
        basket_rect = pygame.Rect(int(self.basket_x), self.basket_y,
                                  self.basket_width, self.basket_height)
        for g in self.guampas:
            g.update()
            if g.active and g.get_rect().colliderect(basket_rect):
                g.active = False
                self.caught += 1

        self.guampas = [g for g in self.guampas if g.active]

    def draw(self) -> None:
        self.screen.fill((30, 80, 50))

        self.text.render_centered(self.screen, "TERERE RUSH!", 20, 30, YELLOW)
        self.text.render(self.screen, f"Atrapadas: {self.caught}", 20, 60, 22, WHITE)
        self.text.render(self.screen, f"Tiempo: {self.get_time_remaining():.0f}s",
                         SCREEN_WIDTH - 150, 60, 22, WHITE)

        # Guampas
        for g in self.guampas:
            g.draw(self.screen)

        # Canasta
        basket_rect = pygame.Rect(int(self.basket_x), self.basket_y,
                                  self.basket_width, self.basket_height)
        pygame.draw.rect(self.screen, (180, 130, 60), basket_rect)
        pygame.draw.rect(self.screen, (140, 100, 40), basket_rect, 3)

        # Instrucciones
        self.text.render_centered(self.screen, "Flechas para mover la canasta",
                                  SCREEN_HEIGHT - 30, 16, (150, 180, 150))
