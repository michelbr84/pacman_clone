# config.py
import pygame

# Cores
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
BLUE    = (0, 0, 255)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
PURPLE  = (255, 0, 255)
YELLOW  = (255, 255, 0)

# Dimensões da tela
SCREEN_WIDTH  = 606
SCREEN_HEIGHT = 606

ICON_PATH   = 'images/pacman.png'
MUSIC_PATH  = 'pacman.mp3'
FONT_PATH   = "freesansbold.ttf"
FONT_SIZE   = 24

# Lazy-loaded assets — populated by init_assets() after pygame.init().
FONT = None
TROLLICON = None
_initialized = False


def init_assets():
    """Load icon, music and font. Idempotent. Must be called after pygame.init()."""
    global _initialized, FONT, TROLLICON
    if _initialized:
        return
    TROLLICON = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(TROLLICON)

    pygame.mixer.init()
    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1, 0.0)
    except pygame.error:
        pass  # music is non-essential

    pygame.font.init()
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
    _initialized = True
