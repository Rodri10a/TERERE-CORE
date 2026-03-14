"""Motor principal del juego Tereré Quest."""

import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, STATE_MENU
from core.state_manager import StateManager
from core.input_handler import InputHandler


class Game:
    """Clase principal que maneja el loop del juego."""

    def __init__(self) -> None:
        """Inicializa pygame, la pantalla y los sistemas."""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.input_handler = InputHandler()
        self.state_manager = StateManager(self.screen, self.input_handler)
        self.state_manager.change_state(STATE_MENU)

    def handle_events(self) -> None:
        """Procesa eventos de pygame."""
        self.input_handler.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            self.state_manager.handle_events(event)

        if self.state_manager.should_quit:
            self.running = False

    def update(self, dt: float) -> None:
        """Actualiza el estado actual del juego."""
        self.state_manager.update(dt)

    def draw(self) -> None:
        """Dibuja el frame actual."""
        self.state_manager.draw()
        pygame.display.flip()

    def run(self) -> None:
        """Loop principal del juego."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
