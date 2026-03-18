"""Pantalla de ingreso de nombre del jugador."""

import os
import math
import random
import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE,
                           TERERE_GREEN, YELLOW, GRAY, STATE_GAME, DARK_GREEN)
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

        # Fondo
        try:
            bg_path = os.path.join(os.path.dirname(__file__), "..",
                                   "assets", "images", "backgrounds", "menu_del_nombre.png")
            bg = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.background = None

        # Partículas de polvo flotando en el rayo de luz
        self.particles = [
            {
                "x": random.randint(380, 700),
                "y": random.randint(200, 600),
                "vy": random.uniform(-0.3, -0.1),
                "vx": random.uniform(-0.15, 0.15),
                "size": random.randint(1, 3),
                "alpha": random.randint(60, 180),
            }
            for _ in range(35)
        ]

    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja entrada de texto del jugador."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                self.state_manager.shared_data["player_name"] = self.player_name
                self.state_manager.shared_data["character"] = "capiateno"
                self.state_manager.change_state(STATE_GAME)
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_ESCAPE:
                from core.settings import STATE_MENU
                self.state_manager.change_state(STATE_MENU)
            elif len(self.player_name) < self.max_length and event.unicode.isprintable() and event.unicode:
                self.player_name += event.unicode

    def update(self, dt: float) -> None:
        """Actualiza animaciones."""
        self.cursor_timer += 1

        # Mover partículas
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            # Reiniciar si salen del área del rayo de luz
            if p["y"] < 180 or p["x"] < 340 or p["x"] > 740:
                p["x"] = random.randint(400, 680)
                p["y"] = random.randint(500, 600)
                p["vy"] = random.uniform(-0.3, -0.1)
                p["vx"] = random.uniform(-0.15, 0.15)
                p["alpha"] = random.randint(60, 180)

    def draw(self) -> None:
        """Dibuja la pantalla de ingreso de nombre."""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((20, 40, 20))

        # Partículas de polvo
        for p in self.particles:
            surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 220, 150, p["alpha"]), (p["size"], p["size"]), p["size"])
            self.screen.blit(surf, (int(p["x"]), int(p["y"])))

        # Título con bounce y pulso de color
        bounce = abs(math.sin(self.cursor_timer * 0.05)) * 6
        pulse = int(200 + 55 * abs(math.sin(self.cursor_timer * 0.03)))
        title_y = int(148 + bounce)
        self.text.render_title_centered(self.screen, "INGRESA TU NOMBRE",
                                        title_y + 2, 20, (60, 30, 10))
        self.text.render_title_centered(self.screen, "INGRESA TU NOMBRE",
                                        title_y, 20, (pulse, 200, 60))

        # Caja de texto — borde con pulso
        box_w, box_h = 420, 60
        box_x = SCREEN_WIDTH // 2 - box_w // 2
        box_y = 310
        border_r = int(180 + 60 * abs(math.sin(self.cursor_timer * 0.04)))
        border_g = int(120 + 40 * abs(math.sin(self.cursor_timer * 0.04)))

        overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        overlay.fill((30, 15, 5, 180))
        self.screen.blit(overlay, (box_x, box_y))
        pygame.draw.rect(self.screen, (border_r, border_g, 50), (box_x, box_y, box_w, box_h), 3)

        # Texto ingresado + cursor parpadeante, centrado en el box
        cursor = "_" if (self.cursor_timer // 30) % 2 == 0 else ""
        display_text = self.player_name + cursor
        font = self.text._get_font(16)
        text_surf = font.render(display_text, True, (255, 230, 150))
        text_x = box_x + (box_w - text_surf.get_width()) // 2
        text_y = box_y + (box_h - text_surf.get_height()) // 2
        self.screen.blit(text_surf, (text_x, text_y))

        # Instrucciones
        self.text.render_centered(self.screen, "Presiona ENTER para continuar",
                                  430, 10, (255, 240, 180))
        self.text.render_centered(self.screen, "ESC para volver al menu",
                                  455, 10, (255, 240, 180))
