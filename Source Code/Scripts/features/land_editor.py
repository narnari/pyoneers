# land_editor.py
from Scripts.utils import assets, config

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
    클릭한 타일을 열기 (True로 설정)
    tile_map: 2차원 리스트 (bool)
    mouse_pos: 마우스 클릭 위치 (x, y)
    tile_size: 타일 크기 (int)
    """
    if not editing_mode:
        return

    col = mouse_pos[0] // tile_size
    row = mouse_pos[1] // tile_size

    # 범위 체크
    if 4 <= row < config.GRID_HEIGHT-1 and 5 <= col < config.GRID_WIDTH-5:
        tile_map[row][col] = True  # 잠긴 땅 
        
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
