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

    def save_highscore(self, name: str, score: int) -> bool:
        """Guarda el puntaje si entra en el top 5. Retorna True si es highscore."""
        highscores = self.load_highscores()

        # Verificar si entra al ranking
        if len(highscores) >= self.MAX_HIGHSCORES:
            min_score = min(h["score"] for h in highscores)
            if score <= min_score:
                return False

        entry = {
            "name": name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        highscores.append(entry)
        highscores.sort(key=lambda x: x["score"], reverse=True)
        highscores = highscores[:self.MAX_HIGHSCORES]

        try:
            os.makedirs(os.path.dirname(self.HIGHSCORE_FILE), exist_ok=True)
            with open(self.HIGHSCORE_FILE, "w") as f:
                json.dump({"highscores": highscores}, f, indent=2)
        except Exception:
            pass

        return True
