"""Botón clickeable para menús e interfaces."""

import pygame
from core.settings import WHITE, BLACK


class Button:
    """Botón con texto, estados normal/hover y detección de click."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 bg_color: tuple = (80, 80, 80),
                 hover_color: tuple = (120, 120, 120),
                 text_color: tuple = WHITE,
                 font_size: int = 24) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
