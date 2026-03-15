"""Pantalla de Game Over."""

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
                self.state_manager.shared_data["player_health"] = 100
                self.state_manager.change_state(STATE_GAME)
            elif self.btn_menu.is_clicked(mouse_pos, True):
                self.state_manager.change_state(STATE_MENU)

    def update(self, dt: float) -> None:
        """Actualiza animaciones."""
        self.animation_timer += 1

    def draw(self) -> None:
        """Dibuja la pantalla de game over."""
        self.screen.fill((40, 15, 15))

        # Título con shake
        shake_x = 0
        if self.animation_timer < 30:
            import random
            shake_x = random.randint(-3, 3)

        self.text.render_centered(self.screen, "GAME OVER", 120 + shake_x, 52, RED)

        self.text.render_centered(self.screen, "El cheto se escapó con tu tereré...",
                                200, 22, (200, 180, 180))

        self.text.render_centered(self.screen, f"Puntaje final: {self.final_score}",
                                270, 32, YELLOW)

        if self.is_highscore:
            self.text.render_centered(self.screen, "NUEVO HIGHSCORE!", 320, 24, (255, 215, 0))

        mouse_pos = pygame.mouse.get_pos()
        self.btn_retry.draw(self.screen, mouse_pos)
        self.btn_menu.draw(self.screen, mouse_pos)
