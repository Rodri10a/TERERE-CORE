"""
Tereré Quest - Punto de entrada del juego.
Un juego de pelea 2D con temática paraguaya.
"""

import sys

try:
    import pygame
except ImportError:
    print("Error: pygame no está instalado.")
    print("Instalalo con: pip install pygame")
    sys.exit(1)

from core.game import Game


def main() -> None:
    """Punto de entrada principal del juego."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error fatal: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
