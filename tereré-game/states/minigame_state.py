"""Estado de transición que carga y ejecuta minijuegos entre niveles."""

import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, STATE_GAME, STATE_MENU,
                           STATE_GAMEOVER, WHITE, BLACK, TERERE_GREEN, YELLOW, RED)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from minigames.terere_rush import TerereRush
from minigames.esquiva_cheto import EsquivaCheto
from minigames.yuyos_quiz import YuyosQuiz
from ui.text_renderer import TextRenderer
from ui.button import Button


MINIGAME_MAP = {
    "terere_rush": TerereRush,
    "esquiva_cheto": EsquivaCheto,
    "yuyos_quiz": YuyosQuiz,
}


class MinigameState:
    """Carga el minijuego correspondiente al nivel y transiciona al siguiente nivel al terminar."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.text = TextRenderer()

        self.minigame_id: str = state_manager.shared_data.get("minigame_id", "terere_rush")
        minigame_class = MINIGAME_MAP.get(self.minigame_id, TerereRush)
        self.minigame = minigame_class(screen, input_handler)

        self.show_result: bool = False
        self.show_failed: bool = False
        self.result_timer: int = 180

        # Pausa
        self.paused: bool = False
        self.show_instructions: bool = False
        self._setup_pause_buttons()

    def handle_events(self, event: pygame.event.Event) -> None:
        """Pasa eventos al minijuego activo."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.show_instructions:
                self.show_instructions = False
            elif not self.show_result:
                self.paused = not self.paused

        if self.paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.pause_buttons["reanudar"].is_clicked(mouse_pos, True):
                self.paused = False
            elif self.pause_buttons["instrucciones"].is_clicked(mouse_pos, True):
                self.show_instructions = True
            elif self.pause_buttons["menu"].is_clicked(mouse_pos, True):
                self.state_manager.change_state(STATE_MENU)
            elif self.pause_buttons["salir"].is_clicked(mouse_pos, True):
                self.state_manager.should_quit = True
            return

        if not self.show_result and not self.paused:
            self.minigame.handle_events(event)

    def update(self, dt: float) -> None:
        """Actualiza el minijuego o la pantalla de resultados."""
        if self.paused:
            return

        if self.show_result:
            self.result_timer -= 1
            if self.result_timer <= 0:
                if self.show_failed:
                    self.state_manager.change_state(STATE_GAMEOVER)
                else:
                    self._advance_to_next_level()
            return

        self.minigame.update()

        if self.minigame.completed:
            self.state_manager.shared_data["score"] += self.minigame.score_earned
            if self.minigame.failed:
                self.show_failed = True
            self.show_result = True

    def _setup_pause_buttons(self) -> None:
        """Crea los botones del menú de pausa."""
        cx = SCREEN_WIDTH // 2 - 110
        self.pause_buttons = {
            "reanudar":      Button(cx, 210, 220, 45, "Reanudar",
                                   bg_color=(40, 100, 40), hover_color=(60, 140, 60)),
            "instrucciones": Button(cx, 270, 220, 45, "Instrucciones",
                                   bg_color=(40, 60, 100), hover_color=(60, 90, 140)),
            "menu":          Button(cx, 330, 220, 45, "Volver al Menu",
                                   bg_color=(80, 60, 30), hover_color=(120, 90, 45)),
            "salir":         Button(cx, 390, 220, 45, "Salir",
                                   bg_color=(100, 30, 30), hover_color=(140, 50, 50)),
        }

    def _draw_pause_menu(self) -> None:
        """Dibuja el overlay del menú de pausa."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        self.text.render_centered(self.screen, "PAUSA", 130, 48, WHITE)
        if self.show_instructions:
            self._draw_pause_instructions()
            return
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.pause_buttons.values():
            btn.draw(self.screen, mouse_pos)

    def _draw_pause_instructions(self) -> None:
        """Dibuja los controles del minijuego activo."""
        self.text.render_centered(self.screen, "CONTROLES", 185, 26, TERERE_GREEN)
        instructions = {
            "terere_rush":   [("Mover canasta", "Flechas  /  A  D")],
            "esquiva_cheto": [("Cambiar carril", "Flechas  /  W  S")],
            "yuyos_quiz":    [("Seleccionar",    "Click izquierdo")],
        }
        lines = instructions.get(self.minigame_id, [])
        lines.append(("Pausar", "Escape"))
        y = 250
        for action, keys in lines:
            self.text.render(self.screen, action, 200, y, 20, WHITE)
            self.text.render(self.screen, keys, 440, y, 20, TERERE_GREEN)
            y += 40
        self.text.render_centered(self.screen, "Escape para volver", 450, 16, (150, 150, 150))

    def _advance_to_next_level(self) -> None:
        """Avanza al siguiente nivel de pelea."""
        current = self.state_manager.shared_data.get("current_level", 1)
        self.state_manager.shared_data["current_level"] = current + 1
        self.state_manager.change_state(STATE_GAME)

    def draw(self) -> None:
        """Dibuja el minijuego o los resultados."""
        if self.show_result:
            if self.show_failed:
                self.screen.fill((50, 20, 20))
                self.text.render_centered(self.screen, "PERDISTE!",
                                          180, 36, RED)
                self.text.render_centered(self.screen, "Te quedaste sin vidas...",
                                          260, 28, WHITE)
                self.text.render_centered(self.screen,
                                          f"Puntaje final: {self.state_manager.shared_data['score']}",
                                          310, 22, TERERE_GREEN)
            else:
                self.screen.fill((20, 40, 20))
                self.text.render_centered(self.screen, "MINIJUEGO COMPLETADO!",
                                          180, 36, YELLOW)
                self.text.render_centered(self.screen, f"Puntos ganados: {self.minigame.score_earned}",
                                          260, 28, WHITE)
                self.text.render_centered(self.screen,
                                          f"Puntaje total: {self.state_manager.shared_data['score']}",
                                          310, 22, TERERE_GREEN)
                self.text.render_centered(self.screen, "Preparate para el siguiente nivel...",
                                          400, 20, (180, 180, 180))
        else:
            self.minigame.draw()

        if self.paused:
            self._draw_pause_menu()
