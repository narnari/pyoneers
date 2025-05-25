import pygame, sys, ctypes
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor, tree_editor, fire_editor
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()
"""
tile_objects는 오브젝트 그리는거 전용으로 하는 배열
1 : 쓰레기
2 : 불
3~6 : 나무 1~4
"""
tiles = {}
tile_map = [[False for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
tick = 0
tile_objects = [[0 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
t_to_f = []     #trash to fire: 쓰레기에서 불로 발화하기 위해 사용. 쓰레기 생성 시 x좌표, y좌표, 생성시간을 Fire 클래스로 append.
fspread = []    #fire spread: 불이 주변으로 번지게 하기 위해 사용. 불 생성시시 x좌표, y좌표, 생성 시간을 Fire 클래스로 append.

# --- 중앙 3x3 타일만 선명하게 설정 ---
center_x = config.GRID_WIDTH // 2
center_y = config.GRID_HEIGHT // 2
for row in range(center_y, center_y + 3):
    for col in range(center_x - 1, center_x + 2):
        tile_map[row][col] = True

initialized = None
def load_assets():
    global tiles, UIs, initialized
    if not initialized:
        tiles = {
            "tile": assets.load_image("Tile04.png", (64, 64)),
            "fire": assets.load_image("fire01.png",(64,64)),
            "tile_tree1": assets.load_image("Tree1Plant.png",(64, 64)),
            "tile_tree2": assets.load_image("Tree2Plant.png", (64, 64)),
            "tile_tree3": assets.load_image("Tree3Plant.png", (64, 64)),
            "tile_tree4": assets.load_image("Tree4Plant.png", (64, 64)),
            "trash": assets.load_image("trash03.png", (64, 64)),
        }

def get_transparent_tile(tile, alpha):
    copy_tile = tile.copy()
    copy_tile.set_alpha(alpha)
    return copy_tile


def draw_tilemap(screen):
    faded_tile = get_transparent_tile(tiles["tile"], 100)
    for row in range(4, config.GRID_HEIGHT - 1):
        for col in range(5, config.GRID_WIDTH - 5):
            x = col * config.TILE_SIZE
            y = row * config.TILE_SIZE
            tile = tiles["tile"] if tile_map[row][col] else faded_tile
            screen.blit(tile, (x, y))

    global tick, trash_count
    tick, trash_editor.trash_count = trash_editor.generate_trash(tick, tile_objects, tile_map, trash_editor.trash_count, t_to_f)
    fire_editor.control_fire(t_to_f, fspread, tile_objects, tile_map)


def draw_tile_objects(screen, tile_objects, tiles):
    for row in range(4, config.GRID_HEIGHT-1):
        for col in range(5, config.GRID_WIDTH-5):
            obj = tile_objects[row][col]
            if obj == 0:
                continue
            x = col * config.TILE_SIZE
            y = row * config.TILE_SIZE
            if obj == 1:
                screen.blit(tiles["trash"], (x, y))
            elif obj == 2:
                screen.blit(tiles["fire"], (x, y))
            elif 3 <= obj <= 6:
                screen.blit(tiles[f"tile_tree{obj - 2}"], (x, y))
