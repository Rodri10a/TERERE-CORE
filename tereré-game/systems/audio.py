"""Sistema de audio con manejo seguro de archivos faltantes."""

import pygame


class AudioSystem:
    """Maneja música y efectos de sonido sin romper si faltan archivos."""

    def __init__(self) -> None:
        self.initialized: bool = False
        try:
            pygame.mixer.init()
            self.initialized = True
        except Exception:
            pass
        self.music_playing: bool = False
