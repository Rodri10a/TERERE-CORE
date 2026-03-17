"""Pantalla de Game Over."""

import os
import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU, STATE_GAME,
                           WHITE, RED, YELLOW, GRAY)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from systems.score import ScoreSystem
from ui.button import Button
from ui.text_renderer import TextRenderer


class GameOverState:
    """Pantalla de derrota con puntaje final, guardado de highscore y opciones."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.text = TextRenderer()
        self.final_score: int = state_manager.shared_data.get("score", 0)

        # Imagen de fondo
        self.bg_image: pygame.Surface | None = None
        bg_path = os.path.join(os.path.dirname(__file__), "..",
                               "assets", "images", "backgrounds", "gameover.jpg")
        if os.path.exists(bg_path):
            img = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Guardar highscore
        self.score_system = ScoreSystem()
        self.is_highscore = self.score_system.save_highscore("Capiateno", self.final_score)

        btn_x = SCREEN_WIDTH // 2 - 100
        self.btn_retry = Button(btn_x, 380, 200, 50, "REINTENTAR",
                                bg_color=(80, 150, 80), hover_color=(110, 180, 110))
        self.btn_menu = Button(btn_x, 450, 200, 50, "MENU PRINCIPAL",
                               bg_color=(80, 80, 150), hover_color=(110, 110, 180))

        self.animation_timer: int = 0

    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja clicks en botones."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.btn_retry.is_clicked(mouse_pos, True):
                self.state_manager.shared_data["score"] = 0
                self.state_manager.shared_data["current_level"] = 1
                self.state_manager.shared_data["player_health"] = 250
                self.state_manager.change_state(STATE_GAME)
            elif self.btn_menu.is_clicked(mouse_pos, True):
                self.state_manager.change_state(STATE_MENU)

    def update(self, dt: float) -> None:
        """Actualiza animaciones."""
        self.animation_timer += 1

    def draw(self) -> None:
        """Dibuja la pantalla de game over."""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill((40, 15, 15))

        # Título con shake
        shake_x = 0
        if self.animation_timer < 30:
            import random
            shake_x = random.randint(-3, 3)

        self.text.render_title_centered(self.screen, "GAME OVER", 100 + shake_x, 32, RED)

        self.text.render_centered(self.screen, "El cheto se escapo con tu terere...",
                                  180, 12, (200, 180, 180))

        self.text.render_centered(self.screen, f"Puntaje final: {self.final_score}",
                                  240, 16, YELLOW)

        if self.is_highscore:
            self.text.render_centered(self.screen, "NUEVO HIGHSCORE", 290, 14, (255, 215, 0))

        mouse_pos = pygame.mouse.get_pos()
        self.btn_retry.draw(self.screen, mouse_pos)
        self.btn_menu.draw(self.screen, mouse_pos)
