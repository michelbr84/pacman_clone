from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    WIN = auto()
    SETTINGS = auto()
    HIGHSCORES = auto()
    CREDITS = auto()


class StateManager:
    """Stack-based state manager. `transition` replaces; `push`/`pop` layer (e.g. pause)."""

    def __init__(self, initial=GameState.MENU):
        self._stack = [initial]
        self.context = {"level": 1, "score": 0}

    @property
    def current(self):
        return self._stack[-1]

    def transition(self, state):
        self._stack = [state]

    def push(self, state):
        self._stack.append(state)

    def pop(self):
        if len(self._stack) > 1:
            self._stack.pop()
