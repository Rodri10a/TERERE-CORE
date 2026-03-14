"""Pantalla de victoria al completar el juego."""

import math
import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU,
                           WHITE, YELLOW, TERERE_GREEN, GRAY)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from systems.score import ScoreSystem
from ui.button import Button
from ui.text_renderer import TextRenderer


class VictoryState:
    """Pantalla de victoria con mensaje, puntaje, estrellas y opciones."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.text = TextRenderer()
        self.final_score: int = state_manager.shared_data.get("score", 0)

        # Guardar highscore
        self.score_system = ScoreSystem()
        self.score_system.save_highscore("Capiateno", self.final_score)

        # Calcular estrellas (1-3 según puntaje)
        if self.final_score >= 5000:
            self.stars = 3
        elif self.final_score >= 3000:
            self.stars = 2
        else:
            self.stars = 1

        btn_x = SCREEN_WIDTH // 2 - 100
        self.btn_menu = Button(btn_x, 450, 200, 50, "MENU PRINCIPAL",
                               bg_color=TERERE_GREEN, hover_color=(130, 210, 110))

        self.animation_timer: int = 0

    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.btn_menu.is_clicked(mouse_pos, True):
                self.state_manager.change_state(STATE_MENU)

    def update(self, dt: float) -> None:
        """Actualiza animaciones."""
        self.animation_timer += 1

    def draw(self) -> None:
        """Dibuja la pantalla de victoria."""
        self.screen.fill((20, 50, 30))

        # Partículas de celebración
        for i in range(20):
            angle = (self.animation_timer * 2 + i * 18) * math.pi / 180
            radius = 100 + i * 8
            px = SCREEN_WIDTH // 2 + int(math.cos(angle) * radius)
            py = 200 + int(math.sin(angle) * radius * 0.4)
            colors = [(255, 215, 0), (100, 200, 100), (100, 180, 255)]
            pygame.draw.circle(self.screen, colors[i % 3], (px, py), 4)

        self.text.render_centered(self.screen, "VICTORIA!", 100, 56, YELLOW)
        self.text.render_centered(self.screen, "Recuperaste el terere!",
                                  170, 26, TERERE_GREEN)
        self.text.render_centered(self.screen, "El capiateno triunfa sobre el cheto",
                                  210, 20, WHITE)

        # Estrellas
        star_y = 280
        star_spacing = 60
        start_x = SCREEN_WIDTH // 2 - (self.stars * star_spacing) // 2
        for i in range(self.stars):
            x = start_x + i * star_spacing + 30
            self._draw_star(x, star_y, 20, YELLOW)

        self.text.render_centered(self.screen, f"Puntaje final: {self.final_score}",
                                  350, 32, WHITE)

        rank = "MAESTRO TERERE" if self.stars >= 3 else "CAPIATENO PRO" if self.stars >= 2 else "NOVATO"
        self.text.render_centered(self.screen, f"Rango: {rank}", 395, 22, YELLOW)

        mouse_pos = pygame.mouse.get_pos()
        self.btn_menu.draw(self.screen, mouse_pos)

    def _draw_star(self, cx: int, cy: int, size: int, color: tuple) -> None:
        """Dibuja una estrella en la posición indicada."""
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = size if i % 2 == 0 else size // 2
            points.append((cx + int(math.cos(angle) * r),
                           cy - int(math.sin(angle) * r)))
        pygame.draw.polygon(self.screen, color, points)
