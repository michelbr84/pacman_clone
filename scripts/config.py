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

# Caminhos para os arquivos de imagem, som e fonte
ICON_PATH   = 'images/pacman.png'
MUSIC_PATH  = 'pacman.mp3'
FONT_PATH   = "freesansbold.ttf"
FONT_SIZE   = 24

# OBS.: É importante que o pygame seja inicializado (pygame.init()) antes de carregar imagens e sons.
# Se a inicialização ocorrer no main.py, certifique-se de importar este módulo após a chamada a pygame.init().

# Carrega o ícone do jogo e define-o como ícone da janela
TROLLICON = pygame.image.load(ICON_PATH)
pygame.display.set_icon(TROLLICON)

# Inicializa o mixer e carrega a música de fundo, fazendo-a tocar em loop
pygame.mixer.init()
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.play(-1, 0.0)

# Inicializa a fonte padrão para o jogo
pygame.font.init()
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
