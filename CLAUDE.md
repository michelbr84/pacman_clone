# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Run

```bash
pip install pygame   # Python 3.12+, Pygame 2.6.1
python main.py
```

Run from the repo root — `scripts/config.py` loads assets with relative paths (`images/pacman.png`, `pacman.mp3`, `freesansbold.ttf`) at import time, so running from another directory crashes before `main.py` executes.

There is no build step, linter config, or test suite.

## Architecture

Single-process Pygame loop. Entry point is `main.py::startGame`, which owns the game state and is called recursively via `doNext` to restart after win/lose.

**Import-time side effects in `scripts/config.py`**: importing config triggers `pygame.image.load`, `pygame.mixer.init`, music playback, and font loading. This means `pygame.init()` in `main.py` must run *before* any `from scripts.config import ...` — reordering imports will break startup. Keep this constraint in mind when refactoring.

**Sprite hierarchy**: `Ghost(Player)` inherits from `Player` but overrides `changespeed` with a completely different signature — `Player.changespeed(dx, dy)` takes deltas from keyboard events, while `Ghost.changespeed(direction_list, ghost, turn, steps, max_turn)` advances through a scripted path. They are not interchangeable; don't treat `Ghost` as a drop-in `Player`.

**Ghost AI is scripted, not pathfinding**: each ghost follows a hard-coded sequence in `scripts/directions.py` (`Pinky_directions`, `Blinky_directions`, `Inky_directions`, `Clyde_directions`), with per-ghost max-turn values `pl`, `bl`, `il`, `cl`. Each direction entry is `[dx, dy, steps]`. The main loop tracks `(turn, steps)` per ghost and passes them back into `changespeed` every tick. Clyde has a special case: on wraparound, its `turn` resets to `2` instead of `0` (see `ghost.py:30`). Modifying ghost behavior means editing those lists, not writing new AI.

**Collision resolution in `Player.update`**: horizontal movement is applied and reverted on wall collision *before* vertical is even attempted, so diagonal glide along walls works but the order (horizontal-first) is load-bearing. The gate is checked separately and reverts *both* axes together.

**Maze + pellet layout**: `setupRoomOne` / `setupGate` in `scripts/maze.py` build the wall/gate sprite groups. Pellets are generated in `main.py` as a 19×19 grid with the ghost-house area (`row 7–8, col 8–10`) skipped, then filtered via `spritecollide` against walls and Pacman's starting rect. Grid cell size is 30px with a 26px offset — these magic numbers are tied to the screen size (606×606) and wall layout in `maze.py`; changing one requires changing the others.

**Game clock**: `clock.tick(10)` — the whole game runs at 10 FPS, which is why movement deltas are large (30px/tick). Don't raise the FPS without also scaling the speeds and the ghost direction-list step counts.

## Known quirks

- `main.py` calls `Pinky.changespeed(...)` twice per frame (once to capture the return, once ignored) for each ghost. This is not a bug in the sense of breaking gameplay, but the second call is dead code — preserve it if doing minimal edits, since removing it changes the `(turn, steps)` progression subtly.
- `doNext` calls `pygame.quit()` on ESC/QUIT but does not `return` or `sys.exit`, so the loop can keep running against a torn-down display. Matches upstream; don't "fix" casually.
- Comments and variable names in the scripts are in Portuguese; user-facing strings are in English.

---

## ClaudeMaxPower

This repo has ClaudeMaxPower installed non-destructively. Layout:
- `.claude/agents/` — team-coordinator, code-reviewer, security-auditor, doc-writer
- `.claude/hooks/` — session-start / pre-tool-use / post-tool-use / stop
- `.claude/settings.json` — hooks + agent-teams wiring
- `skills/` — /assemble-team, /fix-issue, /review-pr, /refactor-module, /tdd-loop, /pre-commit, /generate-docs
- `.cmp/` — CMP's shell scripts (setup.sh, verify.sh, auto-dream.sh), renamed from upstream `scripts/` to avoid clashing with this repo's Python `scripts/` package.
- `mcp/` — optional GitHub + Sentry MCP configs.
- `docs/cmp-CLAUDE.md` — upstream CMP CLAUDE.md, imported below.

@import docs/cmp-CLAUDE.md
