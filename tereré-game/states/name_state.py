"""Pantalla de ingreso de nombre del jugador."""

import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,
                           TERERE_GREEN, YELLOW, GRAY, STATE_STORY, DARK_GREEN)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from ui.text_renderer import TextRenderer


class NameState:
    """Pantalla donde el jugador ingresa su nombre antes de jugar."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.text = TextRenderer()
        self.player_name: str = ""
        self.max_length: int = 15
        self.cursor_timer: int = 0

    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja entrada de texto del jugador."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                self.state_manager.shared_data["player_name"] = self.player_name
                self.state_manager.change_state(STATE_STORY)
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_ESCAPE:
                from core.settings import STATE_MENU
                self.state_manager.change_state(STATE_MENU)
            elif len(self.player_name) < self.max_length and event.unicode.isprintable() and event.unicode:
                self.player_name += event.unicode

    def update(self, dt: float) -> None:
        """Actualiza animacion del cursor."""
        self.cursor_timer += 1

    def draw(self) -> None:
        """Dibuja la pantalla de ingreso de nombre."""
        self.screen.fill((20, 40, 20))

        self.text.render_centered(self.screen, "INGRESA TU NOMBRE",
                                  150, 42, TERERE_GREEN)

        # Caja de texto
        box_w, box_h = 400, 60
        box_x = SCREEN_WIDTH // 2 - box_w // 2
        box_y = 280
        pygame.draw.rect(self.screen, (40, 70, 40), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(self.screen, TERERE_GREEN, (box_x, box_y, box_w, box_h), 3)

        # Texto ingresado + cursor parpadeante
        cursor = "|" if (self.cursor_timer // 30) % 2 == 0 else ""
        display_text = self.player_name + cursor
        self.text.render_centered(self.screen, display_text, box_y + 18, 28, WHITE)

        # Instrucciones
        self.text.render_centered(self.screen, "Presiona ENTER para continuar",
                                  420, 18, GRAY)
        self.text.render_centered(self.screen, "ESC para volver al menu",
                                  450, 14, (100, 100, 100))
