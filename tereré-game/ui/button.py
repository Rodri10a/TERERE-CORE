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

    def is_clicked(self, mouse_pos: tuple, mouse_click: bool) -> bool:
        """Retorna True si el botón fue clickeado."""
        return mouse_click and self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface, mouse_pos: tuple = (0, 0)) -> None:
        """Dibuja el botón con efecto hover."""
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.bg_color

        # Sombra
        shadow = self.rect.move(3, 3)
        pygame.draw.rect(screen, (30, 30, 30), shadow, border_radius=6)
        # Fondo
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        # Borde
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=6)

        # Texto centrado
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
