# Assets TODO

Drop real WAV files into `assets/sfx/` with these exact names:

- chomp.wav       — pellet eat (fires every tick while munching)
- power.wav       — power pellet pickup
- death.wav       — Pacman dies
- eat_ghost.wav   — Pacman eats a frightened ghost
- menu_move.wav   — menu navigation (reserved)
- menu_select.wav — menu confirmation (reserved)

Missing files are handled gracefully: `scripts/audio.py::load` skips any that
are absent, so the game runs silently until assets are provided.

Volumes are controlled by the in-game Settings screen (persisted to
`savegame/settings.json`).
