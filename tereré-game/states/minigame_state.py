"""Estado de transición que carga y ejecuta minijuegos entre niveles."""

import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, STATE_GAME,
                           WHITE, BLACK, TERERE_GREEN, YELLOW)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from minigames.terere_rush import TerereRush
from minigames.esquiva_cheto import EsquivaCheto
from minigames.yuyos_quiz import YuyosQuiz
from ui.text_renderer import TextRenderer


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

        minigame_id = state_manager.shared_data.get("minigame_id", "terere_rush")
        minigame_class = MINIGAME_MAP.get(minigame_id, TerereRush)
        self.minigame = minigame_class(screen, input_handler)

        self.show_result: bool = False
        self.result_timer: int = 180

    def handle_events(self, event: pygame.event.Event) -> None:
        """Pasa eventos al minijuego activo."""
        if not self.show_result:
            self.minigame.handle_events(event)

    def update(self, dt: float) -> None:
        """Actualiza el minijuego o la pantalla de resultados."""
        if self.show_result:
            self.result_timer -= 1
            if self.result_timer <= 0:
                self._advance_to_next_level()
            return

        self.minigame.update()

        if self.minigame.completed:
            self.state_manager.shared_data["score"] += self.minigame.score_earned
            self.show_result = True

    def _advance_to_next_level(self) -> None:
        """Avanza al siguiente nivel de pelea."""
        current = self.state_manager.shared_data.get("current_level", 1)
        self.state_manager.shared_data["current_level"] = current + 1
        self.state_manager.change_state(STATE_GAME)

    def draw(self) -> None:
        """Dibuja el minijuego o los resultados."""
        if self.show_result:
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
