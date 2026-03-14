"""Renderizado de texto con fuente por defecto de pygame."""

import pygame
from core.settings import SCREEN_WIDTH, WHITE


class TextRenderer:
    """Renderiza texto en pantalla con soporte para centrado y diferentes tamaños."""

    def __init__(self) -> None:
        self._font_cache: dict[int, pygame.font.Font] = {}

    def _get_font(self, size: int) -> pygame.font.Font:
        """Obtiene o crea una fuente del tamaño indicado."""
        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.Font(None, size)
        return self._font_cache[size]

    def render(self, screen: pygame.Surface, text: str, x: int, y: int,
               size: int = 24, color: tuple = WHITE) -> None:
        """Renderiza texto en la posición (x, y)."""
        font = self._get_font(size)
        surface = font.render(text, True, color)
        screen.blit(surface, (x, y))

    def render_centered(self, screen: pygame.Surface, text: str, y: int,
                        size: int = 24, color: tuple = WHITE) -> None:
        """Renderiza texto centrado horizontalmente en la pantalla."""
        font = self._get_font(size)
        surface = font.render(text, True, color)
        x = (SCREEN_WIDTH - surface.get_width()) // 2
        screen.blit(surface, (x, y))
