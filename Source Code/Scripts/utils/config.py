import os
# Define color
SKY = (220, 245, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (57, 150, 82)
LIGHTGREEN = (143, 217, 119)

# Screen settings
WIDTH = 1920
HEIGHT = 1080
FPS = 60
TILE_SIZE = 64

GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

TRASH_TICK_INTERVAL = 100
SELECTED_TREE = None # 나무 심을 때, 선택된 나무 이름

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

ASSET_DIR = os.path.join(ROOT_DIR, "assets")
IMG_DIR = os.path.join(ASSET_DIR, "images")
SFX_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
