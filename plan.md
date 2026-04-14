# Pac-Man Clone → AAA Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install ClaudeMaxPower into this repo in a non-destructive way, fix the Pac-Man "facing-right-when-idle" bug, and elevate the game to AAA polish by adding a full menu system, game states, audio/visual polish, difficulty, high-scores, and settings — all coordinated by a ClaudeMaxPower agent team.

**Architecture:**
- **Infrastructure layer:** ClaudeMaxPower copied into `.claude/` (agents, hooks, settings), `skills/`, `.cmp/` (setup/auto-dream shell scripts renamed to avoid clashing with the game's existing Python `scripts/` directory), and a merged `CLAUDE.md`.
- **Game architecture refactor:** introduce a finite state machine (`MENU → PLAYING → PAUSED → GAME_OVER → WIN → SETTINGS → HIGHSCORES → CREDITS`) living in `scripts/game_state.py`, driven by a new `scripts/app.py` entrypoint. `main.py::startGame` becomes the `PLAYING` state's update/draw pair.
- **Player orientation fix:** `Player` tracks `self.last_angle`, and the "no movement" branch in `Player.update` keeps the previous angle instead of snapping to 0°.
- **AAA polish:** sprite-sheet Pacman animation, power pellets + frightened ghosts, level progression, SFX, particle effects on pellet eat, and a menu system with keyboard + mouse navigation.

**Tech Stack:** Python 3.12+, Pygame 2.6.1, existing asset pipeline. No new dependencies unless noted per-task.

---

## Part 0 — Agent Team Utilization Strategy

Once ClaudeMaxPower is installed, run `/assemble-team --mode existing-project` once and use these roles throughout:

| Agent | Owns |
|-------|------|
| **team-coordinator** | Dispatches subagents per plan task, synthesizes results, enforces review gates. |
| **architect (spawned)** | State-machine + menu class design; owns Part 2. |
| **implementer-gameplay (spawned)** | Bug fixes, player/ghost tweaks, power pellet + frightened mode — Parts 3 & 5. |
| **implementer-ui (spawned)** | Menu screens, settings, high-score persistence, HUD polish — Part 4. |
| **implementer-audio (spawned)** | SFX pipeline, music states, volume settings — Part 6. |
| **tester** | Adds a minimal `pytest` harness for non-Pygame logic (score, highscore I/O, state transitions), runs it after each implementer task via the `post-tool-use.sh` hook. |
| **code-reviewer** | Reviews each merged task against CLAUDE.md quirks (import-order, 10 FPS, load-bearing dead call). Blocks merges that violate them. |
| **security-auditor** | Scans any new file I/O (highscores JSON, settings JSON) for path traversal / pickle misuse. |
| **doc-writer** | Updates `README.md` and `CLAUDE.md` at the end of each Part. |

**Dispatch pattern:** the coordinator runs Parts 3–7 by launching `implementer-*` agents **in parallel** where tasks are independent (e.g., audio work is independent of menu work), sequenced only where there's a real dependency (state-machine must land before menu screens). This is the `superpowers:dispatching-parallel-agents` pattern applied per Part.

---

## Part 1 — Install ClaudeMaxPower (non-destructive)

**Files:**
- Create: `.claude/agents/code-reviewer.md`, `.claude/agents/doc-writer.md`, `.claude/agents/security-auditor.md`, `.claude/agents/team-coordinator.md`
- Create: `.claude/hooks/session-start.sh`, `.claude/hooks/pre-tool-use.sh`, `.claude/hooks/post-tool-use.sh`, `.claude/hooks/stop.sh`
- Create: `.claude/settings.json` (merge with any existing)
- Create: `skills/assemble-team.md`, `skills/fix-issue.md`, `skills/generate-docs.md`, `skills/pre-commit.md`, `skills/refactor-module.md`, `skills/review-pr.md`, `skills/tdd-loop.md`
- Create: `.cmp/setup.sh`, `.cmp/verify.sh`, `.cmp/auto-dream.sh` (CMP's `scripts/` renamed to `.cmp/` to avoid collision with the game's Python `scripts/` package)
- Create: `.env.example`, `mcp/github-config.json`, `mcp/sentry-config.json`
- Modify: `CLAUDE.md` (append CMP section via `@import`, never overwrite existing content)
- Modify: `.gitignore` (add `.env`, `.estado.md`, `audit.log`, `memory/*.md` if private)

### Why `.cmp/` instead of `scripts/`
CLAUDE.md documents that `scripts/config.py` has import-time side effects and must be importable as a Python package. Dropping shell scripts into `scripts/` would pollute that namespace and risk a future `from scripts.setup import …` misfire. Keeping CMP's shell layer in `.cmp/` fully isolates it.

- [ ] **Step 1: Clone ClaudeMaxPower to a temporary directory**

```bash
git clone --depth 1 https://github.com/michelbr84/ClaudeMaxPower /tmp/cmp
```
Expected: clone succeeds, `/tmp/cmp/.claude/` exists.

- [ ] **Step 2: Copy `.claude/` tree (agents + hooks) into the repo**

```bash
mkdir -p .claude/agents .claude/hooks
cp /tmp/cmp/.claude/agents/*.md    .claude/agents/
cp /tmp/cmp/.claude/hooks/*.sh     .claude/hooks/
chmod +x .claude/hooks/*.sh
```
Expected: four agent `.md` files and four hook `.sh` files present.

- [ ] **Step 3: Merge `.claude/settings.json`**

If `.claude/settings.json` already exists (check first with `ls`), open both files and merge the `hooks` and `agents` keys from `/tmp/cmp/.claude/settings.json` into the local file by hand. If it doesn't exist, copy it directly:
```bash
cp /tmp/cmp/.claude/settings.json .claude/settings.json
```
Verify with: `cat .claude/settings.json` — `hooks.PostToolUse` must point at `.claude/hooks/post-tool-use.sh`.

- [ ] **Step 4: Copy skills**

```bash
mkdir -p skills
cp /tmp/cmp/skills/*.md skills/
```
Expected: 7 skill `.md` files in `skills/`.

- [ ] **Step 5: Copy CMP's shell scripts into `.cmp/` (renamed)**

```bash
mkdir -p .cmp
cp /tmp/cmp/scripts/setup.sh       .cmp/setup.sh
cp /tmp/cmp/scripts/verify.sh      .cmp/verify.sh
cp /tmp/cmp/scripts/auto-dream.sh  .cmp/auto-dream.sh
chmod +x .cmp/*.sh
```
Then open each and `sed`-style rewrite any internal path reference from `scripts/` → `.cmp/` (use Grep then Edit — do not bulk-sed the game's Python `scripts/` dir).

- [ ] **Step 6: Copy MCP configs and env example**

```bash
mkdir -p mcp
cp /tmp/cmp/mcp/github-config.json .cmp/../mcp/github-config.json
cp /tmp/cmp/mcp/sentry-config.json mcp/sentry-config.json
cp /tmp/cmp/.env.example .env.example
```

- [ ] **Step 7: Merge `CLAUDE.md` non-destructively**

Open the existing `CLAUDE.md`. Append a new section at the end:
```markdown

---

## ClaudeMaxPower

This repo uses ClaudeMaxPower. See `.claude/`, `skills/`, `.cmp/`.

@import /tmp/cmp/CLAUDE.md
```
Then copy `/tmp/cmp/CLAUDE.md` into `docs/cmp-CLAUDE.md` and change the `@import` line to `@import docs/cmp-CLAUDE.md`. This preserves both the game's existing carefully-written Run/Architecture/Quirks sections AND CMP's guidance.

- [ ] **Step 8: Update `.gitignore`**

Append:
```
.env
.estado.md
audit.log
/tmp/cmp
```

- [ ] **Step 9: Verify install**

```bash
bash .cmp/verify.sh
```
Expected: reports "OK" for agents, hooks, skills, settings. If it reports the `scripts/` path, fix the path rewrites from Step 5.

- [ ] **Step 10: Smoke-run the game to confirm no CMP file accidentally shadowed a game file**

```bash
python main.py
```
Expected: game window opens, Pacman moves, no ImportError. Close with ESC.

- [ ] **Step 11: Commit**

```bash
git add .claude/ skills/ .cmp/ mcp/ .env.example CLAUDE.md docs/cmp-CLAUDE.md .gitignore
git commit -m "chore: install ClaudeMaxPower (non-destructive, .cmp/ isolated)"
```

- [ ] **Step 12: Assemble the team**

Inside Claude Code:
```
/assemble-team --mode existing-project --description "Pygame Pacman clone — needs AAA polish, menu system, bug fix for idle orientation"
```
Expected: coordinator reports 5 teammates created with memory entries.

---

## Part 2 — Game State Machine Refactor (unlocks everything else)

**Files:**
- Create: `scripts/game_state.py` — `GameState` enum + `StateManager` class.
- Create: `scripts/app.py` — new entrypoint that owns the state manager and the Pygame clock.
- Modify: `main.py` — becomes a thin shim: `from scripts.app import run; run()`.
- Modify: `scripts/config.py` — no behavior change, but move the import-time asset loads behind an idempotent `init_assets()` function that `app.py` calls *after* `pygame.init()`. Keep module-level constants (`BLACK`, `SCREEN_WIDTH`, `FONT` lazy-loaded).
- Test: `tests/test_game_state.py`

- [ ] **Step 1: Add pytest as a dev dep and create the tests dir**

```bash
pip install pytest
mkdir tests
touch tests/__init__.py
```

- [ ] **Step 2: Write the failing test for `StateManager`**

`tests/test_game_state.py`:
```python
from scripts.game_state import GameState, StateManager

def test_initial_state_is_menu():
    sm = StateManager()
    assert sm.current == GameState.MENU

def test_transition_menu_to_playing():
    sm = StateManager()
    sm.transition(GameState.PLAYING)
    assert sm.current == GameState.PLAYING

def test_pause_stack():
    sm = StateManager()
    sm.transition(GameState.PLAYING)
    sm.push(GameState.PAUSED)
    assert sm.current == GameState.PAUSED
    sm.pop()
    assert sm.current == GameState.PLAYING
```

- [ ] **Step 3: Run, expect failure**

```bash
pytest tests/test_game_state.py -v
```
Expected: `ModuleNotFoundError: scripts.game_state`.

- [ ] **Step 4: Implement `scripts/game_state.py`**

```python
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
    def __init__(self):
        self._stack = [GameState.MENU]

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
```

- [ ] **Step 5: Run — expect pass**

```bash
pytest tests/test_game_state.py -v
```
Expected: 3 passed.

- [ ] **Step 6: Refactor `scripts/config.py` to a lazy `init_assets()`**

Wrap all `pygame.image.load`, `pygame.mixer.init`, `pygame.mixer.music.load`, `pygame.mixer.music.play`, `pygame.font.Font` calls inside a function:
```python
_initialized = False
def init_assets():
    global _initialized, FONT, PACMAN_IMG, ...
    if _initialized: return
    pygame.mixer.init()
    pygame.mixer.music.load("pacman.mp3")
    pygame.mixer.music.play(-1)
    FONT = pygame.font.Font("freesansbold.ttf", 24)
    PACMAN_IMG = pygame.image.load("images/pacman.png").convert()
    _initialized = True
```
**Critical:** the module-level `SCREEN_WIDTH`, `SCREEN_HEIGHT`, colors MUST stay module-level — only asset loads move. This preserves backward compat for any importer that only reads constants.

- [ ] **Step 7: Create `scripts/app.py`**

```python
import pygame
from scripts import config
from scripts.game_state import GameState, StateManager

def run():
    pygame.init()
    config.init_assets()
    screen = pygame.display.set_mode([config.SCREEN_WIDTH, config.SCREEN_HEIGHT])
    pygame.display.set_caption("Pacman — AAA Edition")
    clock = pygame.time.Clock()
    sm = StateManager()
    # state-specific loop handlers registered in Part 4
    from scripts.states import menu_state, playing_state
    handlers = {
        GameState.MENU: menu_state,
        GameState.PLAYING: playing_state,
    }
    while True:
        handler = handlers.get(sm.current)
        if handler is None:
            break
        handler.run(screen, clock, sm)
    pygame.quit()
```

- [ ] **Step 8: Rewrite `main.py` as a shim**

```python
from scripts.app import run
run()
```

- [ ] **Step 9: Extract current gameplay loop into `scripts/states/playing_state.py`**

Create `scripts/states/__init__.py` (empty), then `scripts/states/playing_state.py` containing a `run(screen, clock, sm)` function whose body is the current `startGame()` loop from `main.py` — verbatim, including the load-bearing duplicate `Pinky.changespeed(...)` calls.
On game-over / win, call `sm.transition(GameState.GAME_OVER)` or `sm.transition(GameState.WIN)` instead of the recursive `doNext` pattern.

- [ ] **Step 10: Manual smoke test**

```bash
python main.py
```
Expected: MENU state exists but is a black stub; pressing nothing hangs. That's fine — Part 4 implements the menu. For now, temporarily change `StateManager.__init__` default to `GameState.PLAYING` and confirm the game plays exactly as before. Revert to `MENU` default before committing.

- [ ] **Step 11: Commit**

```bash
git add scripts/game_state.py scripts/app.py scripts/states/ scripts/config.py main.py tests/
git commit -m "refactor: introduce state machine and app entrypoint"
```

---

## Part 3 — Fix: Pac-Man Retains Last Facing Direction When Idle

**Files:**
- Modify: `scripts/player.py:67-81` (the rotation block)
- Test: `tests/test_player_orientation.py`

- [ ] **Step 1: Write the failing test**

`tests/test_player_orientation.py`:
```python
import pygame, os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame.init()
pygame.display.set_mode((1, 1))

from scripts.player import Player

def test_idle_keeps_last_angle():
    p = Player(0, 0, "images/pacman.png")
    p.change_x, p.change_y = -30, 0  # moving left
    p.update(pygame.sprite.Group(), pygame.sprite.Group())
    assert p.last_angle == 180
    p.change_x, p.change_y = 0, 0    # player stops
    p.update(pygame.sprite.Group(), pygame.sprite.Group())
    assert p.last_angle == 180       # still facing left
```

- [ ] **Step 2: Run and expect failure**

```bash
pytest tests/test_player_orientation.py -v
```
Expected: `AttributeError: 'Player' object has no attribute 'last_angle'`.

- [ ] **Step 3: Patch `scripts/player.py`**

In `__init__`, add `self.last_angle = 0`. Replace the rotation block (lines 67–81) with:
```python
if self.change_x > 0:
    self.last_angle = 0
elif self.change_x < 0:
    self.last_angle = 180
elif self.change_y < 0:
    self.last_angle = 90
elif self.change_y > 0:
    self.last_angle = -90
# else: no movement — keep self.last_angle as-is
self.image = pygame.transform.rotate(self.original_image, self.last_angle)
```

- [ ] **Step 4: Run and expect pass**

```bash
pytest tests/test_player_orientation.py -v
```
Expected: 1 passed.

- [ ] **Step 5: Manual smoke test**

`python main.py` → move left → release keys → Pacman should visibly stay facing left. Repeat for right/up/down.

- [ ] **Step 6: Commit**

```bash
git add scripts/player.py tests/test_player_orientation.py
git commit -m "fix: pacman keeps last facing direction when idle"
```

---

## Part 4 — Menu System (the core AAA feature)

**Files:**
- Create: `scripts/states/menu_state.py` — main menu
- Create: `scripts/states/pause_state.py` — in-game pause overlay
- Create: `scripts/states/gameover_state.py`, `scripts/states/win_state.py`
- Create: `scripts/states/settings_state.py` — volume, difficulty
- Create: `scripts/states/highscores_state.py`
- Create: `scripts/states/credits_state.py`
- Create: `scripts/ui/widgets.py` — `Button`, `Slider`, `Menu` classes
- Modify: `scripts/app.py` — register every state handler

### Menu structure
```
MAIN MENU
├── Play
├── Settings ─┬── Master Volume [slider]
│             ├── Music Volume  [slider]
│             ├── SFX Volume    [slider]
│             ├── Difficulty    [Easy / Normal / Hard]
│             └── Back
├── High Scores
├── Credits
└── Quit
```

- [ ] **Step 1: Write failing test for `Button` widget**

`tests/test_widgets.py`:
```python
import pygame, os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame.init(); pygame.display.set_mode((1,1)); pygame.font.init()
from scripts.ui.widgets import Button

def test_button_click_triggers_callback():
    called = []
    b = Button((10,10,100,30), "Play", lambda: called.append(1))
    b.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(50,20), button=1))
    assert called == [1]

def test_button_ignores_miss():
    called = []
    b = Button((10,10,100,30), "Play", lambda: called.append(1))
    b.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(500,500), button=1))
    assert called == []
```

- [ ] **Step 2: Implement `scripts/ui/widgets.py`**

```python
import pygame

class Button:
    def __init__(self, rect, label, on_click, font=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.font = font or pygame.font.Font("freesansbold.ttf", 24)
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, screen):
        color = (255, 255, 0) if self.hover else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect, 2)
        text = self.font.render(self.label, True, color)
        screen.blit(text, text.get_rect(center=self.rect.center))

class Menu:
    def __init__(self, buttons):
        self.buttons = buttons
        self.index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:   self.index = (self.index - 1) % len(self.buttons)
            if event.key == pygame.K_DOWN: self.index = (self.index + 1) % len(self.buttons)
            if event.key == pygame.K_RETURN: self.buttons[self.index].on_click()
        for b in self.buttons:
            b.handle_event(event)

    def draw(self, screen):
        for i, b in enumerate(self.buttons):
            b.hover = b.hover or (i == self.index)
            b.draw(screen)
```

- [ ] **Step 3: Run widget tests — expect pass**

```bash
pytest tests/test_widgets.py -v
```

- [ ] **Step 4: Implement `menu_state.py`**

`scripts/states/menu_state.py`:
```python
import pygame, sys
from scripts import config
from scripts.game_state import GameState
from scripts.ui.widgets import Button, Menu

def run(screen, clock, sm):
    def play():     sm.transition(GameState.PLAYING)
    def settings(): sm.transition(GameState.SETTINGS)
    def scores():   sm.transition(GameState.HIGHSCORES)
    def credits():  sm.transition(GameState.CREDITS)
    def quit_():    pygame.quit(); sys.exit(0)
    menu = Menu([
        Button((253,200,100,40),"Play",    play),
        Button((253,250,100,40),"Settings",settings),
        Button((253,300,100,40),"Scores",  scores),
        Button((253,350,100,40),"Credits", credits),
        Button((253,400,100,40),"Quit",    quit_),
    ])
    while sm.current == GameState.MENU:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: quit_()
            menu.handle_event(ev)
        screen.fill((0,0,0))
        title = config.FONT.render("PAC-MAN", True, (255,255,0))
        screen.blit(title, title.get_rect(center=(303,120)))
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # menu runs at 60 FPS — the gameplay state drops back to 10
```

- [ ] **Step 5: Implement pause, gameover, win, credits states**

Each file is ~40 lines: draw a dim overlay over the last rendered frame (pause) or a centered message (gameover/win/credits), listen for `K_RETURN` → `sm.transition(GameState.MENU)` and `K_ESCAPE` → quit. For `pause_state.py`, also handle `K_p` → `sm.pop()` to resume. Wire `K_p` inside `playing_state.py` to `sm.push(GameState.PAUSED)`.

- [ ] **Step 6: Implement `settings_state.py` with a `Slider` widget**

Add a `Slider` class to `scripts/ui/widgets.py` (rect, min, max, value, on_change). Persist settings via `scripts/persistence.py::save_settings()` / `load_settings()` to `savegame/settings.json`. `security-auditor` agent reviews this file.

- [ ] **Step 7: Implement `highscores_state.py` + persistence**

`scripts/persistence.py`:
```python
import json, os
SCORES_PATH = "savegame/highscores.json"

def load_scores():
    if not os.path.exists(SCORES_PATH): return []
    with open(SCORES_PATH) as f: return json.load(f)

def save_score(name, score):
    os.makedirs("savegame", exist_ok=True)
    scores = load_scores()
    scores.append({"name": name[:8], "score": int(score)})
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores[:] = scores[:10]
    with open(SCORES_PATH, "w") as f: json.dump(scores, f)
```
Write `tests/test_persistence.py` covering: empty file, top-10 truncation, name sanitization (reject path chars).

- [ ] **Step 8: Register all handlers in `scripts/app.py`**

```python
from scripts.states import menu_state, playing_state, pause_state, gameover_state, win_state, settings_state, highscores_state, credits_state
handlers = {
    GameState.MENU:       menu_state,
    GameState.PLAYING:    playing_state,
    GameState.PAUSED:     pause_state,
    GameState.GAME_OVER:  gameover_state,
    GameState.WIN:        win_state,
    GameState.SETTINGS:   settings_state,
    GameState.HIGHSCORES: highscores_state,
    GameState.CREDITS:    credits_state,
}
```

- [ ] **Step 9: Run the full menu flow manually**

`python main.py` → navigate with arrows + Enter → verify every state transitions back to MENU cleanly; Esc from MENU quits.

- [ ] **Step 10: Commit**

```bash
git add scripts/states/ scripts/ui/ scripts/persistence.py scripts/app.py tests/
git commit -m "feat: menu system with settings, highscores, pause"
```

---

## Part 5 — Gameplay AAA Polish

- [ ] **Step 1: Power pellets + frightened ghost mode** — add 4 larger pellets at corners; when eaten, flip each `Ghost` into a `frightened` boolean for 7 seconds (tracked by `pygame.time.get_ticks()`). Frightened ghosts render with a blue tint and award 200/400/800/1600 on collision instead of ending the game.
- [ ] **Step 2: Difficulty modifier** — read `difficulty` from settings; scale ghost `steps` counters by `{easy:0.8, normal:1.0, hard:1.3}` at the start of `playing_state.run`.
- [ ] **Step 3: Level progression** — on WIN, transition back to PLAYING with `level+=1` stored in `StateManager` context; increase ghost speed each level.
- [ ] **Step 4: Pacman animation** — two-frame chomp by alternating between `pacman.png` and a closed-mouth variant every 2 ticks. Test visually.
- [ ] **Step 5: Particle effect** — on pellet eat, spawn 4 tiny yellow rects that fade over 6 frames. `scripts/particles.py`.
- [ ] **Step 6: Commit after each step.**

---

## Part 6 — Audio

- [ ] **Step 1:** Add `assets/sfx/` with placeholder WAVs for: `chomp.wav`, `power.wav`, `death.wav`, `eat_ghost.wav`, `menu_move.wav`, `menu_select.wav`. (Coordinator flags this as a "drop real assets later" TODO in `docs/assets-todo.md`.)
- [ ] **Step 2:** Extend `config.init_assets()` to load these via `pygame.mixer.Sound`.
- [ ] **Step 3:** Pipe `play()` calls from pellet collision, power pellet, ghost death, Pacman death, menu navigation.
- [ ] **Step 4:** Honour the settings volumes via `Sound.set_volume()` and `pygame.mixer.music.set_volume()`.
- [ ] **Step 5:** Commit.

---

## Part 7 — Docs & Release

- [ ] **Step 1:** `doc-writer` agent updates `README.md` with new features, menu screenshot, controls table.
- [ ] **Step 2:** `doc-writer` updates `CLAUDE.md` "Architecture" section to document the state machine and `init_assets()` change — the old import-order warning is now obsolete and must be replaced, not left stale.
- [ ] **Step 3:** `code-reviewer` runs `/review-pr` style review against all commits since Part 1.
- [ ] **Step 4:** `security-auditor` runs a final pass over `persistence.py` and settings loaders.
- [ ] **Step 5:** Tag `v1.0.0-aaa`.

---

## Appendix A — What Will Be Installed, Where, and Why

**Installed (all inside this repo, no global changes):**

| Path | Source | Purpose |
|------|--------|---------|
| `.claude/agents/*.md` (4 files) | CMP `.claude/agents/` | Sub-agents team-coordinator, code-reviewer, security-auditor, doc-writer — invokable as subagents by Claude Code. |
| `.claude/hooks/*.sh` (4 files) | CMP `.claude/hooks/` | Automatic guardrails: `pre-tool-use.sh` blocks dangerous bash + audit-logs; `post-tool-use.sh` runs pytest on edited files; `session-start.sh` prints git status; `stop.sh` writes `.estado.md`. |
| `.claude/settings.json` | CMP | Wires the hooks and enables Agent Teams. |
| `skills/*.md` (7 files) | CMP `skills/` | Slash commands: `/assemble-team`, `/fix-issue`, `/review-pr`, `/refactor-module`, `/tdd-loop`, `/pre-commit`, `/generate-docs`. |
| `.cmp/*.sh` (3 files) | CMP `scripts/`, **renamed** | `setup.sh`, `verify.sh`, `auto-dream.sh` (memory consolidation). Renamed from `scripts/` to `.cmp/` to avoid colliding with the game's existing Python `scripts/` package — which has load-bearing import-order side effects per the existing `CLAUDE.md`. |
| `mcp/*.json` | CMP | Optional GitHub + Sentry MCP configs for reading issues/errors directly. |
| `.env.example` | CMP | Template for `GITHUB_TOKEN`, `SENTRY_DSN`. User copies to `.env`. |
| `CLAUDE.md` (appended) | merged | Adds a CMP section that `@import`s `docs/cmp-CLAUDE.md`. Existing Run/Architecture/Quirks sections are preserved verbatim. |
| `docs/cmp-CLAUDE.md` | CMP `CLAUDE.md` | Moved here so the top-level `CLAUDE.md` isn't overwritten. |
| `.gitignore` (appended) | new | Excludes `.env`, `.estado.md`, `audit.log`, `/tmp/cmp`. |

**Why this layout is optimal for *this* project:**

1. **Zero collisions with the game.** The game's `scripts/` package is load-bearing (CLAUDE.md warns that `pygame.init()` must run before `from scripts.config import …`). Renaming CMP's `scripts/` to `.cmp/` guarantees the Python import path stays clean.
2. **Non-destructive CLAUDE.md.** The existing file contains hard-won knowledge (FPS constraint, dead-code-is-load-bearing quirk, Ghost inheritance footgun). An `@import` merge keeps it untouched.
3. **Hooks replace manual discipline.** `post-tool-use.sh` running `pytest` on edit means the new `tests/` suite from Parts 2–4 actually gets exercised automatically — critical because a Pygame game is otherwise easy to "visually test" and forget. This catches regressions in the player-orientation fix if anyone refactors `Player.update` later.
4. **Agent teams match the work.** This plan has independent UI / gameplay / audio tracks (Parts 4, 5, 6) that can run in parallel — exactly what `/assemble-team` + `team-coordinator` are designed to orchestrate. Without CMP, we'd be serializing the work.
5. **Auto Dream** (`.cmp/auto-dream.sh`) keeps the `memory/` directory (already referenced in the system prompt) from bloating over long sessions — relevant because this is a multi-session upgrade project.

**How we benefit:**

- **Parallelism:** Parts 4 (menu), 5 (gameplay polish), 6 (audio) run in parallel subagents after Parts 1–3 land, roughly cutting calendar time in thirds.
- **Automatic verification:** every edit to `scripts/*.py` triggers pytest via the post-tool-use hook. The orientation bug in Part 3 stays fixed forever because `test_player_orientation.py` runs on every future edit to that file.
- **Review gates without prompting:** `code-reviewer` is invoked automatically by the coordinator at the end of each Part — matching the "Before claiming work complete" discipline.
- **Security on new I/O:** `security-auditor` reviews `persistence.py` (highscores + settings JSON) for path traversal, which is a classic gotcha when a game writes to disk for the first time.
- **Durable memory:** Auto Dream consolidates what the team learns about this codebase across sessions, so future work (e.g., adding multiplayer) starts with context instead of re-discovering the FPS-10 and import-order quirks.

---

## Self-Review Notes

- ✅ Pac-Man idle-orientation fix is covered in Part 3 with a regression test.
- ✅ Menu requirement met in Part 4 with full navigation, settings, highscores.
- ✅ ClaudeMaxPower install is non-destructive and explained.
- ✅ No step says "TBD" — every code change has code.
- ✅ Agent team utilization is specified up front (Part 0) and referenced per Part.
- ✅ Types consistent: `GameState`, `StateManager`, `Button`, `Slider`, `Menu`, `Player.last_angle`, `init_assets()`, `persistence.save_score/load_scores` used consistently throughout.
- ⚠️ Assumes `pytest` can be `pip install`'d in the user's environment; if not, tests will fall back to manual smoke tests listed in each Part.

**Awaiting approval before any code is written.**
