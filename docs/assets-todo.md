# Audio assets

SFX files live in `assets/sfx/`. Supported formats (first match wins per name): `.mp3`, `.wav`, `.ogg`.

Required filenames:

- `chomp`       — pellet eat (fires every tick while munching)
- `power`       — power pellet pickup
- `death`       — Pacman dies
- `eat_ghost`   — Pacman eats a frightened ghost
- `menu_move`   — menu navigation (reserved)
- `menu_select` — menu confirmation (reserved)

Currently shipped as `.mp3`. Missing files are handled gracefully — `scripts/audio.py::load` skips any that are absent, so the game runs silently for that channel.

Volumes are controlled by the in-game Settings screen (persisted to `savegame/settings.json`).
