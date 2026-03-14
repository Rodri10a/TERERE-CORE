"""Sistema de puntaje con persistencia en JSON."""

import json
import os
from datetime import datetime


class ScoreSystem:
    """Maneja el puntaje actual y los highscores guardados en data/highscores.json."""

    HIGHSCORE_FILE = "data/highscores.json"
    MAX_HIGHSCORES = 5

    def __init__(self) -> None:
        self.score: int = 0

    def add_points(self, points: int) -> None:
        """Suma puntos al puntaje actual."""
        self.score += points

    def get_score(self) -> int:
        """Retorna el puntaje actual."""
        return self.score

    def reset(self) -> None:
        """Reinicia el puntaje a 0."""
        self.score = 0
