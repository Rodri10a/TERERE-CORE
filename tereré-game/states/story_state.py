"""Pantalla de historia del juego."""

import os
import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,
                           TERERE_GREEN, YELLOW, GRAY, STATE_GAME, DARK_GREEN)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from ui.text_renderer import TextRenderer


class StoryState:
    """Pantalla que muestra la historia del juego antes de empezar."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.text = TextRenderer()
        self.timer: int = 0
        self.player_name: str = state_manager.shared_data.get("player_name", "Jugador")

        # Imagen de fondo (antesjuego)
        self.bg_image: pygame.Surface | None = None
        bg_path = os.path.join(os.path.dirname(__file__), "..",
                               "assets", "images", "backgrounds", "antesjuego.png")
        if os.path.exists(bg_path):
            img = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_events(self, event: pygame.event.Event) -> None:
        """Avanza con ENTER o click."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.state_manager.shared_data["character"] = "capiateno"
            self.state_manager.change_state(STATE_GAME)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.state_manager.shared_data["character"] = "capiateno"
            self.state_manager.change_state(STATE_GAME)

    def update(self, dt: float) -> None:
        """Actualiza animacion."""
        self.timer += 1

    def draw(self) -> None:
        """Dibuja la pantalla de historia."""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill((15, 30, 15))

        # Titulo
        self.text.render_title_centered(self.screen, "TERERE CORE",
                                        60, 32, YELLOW)
        self.text.render_centered(self.screen, "La venganza del capiateno",
                                  115, 14, (255, 200, 100))

        # Presiona ENTER
        if self.timer > 60:
            flash = (self.timer // 30) % 2 == 0
            if flash:
                self.text.render_centered(self.screen, "Presiona ENTER para comenzar",
                                          SCREEN_HEIGHT - 40, 10, (255, 220, 130))
