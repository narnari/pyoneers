import pygame, sys, ctypes
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor, tree_editor, fire_editor, save_editor
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()
"""
tile_objects는 오브젝트 그리는거 전용으로 하는 배열
1 : 쓰레기
2 : 불
3~6 : 나무 1~4
"""
tiles = {}
tile_map = [[ 0 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
tick = 0
tile_objects = [[0 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
t_to_f = []     #trash to fire: 쓰레기에서 불로 발화하기 위해 사용. 쓰레기 생성 시 x좌표, y좌표, 생성시간을 Fire 클래스로 append.
fspread = []    #fire spread: 불이 주변으로 번지게 하기 위해 사용. 불 생성시시 x좌표, y좌표, 생성 시간을 Fire 클래스로 append.
#세이브 파일에서 땅 정보 불러올때 사용하는 상수
HOFF = config.OFFSET_HEIGHT
WOFF = config.OFFSET_WIDTH



#세이브 파일에서 돈, 산소, 땅 열림 유무, 오브젝트 ID 불러옴
map_temp, object_temp = save_editor.file_load_tile()
#땅 열림 유무 붙여넣기
for row in range(config.HEIGHT_SIZE):
    for col in range(config.WIDTH_SIZE):
        tile_map[row + HOFF][col + WOFF] = map_temp[row][col]

#오브젝트 ID 붙여넣기, 쓰레기나 불을 불러올 땐 따로 처리해줘야함
for row in range(config.HEIGHT_SIZE):
    for col in range(config.WIDTH_SIZE):
        if (object_temp[row][col] == 1):                                #쓰레기일 경우 카운트 올려주고, t_to_f에 어팬드
            trash_editor.trash_count = trash_editor.trash_on_load(trash_editor.trash_count, t_to_f, col + WOFF, row + HOFF)
        if (object_temp[row][col] == 2):                                #불일경우 fspread에 어팬드드
            fire_editor.fire_on_load(col+WOFF, row+HOFF, fspread, tile_map)
        tile_objects[row + HOFF][col + WOFF] = object_temp[row][col]    #나머진 걍 붙여넣어

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
