# Pac-Man — AAA Edition

A Pygame-based Pac-Man clone upgraded with a full menu system, state machine, power pellets, frightened ghost mode, difficulty settings, persistent high scores, particles, and a modular audio pipeline. Engineered with [ClaudeMaxPower](https://github.com/michelbr84/ClaudeMaxPower) and the Claude Code superpowers skill suite.

## Features

- **Main menu** — Play / Settings / High Scores / Credits / Quit, keyboard- and mouse-navigable.
- **Settings** — Master / Music / SFX volume sliders, Easy / Normal / Hard difficulty. Persists to `savegame/settings.json`.
- **High scores** — Top-10 persisted to `savegame/highscores.json`, path-traversal-safe name sanitisation.
- **Pause** — Press `P` in-game to pause with a dimmed overlay.
- **Power pellets** — Four white pellets at the maze corners. Eating one turns ghosts blue for 7s; bump them to score 200 each and send them back to the ghost house.
- **Level progression** — Winning a level bumps the level counter; press Enter to replay.
- **Difficulty speed scaling** — Easy = 0.8×, Normal = 1.0×, Hard = 1.3× ghost speed.
- **Chomp animation** — Pacman's mouth opens/closes while moving; the last facing direction is preserved when idle (previously snapped back to facing right).
- **Particles** — Tiny bursts on pellet eat and power-up pickup.
- **Audio** — Drop `.wav` files into `assets/sfx/` (see `docs/assets-todo.md`). Missing files are gracefully skipped.

## Requirements

- Python 3.12+
- Pygame 2.6.1+
- `pytest` (for running the test suite; optional for just playing)

```bash
pip install pygame pytest
```

## Run

From the repository root:

```bash
python main.py
```

The game **must** be launched from the repo root — `scripts/config.py` loads assets with relative paths.

## Controls

| Key | Action |
|-----|--------|
| Arrow keys | Move Pacman / navigate menus |
| Enter | Confirm / select |
| P | Pause in-game |
| Esc | Back to menu / quit |
| Mouse | Click any menu button or drag sliders |

## Project Structure

```
pacman_clone/
├── main.py                    # Thin shim: from scripts.app import run; run()
├── scripts/
│   ├── app.py                 # Pygame init + state-machine loop
│   ├── game_state.py          # GameState enum + StateManager (stack-based)
│   ├── config.py              # Colors, dimensions, lazy init_assets()
│   ├── persistence.py         # settings + highscores JSON I/O (sanitised)
│   ├── audio.py               # SFX loader + volume plumbing
│   ├── particles.py           # Lightweight particle system
│   ├── player.py              # Pacman (now keeps last facing direction when idle)
│   ├── ghost.py               # Ghost (scripted AI) + frightened mode
│   ├── maze.py, block.py, directions.py
│   ├── states/                # One module per GameState
│   │   ├── menu_state.py
│   │   ├── playing_state.py
│   │   ├── pause_state.py
│   │   ├── gameover_state.py
│   │   ├── win_state.py
│   │   ├── settings_state.py
│   │   ├── highscores_state.py
│   │   └── credits_state.py
│   └── ui/widgets.py          # Button, Slider, Toggle, Menu
├── tests/                     # pytest suite (state machine, player, persistence)
├── .claude/                   # ClaudeMaxPower agents + hooks + settings
├── skills/                    # ClaudeMaxPower slash commands
├── .cmp/                      # ClaudeMaxPower shell scripts (renamed from scripts/)
├── mcp/                       # Optional GitHub + Sentry MCP configs
├── docs/                      # cmp-CLAUDE.md, assets-todo.md
├── plan.md                    # Full implementation plan executed to build this edition
├── images/, pacman.mp3, freesansbold.ttf
└── savegame/                  # Created at runtime — settings + highscores
```

## Testing

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest tests/ -v
```

17 tests cover state transitions, the Pacman idle-orientation regression, and persistence I/O (including corrupt-file handling and name sanitisation).

## ClaudeMaxPower

This project is instrumented with ClaudeMaxPower so Claude Code acts as a coordinated AI engineering team. See `CLAUDE.md` and `docs/cmp-CLAUDE.md`.

## Contributing

Fork, branch, run the tests, open a PR. Contributions welcome.
