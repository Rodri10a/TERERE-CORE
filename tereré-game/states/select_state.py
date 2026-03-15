"""Pantalla de seleccion de personaje."""

import os
import pygame
from core.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,
                           TERERE_GREEN, YELLOW, GRAY, STATE_GAME)
from core.input_handler import InputHandler
from core.state_manager import StateManager
from ui.text_renderer import TextRenderer


CHARACTERS = [
    {
        "name": "Capiateno",
        "file": "personaje_principal.jpg",
        "description": "El capiateno clasico con su sombrero",
    },
    {
        "name": "Karateka",
        "file": "personaje1111.png",
        "description": "Peleador con cinta roja",
    },
    {
        "name": "General",
        "file": "personaje22.webp",
        "description": "El general de rojo",
    },
]


class SelectState:
    """Pantalla donde el jugador elige su personaje."""

    def __init__(self, screen: pygame.Surface, state_manager: StateManager,
                 input_handler: InputHandler) -> None:
        self.screen = screen
        self.state_manager = state_manager
        self.input_handler = input_handler
        self.text = TextRenderer()
        self.selected: int = 0
        self.characters = CHARACTERS
        self.previews: list[pygame.Surface | None] = []
        self._load_previews()

    def _load_previews(self) -> None:
        """Carga las imagenes de preview de cada personaje."""
        base = os.path.join(os.path.dirname(__file__), "..",
                            "assets", "images", "characters")
        for char in self.characters:
            path = os.path.join(base, char["file"])
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (180, 250))
                clean = self._remove_background(img)
                self.previews.append(clean)
            else:
                self.previews.append(None)

    def _remove_background(self, img: pygame.Surface) -> pygame.Surface:
        """Quita el fondo blanco/gris claro de una imagen."""
        w, h = img.get_size()
        clean = pygame.Surface((w, h), pygame.SRCALPHA)
        for px in range(w):
            for py in range(h):
                pixel = img.get_at((px, py))
                r, g, b = pixel[0], pixel[1], pixel[2]
                a = pixel[3] if len(pixel) > 3 else 255
                if a < 30 or (r > 230 and g > 230 and b > 230):
                    continue
                clean.set_at((px, py), (r, g, b, 255))
        return clean

    def handle_events(self, event: pygame.event.Event) -> None:
        """Maneja seleccion con flechas y confirmacion con ENTER."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected = (self.selected - 1) % len(self.characters)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected = (self.selected + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                self.state_manager.shared_data["character"] = self.characters[self.selected]["file"]
                self.state_manager.change_state(STATE_GAME)
            elif event.key == pygame.K_ESCAPE:
                from core.settings import STATE_STORY
                self.state_manager.change_state(STATE_STORY)

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        """Dibuja la pantalla de seleccion."""
        self.screen.fill((20, 35, 20))

        self.text.render_centered(self.screen, "ELIGE TU PERSONAJE",
                                  50, 42, YELLOW)

        # Dibujar los 3 personajes
        total = len(self.characters)
        card_w, card_h = 250, 380
        spacing = 60
        total_w = total * card_w + (total - 1) * spacing
        start_x = SCREEN_WIDTH // 2 - total_w // 2

        for i, char in enumerate(self.characters):
            x = start_x + i * (card_w + spacing)
            y = 140
            is_selected = i == self.selected

            # Fondo de la carta
            if is_selected:
                pygame.draw.rect(self.screen, TERERE_GREEN, (x - 5, y - 5, card_w + 10, card_h + 10), 0, 10)
                pygame.draw.rect(self.screen, YELLOW, (x - 5, y - 5, card_w + 10, card_h + 10), 3, 10)
            else:
                pygame.draw.rect(self.screen, (40, 60, 40), (x, y, card_w, card_h), 0, 8)
                pygame.draw.rect(self.screen, (80, 100, 80), (x, y, card_w, card_h), 2, 8)

            # Imagen del personaje
            if i < len(self.previews) and self.previews[i]:
                img = self.previews[i]
                img_x = x + card_w // 2 - img.get_width() // 2
                img_y = y + 15
                self.screen.blit(img, (img_x, img_y))

            # Nombre (centrado en la carta)
            name_y = y + 275
            color = YELLOW if is_selected else WHITE
            font = self.text._get_font(24)
            name_surf = font.render(char["name"], True, color)
            name_x = x + card_w // 2 - name_surf.get_width() // 2
            self.screen.blit(name_surf, (name_x, name_y))

            # Descripcion (centrada en la carta)
            desc_y = y + 310
            font_sm = self.text._get_font(14)
            desc_surf = font_sm.render(char["description"], True, GRAY)
            desc_x = x + card_w // 2 - desc_surf.get_width() // 2
            self.screen.blit(desc_surf, (desc_x, desc_y))

        # Instrucciones
        self.text.render_centered(self.screen, "< A / D >  para elegir   |   ENTER para confirmar",
                                  570, 18, GRAY)
