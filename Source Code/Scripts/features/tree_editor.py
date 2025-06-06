import pygame
import time
from Scripts.utils import config, assets
from Scripts.features import tilemap_drawer, resource_manager

planting_mode = False
FONT = None

def plant_tree(tile_map, tile_objects, mouse_pos, tile_size, selected_tree_index):
    """ 실제 나무를 심는 함수 """
    global planting_mode
    if not planting_mode:
        return

    col = mouse_pos[0] // tile_size
    row = mouse_pos[1] // tile_size
    tree_index = selected_tree_index + 3  # 실제 나무 인덱스 (3~6)

    resource_manager.check_resource(tile_objects)
    cost = resource_manager.get_tree_cost(tree_index)

    if 4 <= row < config.GRID_HEIGHT - 1 and 5 <= col < config.GRID_WIDTH - 5:
        if tile_map[row][col] and tile_objects[row][col] == 0:
            if not resource_manager.can_spend(money=cost):
                print("돈 부족! 나무 못 심음!")
                import Scripts.screens.game_screen as game_screen
                game_screen.State.show_no_tree_text = True
                game_screen.State.show_no_tree_time = time.time()
                planting_mode = False
                return

            tile_objects[row][col] = tree_index
            resource_manager.tree_level_map[row][col] = 1  # 나무 처음 심을 땐 LV.1

            # 업그레이드 시간 초기화
            resource_manager.tree_timer_map[row][col] = 1800

            import Scripts.screens.game_screen as game_screen
            game_screen.State.show_success_tree_text = True
            game_screen.State.show_success_tree_time = time.time()

            resource_manager.check_resource(tile_objects)
            planting_mode = False
            print(f"{resource_manager.get_tree_name(tree_index)} 심음! 비용 {cost}원 차감됨!")

# 나무 살 돈 없음 화면에 출력
def draw_no_tree_text(screen):
    global FONT
    if FONT is None:
        FONT = assets.load_font("Jalnan.ttf", 38)
    text1 = FONT.render("돈 부족", True, config.BLACK)
    text2 = FONT.render("구매 불가능!", True, config.BLACK)
    screen.blit(text1, (100, 200))
    screen.blit(text2, (50, 240))

# 나무 구매 완료 화면에 출력
def draw_success_tree_text(screen):
    global FONT
    if FONT is None:
        FONT = assets.load_font("Jalnan.ttf", 38)
    text = FONT.render("나무 구매 완료!", True, config.BLACK)
    screen.blit(text, (30, 240))

# 나무 심는 모드 인지 화면에 그림
def draw_editing_text(screen):
    global FONT
    if not planting_mode:
        return
    if FONT is None:
        FONT = assets.load_font("Jalnan.ttf", 38)
    text = FONT.render("나무 심는 중!", True, config.BLACK)
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
        key = f"tile_tree{config.SELECTED_TREE_INDEX + 1}"
        tile_image = tilemap_drawer.tiles[key]
        preview_img = get_transparent_image(tile_image, alpha=150)
        screen.blit(preview_img, preview_img.get_rect(center=(mouse_x, mouse_y)))
    except KeyError:
        pass

# 나무 업그레이드
def upgrade_tree_at(row, col):
    tile_objects = tilemap_drawer.tile_objects
    if resource_manager.tree_upgrade_time[row][col] > 0:
        print("시간 부족 : 업그레이드 실패")
        return False
    if not resource_manager.can_spend(oxy=2000, money=3000):
        print("자원 부족: 업그레이드 실패")
        return False
    resource_manager.tree_level_map[row][col] += 1
    resource_manager.tree_upgrade_time[row][col] = 1800 # 업그레이드 성공 시 시간 초기화
    print(f"[업그레이드] ({row},{col}) 나무 레벨 → {resource_manager.tree_level_map[row][col]}")
    resource_manager.check_resource(tile_objects)
    return True

# 업그레이드 팝업 정보 출력
def draw_popup_tree_info(screen, popup_pos, popup_type):
    col = popup_pos[0] // config.TILE_SIZE
    if popup_type == "popup2":
        row = (popup_pos[1] - 392 + 330) // config.TILE_SIZE
    else:
        row = (popup_pos[1] + 330) // config.TILE_SIZE

    font = assets.load_font("Jalnan.ttf", 27)
    obj = tilemap_drawer.tile_objects[row][col]
    upgrade_time = resource_manager.tree_upgrade_time[row][col]
    if upgrade_time <= 0:
        upgrade_text = font.render("업그레이드 가능!", True, config.BLACK)
    else:
        m, s = upgrade_time // 60, upgrade_time % 60
        upgrade_text = font.render(f"{m:02d}분 {s:02d}초", True, config.BLACK)

    level = resource_manager.tree_level_map[row][col]
    oxy = int(resource_manager.TREE_STATS[obj]['oxygen'] * (2.5 ** (level - 1)))
    money = int(resource_manager.TREE_STATS[obj]['money'] * (2.5 ** (level - 1)))
    tree_name = font.render(f"{resource_manager.TREE_NAME[obj]}", True, config.BLACK)
    tree_level_text = font.render(f"{level}", True, config.BLACK)
    tree_produce_oxy_text = font.render(f"{oxy} 개", True, config.BLACK)
    tree_produce_money_text = font.render(f"{money} 원", True, config.BLACK)

    if popup_type == "popup2":
        screen.blit(upgrade_text, (popup_pos[0] + 350, popup_pos[1] + 71))
        screen.blit(tree_level_text, (popup_pos[0] + 455, popup_pos[1] + 133))
        screen.blit(tree_name, (popup_pos[0] + 79, popup_pos[1] + 133))
        screen.blit(tree_produce_oxy_text, (popup_pos[0] + 85, popup_pos[1] + 238))
        screen.blit(tree_produce_money_text, (popup_pos[0] + 333, popup_pos[1] + 238))
    else:
        screen.blit(upgrade_text, (popup_pos[0] + 350, popup_pos[1] + 53))
        screen.blit(tree_level_text, (popup_pos[0] + 455, popup_pos[1] + 115))
        screen.blit(tree_name, (popup_pos[0] + 79, popup_pos[1] + 115))
        screen.blit(tree_produce_oxy_text, (popup_pos[0] + 85, popup_pos[1] + 220))
        screen.blit(tree_produce_money_text, (popup_pos[0] + 333, popup_pos[1] + 220))
