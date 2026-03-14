"""Pantalla de menú principal del juego."""

import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE,
                           TERERE_GREEN, STATE_GAME, YELLOW, DARK_GREEN, GRAY)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from ui.button import Button
from ui.text_renderer import TextRenderer


class MenuState:
    """Menú principal con título, historia y botones de navegación."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.text = TextRenderer()
        self.animation_timer: int = 0

        # Botones
        btn_x = SCREEN_WIDTH // 2 - 100
        self.btn_play = Button(btn_x, 360, 200, 50, "JUGAR",
                               bg_color=TERERE_GREEN, hover_color=(130, 210, 110))
        self.btn_scores = Button(btn_x, 425, 200, 50, "HIGHSCORES",
                                 bg_color=(80, 130, 180), hover_color=(110, 160, 210))
        self.btn_quit = Button(btn_x, 490, 200, 50, "SALIR",
                               bg_color=(180, 60, 60), hover_color=(210, 90, 90))

        self.show_scores: bool = False
        self.highscores: list = []
        self._load_scores()

    def _load_scores(self) -> None:
        """Carga highscores desde archivo."""
        try:
            import json
            with open("data/highscores.json", "r") as f:
                data = json.load(f)
                self.highscores = data.get("highscores", [])
        except (FileNotFoundError, Exception):
            self.highscores = []

    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja clicks en botones del menú."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.show_scores:
                self.show_scores = False
                return
            if self.btn_play.is_clicked(mouse_pos, True):
                self.state_manager.shared_data["score"] = 0
                self.state_manager.shared_data["current_level"] = 1
                self.state_manager.shared_data["player_health"] = 100
                self.state_manager.change_state(STATE_GAME)
            elif self.btn_scores.is_clicked(mouse_pos, True):
                self.show_scores = True
            elif self.btn_quit.is_clicked(mouse_pos, True):
                self.state_manager.should_quit = True
