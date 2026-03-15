"""Pantalla de menú principal del juego."""

import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE,
                           TERERE_GREEN, STATE_NAME, YELLOW, DARK_GREEN, GRAY)
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
                self.state_manager.change_state(STATE_NAME)
            elif self.btn_scores.is_clicked(mouse_pos, True):
                self.show_scores = True
            elif self.btn_quit.is_clicked(mouse_pos, True):
                self.state_manager.should_quit = True

    def update(self, dt: float) -> None:
        """Actualiza animaciones del menú."""
        self.animation_timer += 1

    def draw(self) -> None:
        """Dibuja el menú principal."""
        self.screen.fill((30, 60, 30))

        # Fondo decorativo
        for i in range(0, SCREEN_WIDTH, 40):
            offset = (self.animation_timer + i) % 600
            alpha_y = offset - 100
            pygame.draw.circle(self.screen, (40, 70, 40),
                               (i + 20, alpha_y % SCREEN_HEIGHT), 3)

        if self.show_scores:
            self._draw_scores()
            return

        # Título
        bounce = abs((self.animation_timer % 60) - 30) / 30.0 * 5
        self.text.render_centered(self.screen, "TERERE CORE",
                                  int(80 + bounce), 52, YELLOW)
        self.text.render_centered(self.screen, "TERERE CORE",
                                  int(82 + bounce), 50, TERERE_GREEN)

        # Subtítulo
        self.text.render_centered(self.screen, "La venganza del capiateno",
                                  150, 22, WHITE)

        # Historia
        story_lines = [
            "Un cheto de Asuncion robo el terere",
            "de unos capiatenos en la plaza...",
            "",
            "Recupera tu terere enfrentando al cheto",
            "en peleas epicas y minijuegos!",
        ]
        y = 200
        for line in story_lines:
            if line:
                self.text.render_centered(self.screen, line, y, 18, (200, 220, 200))
            y += 25

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        self.btn_play.draw(self.screen, mouse_pos)
        self.btn_scores.draw(self.screen, mouse_pos)
        self.btn_quit.draw(self.screen, mouse_pos)

        # Controles
        self.text.render_centered(self.screen, "Flechas/A D: Mover | ESPACIO/W: Saltar | ENTER: Atacar | J: Especial",
                                  570, 14, GRAY)

    def _draw_scores(self) -> None:
        """Dibuja la pantalla de highscores."""
        self.text.render_centered(self.screen, "HIGHSCORES", 60, 40, YELLOW)

        if not self.highscores:
            self.text.render_centered(self.screen, "No hay puntajes aun", 200, 24, GRAY)
        else:
            for i, entry in enumerate(self.highscores[:5]):
                name = entry.get("name", "???")
                score = entry.get("score", 0)
                text = f"{i + 1}. {name} - {score}"
                self.text.render_centered(self.screen, text, 150 + i * 40, 24, WHITE)

        self.text.render_centered(self.screen, "Click para volver", 500, 20, GRAY)
