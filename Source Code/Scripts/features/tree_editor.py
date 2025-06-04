# tree_plot_plant.py
import pygame
from Scripts.screens import game_screen
from Scripts.features import tilemap_drawer, resource_manager
from Scripts.utils import assets, config
import time

planting_mode = False

EDITING_TEXT = None

def plant_tree(tile_map, tile_objects, mouse_pos, tile_size, selected_tree_index):
    """ 실제 나무를 심는 함수 """
    global planting_mode
    if not planting_mode:
        return

    col = mouse_pos[0] // tile_size
    row = mouse_pos[1] // tile_size
    tree_index = selected_tree_index + 3 # 실제 나무 인덱스 (3~6)
    resource_manager.check_resource(tile_objects) # 심기 전 tree_counts 갱신
    cost = resource_manager.get_tree_cost(tree_index)
    if 4 <= row < config.GRID_HEIGHT-1 and 5 <= col < config.GRID_WIDTH-5: # 타일 열려있고, 오브젝트 없으면
        if tile_map[row][col] and tile_objects[row][col] == 0:
            # 자원이 충분해야만 심기
            if not resource_manager.can_spend(money=cost):
                print("돈 부족! 나무 못 심음!")
                game_screen.State.show_no_tree_text = True
                game_screen.State.show_no_tree_time = time.time()
                planting_mode = False  # 심기 실패 시 모드 종료
                return

            # 심기 성공
            tile_objects[row][col] = tree_index 

            # 땅 구매 완료 출력용
            game_screen.State.show_success_tree_text = True
            game_screen.State.show_success_tree_time = time.time()

            resource_manager.check_resource(tile_objects)
            planting_mode = False  # 심기 후 모드 종료
            print(f"{resource_manager.get_tree_name(tree_index)} 심음! 비용 {cost}원 차감됨!")


# 나무 살살 돈 없음 화면에 출력
def draw_no_tree_text(screen):
    global EDITING_TEXT

    # pygame 초기화 이후에 폰트 로딩
    if EDITING_TEXT is None:
        EDITING_TEXT = assets.load_font("Jalnan.ttf", 38)

        # text = EDITING_TEXT.render(f"땅 구매 비용 {resource_manager.can_spend(cost)}원!", True, config.BLACK)
    text1 = EDITING_TEXT.render("돈 부족", True, config.BLACK)
    text2 = EDITING_TEXT.render("구매 불가능!", True, config.BLACK)
    screen.blit(text1, (100, 200))
    screen.blit(text2, (50, 240)) 
    return

# 나무 구매 완료 화면에 출력
def draw_success_tree_text(screen):
    global EDITING_TEXT
    if EDITING_TEXT is None:
        EDITING_TEXT = assets.load_font("Jalnan.ttf", 38)
    text = EDITING_TEXT.render("나무 구매 완료!", True, config.BLACK)
    screen.blit(text, (30, 240)) 



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

# 나무 업그레이드 팝업1 버전전에 뜨는 나무 정보 출력
def draw_popup_tree_info(screen, popup_pos, popup_type):
    col = popup_pos[0]//config.TILE_SIZE
    # 팝업 타입에 따라 좌표 달라짐
    if popup_type == "popup2":
        row = (popup_pos[1] - 392 + 330) // config.TILE_SIZE  # popup2는 아래로 내려갔으니 역보정
    else:
        row = (popup_pos[1] + 330) // config.TILE_SIZE

    font = assets.load_font("Jalnan.ttf", 27)
    obj = tilemap_drawer.tile_objects[row][col]

    tree_name = font.render(f"{resource_manager.TREE_NAME[obj]}", True, config.BLACK)
    tree_produce_oxy_text = font.render(f"{resource_manager.TREE_STATS[obj]['oxygen']} 개", True, config.BLACK)
    tree_produce_money_text = font.render(f"{resource_manager.TREE_STATS[obj]['money']} 원", True, config.BLACK)

    # 팝업 타입(기본, 거꾸로)에 따라 텍스트 좌표 달라짐
    if popup_type == "popup2": # 거꾸로
        screen.blit(tree_name, (popup_pos[0] + 79, popup_pos[1] + 131))
        screen.blit(tree_produce_oxy_text, (popup_pos[0] + 85, popup_pos[1] + 238))
        screen.blit(tree_produce_money_text, (popup_pos[0] + 333, popup_pos[1] + 238))
    else:  # 기본
        screen.blit(tree_name, (popup_pos[0] + 79, popup_pos[1] + 115))
        screen.blit(tree_produce_oxy_text, (popup_pos[0] + 85, popup_pos[1] + 220))
        screen.blit(tree_produce_money_text, (popup_pos[0] + 333, popup_pos[1] + 220))
