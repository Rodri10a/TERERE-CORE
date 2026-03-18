"""Pantalla de menú principal del juego."""

import os
import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE,
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

        # Imagen de fondo
        self.bg_image: pygame.Surface | None = None
        bg_path = os.path.join(os.path.dirname(__file__), "..",
                               "assets", "images", "backgrounds", "screen.png")
        if os.path.exists(bg_path):
            img = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Música de portada
        self.portada_music: pygame.mixer.Sound | None = None
        music_path = os.path.join(os.path.dirname(__file__), "..",
                                  "assets", "sounds", "music", "portada.mp3")
        if os.path.exists(music_path):
            self.portada_music = pygame.mixer.Sound(music_path)
            self.portada_music.set_volume(0.5)
            self.portada_music.play(-1)
        # Guardar referencia en shared_data para que otros estados puedan pararla
        state_manager.shared_data["portada_music"] = self.portada_music

        # Botones en horizontal abajo (HIGHSCORES - JUGAR - SALIR)
        btn_w = 180
        btn_h = 45
        btn_y = 660
        gap = 20
        center_x = SCREEN_WIDTH // 2 - btn_w // 2
        self.btn_scores = Button(center_x - btn_w - gap, btn_y, btn_w, btn_h, "HIGHSCORES",
                                 bg_color=(80, 130, 180), hover_color=(110, 160, 210))
        self.btn_play = Button(center_x, btn_y, btn_w, btn_h, "JUGAR",
                               bg_color=TERERE_GREEN, hover_color=(130, 210, 110))
        self.btn_quit = Button(center_x + btn_w + gap, btn_y, btn_w, btn_h, "SALIR",
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
                self.state_manager.shared_data["player_health"] = 250
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
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill((30, 60, 30))

        if self.show_scores:
            self._draw_scores()
            return

        # Título
        self.text.render_title_centered(self.screen, "TERERE CORE", 80, 32, YELLOW)

        # Subtítulo
        self.text.render_centered(self.screen, "La venganza del capiateño",
                                  130, 14, (255, 200, 100))

        # Botones
        mouse_pos = pygame.mouse.get_pos()
        self.btn_play.draw(self.screen, mouse_pos)
        self.btn_scores.draw(self.screen, mouse_pos)
        self.btn_quit.draw(self.screen, mouse_pos)

    def _draw_scores(self) -> None:
        """Dibuja la pantalla de highscores."""
        self.text.render_title_centered(self.screen, "HIGHSCORES", 60, 24, YELLOW)

        if not self.highscores:
            self.text.render_centered(self.screen, "No hay puntajes aun", 200, 12, GRAY)
        else:
            for i, entry in enumerate(self.highscores[:5]):
                name = entry.get("name", "???")
                score = entry.get("score", 0)
                text = f"{i + 1}. {name} - {score}"
                self.text.render_centered(self.screen, text, 160 + i * 45, 12, WHITE)

        self.text.render_centered(self.screen, "Click para volver", 500, 10, GRAY)
