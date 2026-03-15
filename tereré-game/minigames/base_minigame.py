"""Clase base abstracta para todos los minijuegos."""

from abc import ABC, abstractmethod
import pygame
from core.input_handler import InputHandler


class BaseMinigame(ABC):
    """Base para minijuegos con timer, puntaje y estado de completado."""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler,
                 duration: int = 1800) -> None:
        self.screen = screen
        self.input_handler = input_handler
        self.duration: int = duration  # En frames (30s = 1800 a 60fps)
        self.timer: int = duration
        self.completed: bool = False
        self.score_earned: int = 0

    def get_time_remaining(self) -> float:
        """Retorna los segundos restantes."""
        return max(0, self.timer / 60.0)

    def progress(self) -> float:
        """Retorna el avance del minijuego de 0.0 (inicio) a 1.0 (fin)."""
        return max(0.0, 1.0 - self.timer / self.duration)

    @abstractmethod
    def update(self) -> None:
        """Actualiza la lógica del minijuego."""
        pass

    @abstractmethod
    def draw(self) -> None:
        """Dibuja el minijuego."""
        pass

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja eventos del minijuego."""
        pass
