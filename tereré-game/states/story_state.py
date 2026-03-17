"""Pantalla de historia del juego."""

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
        self.screen.fill((15, 30, 15))

        # Titulo
        self.text.render_centered(self.screen, "TERERE CORE",
                                  60, 48, YELLOW)
        self.text.render_centered(self.screen, "La venganza del capiateno",
                                  120, 24, TERERE_GREEN)

        # Linea decorativa
        line_y = 160
        pygame.draw.line(self.screen, TERERE_GREEN,
                         (SCREEN_WIDTH // 2 - 200, line_y),
                         (SCREEN_WIDTH // 2 + 200, line_y), 2)

        # Historia con aparicion gradual
        story = [
            f"{self.player_name} es un capiateno que estaba",
            "tranquilamente tomando terere con sus amigos",
            "en la plaza de Capiata...",
            "",
            "De repente, un cheto de Asuncion aparecio",
            "con su auto importado y les robo el terere!",
            "",
            "Ahora {name} debe recorrer todo el pais",
            "desde Capiata hasta Villarrica,",
            "enfrentando al cheto en peleas epicas",
            "y superando minijuegos para recuperar",
            "su preciado terere!",
        ]

        y = 200
        for i, line in enumerate(story):
            # Aparicion gradual: cada linea aparece 15 frames despues de la anterior
            if self.timer > i * 15:
                line = line.replace("{name}", self.player_name)
                if line:
                    color = (200, 220, 200) if line[0] != " " else GRAY
                    self.text.render_centered(self.screen, line, y, 20, color)
            y += 30

        # Instruccion para continuar (aparece despues de toda la historia)
        if self.timer > len(story) * 15 + 30:
            flash = (self.timer // 30) % 2 == 0
            if flash:
                self.text.render_centered(self.screen, "Presiona ENTER para comenzar la aventura!",
                                          620, 20, TERERE_GREEN)
