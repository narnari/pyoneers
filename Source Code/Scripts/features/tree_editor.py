# tree_plot_plant.py
import pygame
from Scripts.features import tilemap_drawer
from Scripts.screens import game_screen
from Scripts.utils import assets, config

planting_mode = False

EDITING_TEXT = None

def plant_tree(tile_map, tile_objects, mouse_pos, tile_size, selected_tree_index):
    """ 실제 나무를 심는 함수 """
    global planting_mode
    if not planting_mode:
        return

    col = mouse_pos[0] // tile_size
    row = mouse_pos[1] // tile_size

    if 4 <= row < config.GRID_HEIGHT-1 and 5 <= col < config.GRID_WIDTH-5: # 타일 열려있고, 오브젝트 없으면
        if tile_map[row][col] and tile_objects[row][col] == 0:
            tile_objects[row][col] = selected_tree_index + 3
            planting_mode = False


# 나무 심는 모드 인지 화면에 그림
def draw_editing_text(screen):
    global EDITING_TEXT
    if not planting_mode:
        return

    # pygame 초기화 이후에 폰트 로딩
    if EDITING_TEXT is None:
        EDITING_TEXT = assets.load_font("Jalnan.ttf", 38)

    text = EDITING_TEXT.render("나무 심는 중!", True, config.BLACK)
    screen.blit(text, (1680, 1000))

# 흐릿한 이미지 만들기
def get_transparent_image(image, alpha=120):
    transparent = image.copy()
    transparent.set_alpha(alpha)
    return transparent

# 마우스 따라다니는 나무 미리보기
def draw_tree_preview(screen):
    if not planting_mode or config.SELECTED_TREE_INDEX is None:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()

    try:
        # 기존 tiles 딕셔너리 키는 "tile_tree1" ~ "tile_tree4"
        key = f"tile_tree{config.SELECTED_TREE_INDEX + 1}"
        tile_image = tilemap_drawer.tiles[key]

        preview_img = get_transparent_image(tile_image, alpha=150)
        screen.blit(preview_img, preview_img.get_rect(center=(mouse_x, mouse_y)))
    except KeyError:
        pass  # 이미지 없으면 안 그림
