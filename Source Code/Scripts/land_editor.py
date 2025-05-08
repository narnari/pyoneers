# land_editor.py

# 전역 변수: 현재 땅 편집 모드인지 여부
editing_mode = False

def toggle_mode():
    # 모드 ON/OFF 전환 (삽 버튼 누를 때 호출됨)
    global editing_mode
    editing_mode = not editing_mode
    print("땅 열기 모드:", editing_mode)

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
    if 0 <= row < len(tile_map) and 0 <= col < len(tile_map[0]):
        tile_map[row][col] = True  # 잠긴 땅 열기
