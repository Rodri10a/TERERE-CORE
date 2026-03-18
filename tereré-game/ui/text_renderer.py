"""Renderizado de texto con Press Start 2P."""

import pygame
from core.settings import SCREEN_WIDTH, WHITE, FONT_PATH


class TextRenderer:
    """Renderiza texto en pantalla usando Press Start 2P."""

    def __init__(self) -> None:
        self._font_cache: dict[int, pygame.font.Font] = {}

    def _get_font(self, size: int) -> pygame.font.Font:
        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.Font(FONT_PATH, size)
        return self._font_cache[size]

    def _get_title_font(self, size: int) -> pygame.font.Font:
        return self._get_font(size)

    def render(self, screen: pygame.Surface, text: str, x: int, y: int,
               size: int = 12, color: tuple = WHITE) -> None:
        surface = self._get_font(size).render(text, True, color)
        screen.blit(surface, (x, y))

    def render_centered(self, screen: pygame.Surface, text: str, y: int,
                        size: int = 12, color: tuple = WHITE) -> None:
        surface = self._get_font(size).render(text, True, color)
        x = (SCREEN_WIDTH - surface.get_width()) // 2
        screen.blit(surface, (x, y))

    def render_title(self, screen: pygame.Surface, text: str, x: int, y: int,
                     size: int = 32, color: tuple = WHITE) -> None:
        surface = self._get_font(size).render(text, True, color)
        screen.blit(surface, (x, y))

    def render_title_centered(self, screen: pygame.Surface, text: str, y: int,
                              size: int = 32, color: tuple = WHITE) -> None:
        surface = self._get_font(size).render(text, True, color)
        x = (SCREEN_WIDTH - surface.get_width()) // 2
        screen.blit(surface, (x, y))
