from scripts.game_state import GameState, StateManager


def test_initial_state_is_menu():
    sm = StateManager()
    assert sm.current == GameState.MENU


def test_transition_replaces_stack():
    sm = StateManager()
    sm.transition(GameState.PLAYING)
    assert sm.current == GameState.PLAYING


def test_push_pop_pause():
    sm = StateManager()
    sm.transition(GameState.PLAYING)
    sm.push(GameState.PAUSED)
    assert sm.current == GameState.PAUSED
    sm.pop()
    assert sm.current == GameState.PLAYING


def test_pop_never_empties_stack():
    sm = StateManager()
    sm.pop()
    sm.pop()
    assert sm.current == GameState.MENU


def test_context_defaults():
    sm = StateManager()
    assert sm.context["level"] == 1
    assert sm.context["score"] == 0
