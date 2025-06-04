# land_editor.py

from Scripts.features import resource_manager
from Scripts.screens import game_screen
from Scripts.utils import assets, config
import time

# 전역 변수: 현재 땅 편집 모드인지 여부
editing_mode = False

EDITING_TEXT = None

def toggle_mode():
    # 모드 ON/OFF 전환 (삽 버튼 누를 때 호출됨)
    global editing_mode
    editing_mode = not editing_mode

def is_editing():
    # 현재 땅 편집 모드인지 여부 반환
    return editing_mode


def open_tile(tile_map, mouse_pos, tile_size):
    """
    클릭한 타일을 열기 (True로 설정)하고, 동적 비용을 적용.
    tile_map: 2차원 리스트 (bool)
    mouse_pos: 마우스 클릭 위치 (x, y)
    tile_size: 타일 크기 (int)
    """
    if not editing_mode:
        return

    col = mouse_pos[0] // tile_size
    row = mouse_pos[1] // tile_size

    # 범위 체크: 클릭한 타일이 유효한 구매 가능 영역 내에 있는지 확인
    if not (4 <= row < config.GRID_HEIGHT - 1 and 5 <= col < config.GRID_WIDTH - 5):
        print("맵 범위 오류.")
        return # 유효한 구매 범위 밖을 클릭했습니다.

    # 이미 타일이 잠금 해제되었는지 확인
    if tile_map[row][col]:
        print("이미 열린 땅!")
        return # 이미 잠금 해제된 타일은 다시 구매할 수 없습니다.

    # 1. 현재 잠금 해제된 타일 개수(resource_manager.land_count)에 따라 비용 결정
    cost = 0 # cost 변수를 미리 초기화하여 모든 경로에서 정의되도록 합니다.

    if  resource_manager.land_count <= 9:
        cost = 500
    elif 10 <= resource_manager.land_count <= 29:
        cost = 1000
    elif 30 <= resource_manager.land_count <= 49:
        cost = 1500
    else:
        cost = 2000

    # 2. 자원이 충분한지 확인
    if not resource_manager.can_spend(money=cost):
        print("땅 살 돈 없음!")
        game_screen.State.show_no_money_text = True
        game_screen.State.show_no_money_time = time.time()

        return

    # 1. 타일을 잠금 해제 
    tile_map[row][col] = 1

    # 땅 구매 완료 출력용
    game_screen.State.show_success_money_text = True
    game_screen.State.show_success_money_time = time.time()

    # 2. resource_manager에 있는 잠금 해제된 땅의 개수를 증가
    resource_manager.land_count += 1

    # 3. 콘솔에 메시지 출력 (디버깅용)
    print(f"땅 열었음! 비용 {cost}원 차감됨!")

    #toggle_mode() # 하나의 타일을 구매한 직후 편집 모드를 종료

# 땅 열 돈 없음 화면에 출력
def draw_no_money_text(screen):
    global EDITING_TEXT

    # pygame 초기화 이후에 폰트 로딩
    if EDITING_TEXT is None:
        EDITING_TEXT = assets.load_font("Jalnan.ttf", 38)

        # text = EDITING_TEXT.render(f"땅 구매 비용 {resource_manager.can_spend(cost)}원!", True, config.BLACK)
    text1 = EDITING_TEXT.render("돈 부족", True, config.BLACK)
    text2 = EDITING_TEXT.render("확장 불가능!", True, config.BLACK)
    screen.blit(text1, (100, 870))
    screen.blit(text2, (50, 910)) 
    return

# 땅 구매 완료 화면에 출력
def draw_success_text(screen):
    global EDITING_TEXT
    if EDITING_TEXT is None:
        EDITING_TEXT = assets.load_font("Jalnan.ttf", 38)
    text = EDITING_TEXT.render("땅 구매 완료!", True, config.BLACK)
    screen.blit(text, (35, 870)) 


# 땅 열린 모드 인지 화면에 그림
def draw_editing_text(screen):
    global EDITING_TEXT
    if not editing_mode:
        return

    # pygame 초기화 이후에 폰트 로딩
    if EDITING_TEXT is None:
        EDITING_TEXT = assets.load_font("Jalnan.ttf", 38)

    text = EDITING_TEXT.render("땅 편집 중!", True, config.BLACK)
    screen.blit(text, (1700, 1000)) 
