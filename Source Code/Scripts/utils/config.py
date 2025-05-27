import os
# Define color
SKY = (220, 245, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (57, 150, 82)
DARKGREEN = (4, 118, 39)
LIGHTGREEN = (143, 217, 119)

# Screen settings
WIDTH = 1920
HEIGHT = 1080
FPS = 60
TILE_SIZE = 64

GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

#가로 세로 땅의 크기
HEIGHT_SIZE = 11
WIDTH_SIZE = 20

#타일 오프셋
OFFSET_WIDTH = 5
OFFSET_HEIGHT = 4

#자동저장 간격
AUTO_SAVE_INTERVAL = 300
#불 생성에 사용되는 클래스
class Fire:
    def __init__(self,x,y,tick):
        self.x = x
        self.y = y
        self.tick = tick

IGNITION_SEC = 1800 # 쓰레기에서 불로 점화하는데 걸리는 시간(초)
SPREAD_SEC = 600 # 불이 퍼지는데 걸리는 시간(초)

TRASH_TICK_INTERVAL = 300
SELECTED_TREE = None # 나무 심을 때, 선택된 나무 이름
SELECTED_TREE_INDEX = None # 선택된 나무 인덱스 (3~6)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

ASSET_DIR = os.path.join(ROOT_DIR, "assets")
IMG_DIR = os.path.join(ASSET_DIR, "images")
SFX_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
