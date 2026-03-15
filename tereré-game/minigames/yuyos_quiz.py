"""Minijuego 3: Quiz sobre yuyos paraguayos para el tereré."""

import pygame
import random
from minigames.base_minigame import BaseMinigame
from core.input_handler import InputHandler
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, GREEN, RED, GRAY, TERERE_GREEN
from ui.button import Button
from ui.text_renderer import TextRenderer


YUYOS_DATA = [
    {"nombre": "Menta'i", "desc": "Refrescante y digestiva, la mas comun en el terere"},
    {"nombre": "Burrito", "desc": "Hierba aromatica con sabor mentolado suave"},
    {"nombre": "Cedron", "desc": "Citrico y relajante, ideal para el terere de la tarde"},
    {"nombre": "Kokuu", "desc": "Amarga y medicinal, usada para problemas estomacales"},
    {"nombre": "Jaguarete Ka'a", "desc": "Planta medicinal usada para dolor de huesos"},
    {"nombre": "Ka'are", "desc": "Usada para dolores de cabeza y fiebre"},
    {"nombre": "Jatei Ka'a", "desc": "Dulce como la miel, hierba suave y refrescante"},
    {"nombre": "Perdudilla", "desc": "Hierba fresca ideal para dias de mucho calor"},
    {"nombre": "Santa Lucia", "desc": "Usada para problemas de la vista y ojos cansados"},
    {"nombre": "Boldo", "desc": "Amarga, ideal para el higado y la digestion"},
]


class YuyosQuiz(BaseMinigame):
    """Quiz de yuyos paraguayos. 3 preguntas, 10 segundos cada una."""

    def __init__(self, screen: pygame.Surface, input_handler: InputHandler) -> None:
        super().__init__(screen, input_handler, duration=1800)
        self.text = TextRenderer()
        self.questions: list[dict] = []
        self.current_question: int = 0
        self.total_questions: int = 3
        self.question_timer: int = 600  # 10 seg por pregunta
        self.correct_answers: int = 0
        self.answered: bool = False
        self.answer_result: str = ""
        self.answer_timer: int = 0
        self.buttons: list[Button] = []

        self._generate_questions()
        self._setup_current_question()

    def _generate_questions(self) -> None:
        """Genera 3 preguntas aleatorias sobre yuyos."""
        shuffled = random.sample(YUYOS_DATA, min(self.total_questions, len(YUYOS_DATA)))
        for yuyo in shuffled:
            others = [y["nombre"] for y in YUYOS_DATA if y["nombre"] != yuyo["nombre"]]
            wrong = random.sample(others, 2)
            options = [yuyo["nombre"]] + wrong
            random.shuffle(options)
            self.questions.append({
                "description": yuyo["desc"],
                "correct": yuyo["nombre"],
                "options": options,
            })

    def _setup_current_question(self) -> None:
        """Configura los botones para la pregunta actual."""
        if self.current_question >= len(self.questions):
            return
        q = self.questions[self.current_question]
        self.buttons = []
        btn_x = SCREEN_WIDTH // 2 - 120
        for i, option in enumerate(q["options"]):
            btn = Button(btn_x, 320 + i * 70, 240, 50, option,
                         bg_color=(60, 100, 60), hover_color=(80, 140, 80))
            self.buttons.append(btn)
        self.question_timer = 600
        self.answered = False

    def handle_events(self, event: pygame.event.Event) -> None:
        if self.completed or self.answered:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            q = self.questions[self.current_question]
            for i, btn in enumerate(self.buttons):
                if btn.is_clicked(mouse_pos, True):
                    self.answered = True
                    if q["options"][i] == q["correct"]:
                        self.correct_answers += 1
                        self.answer_result = "CORRECTO!"
                    else:
                        self.answer_result = f"Incorrecto! Era: {q['correct']}"
                    self.answer_timer = 90
                    break

    def update(self) -> None:
        if self.completed:
            return

        self.timer -= 1

        if self.answered:
            self.answer_timer -= 1
            if self.answer_timer <= 0:
                self.current_question += 1
                if self.current_question >= self.total_questions:
                    self.completed = True
                    self.score_earned = self.correct_answers * 200
                else:
                    self._setup_current_question()
            return

        self.question_timer -= 1
        if self.question_timer <= 0:
            self.answered = True
            q = self.questions[self.current_question]
            self.answer_result = f"Tiempo! Era: {q['correct']}"
            self.answer_timer = 90

    def draw(self) -> None:
        self.screen.fill((40, 50, 30))

        self.text.render_centered(self.screen, "QUIZ DE YUYOS", 20, 30, YELLOW)
        self.text.render(self.screen,
                         f"Pregunta {self.current_question + 1}/{self.total_questions}",
                         20, 65, 20, WHITE)

        if self.completed:
            self.text.render_centered(self.screen,
                                      f"Resultado: {self.correct_answers}/{self.total_questions}",
                                      250, 36, TERERE_GREEN)
            return

        q = self.questions[self.current_question]

        # Timer
        time_left = self.question_timer / 60.0
        timer_color = WHITE if time_left > 3 else RED
        self.text.render(self.screen, f"Tiempo: {time_left:.0f}s",
                         SCREEN_WIDTH - 150, 65, 20, timer_color)

        # Pregunta
        self.text.render_centered(self.screen, "Que yuyo es este?", 120, 24, TERERE_GREEN)
        self.text.render_centered(self.screen, f'"{q["description"]}"', 170, 20, WHITE)

        if self.answered:
            color = GREEN if "CORRECTO" in self.answer_result else RED
            self.text.render_centered(self.screen, self.answer_result, 250, 28, color)
        else:
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                btn.draw(self.screen, mouse_pos)
