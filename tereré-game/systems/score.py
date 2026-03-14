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
