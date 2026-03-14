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

    def play_music(self, path: str, loops: int = -1, volume: float = 0.5) -> None:
        """Reproduce música de fondo. No crashea si el archivo no existe."""
        if not self.initialized:
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
            self.music_playing = True
        except Exception:
            pass
