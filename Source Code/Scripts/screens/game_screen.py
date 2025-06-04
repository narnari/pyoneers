import pygame, ctypes
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor, tilemap_drawer, tree_editor, resource_manager, fire_editor
from Scripts.utils import assets, config
import time # 돈 없다는 텍스트 출력 시가 확인 시 필요
ctypes.windll.user32.SetProcessDPIAware()

UIs = {}
BUTTON_FONT = assets.load_font("Jalnan.ttf", 28)

# 글로벌 상태 변수. 코드의 전체적인 길이를 줄이기 위해 class로 선언하였다.
class State:
    running = False # 게임의 루프 실행 여부
    tree_upgrade_popup_requested = False # 나무 업그레이드 팝업을 표시하는 상황인지의 여부
    fire_putout_popup_requested = False # 불 끄기 팝업을 표시하는 상황인지의 여부
    trash_throwout_popup_requested = False # 쓰레기 버리기 팝업을 표시하는 상황인지의 여부
    is_manual_open = False # 매뉴얼 화면을 여는 상황인지의 여부
    setting_requested = False # 설정 화면을 열라는 요청이 들어왔는지의 여부
    back_to_title_requested = False # 타이틀 화면으로의 복귀 요청이 들어왔는지의 여부부
    popup_position = None # 팝업 위치 지정
    popup_buttons = [] # 팝업에 표시할 버튼 리스트
    fire_popup_buttons = [] # 불 끄기 팝업에 표시할 버튼 리스트
    trash_popup_buttons = [] # 쓰레기 버리기 팝업에 표시할 버튼 리스트
    popup_type = "default"  # 팝업창에 사용할 이미지
    show_no_money_text = False # 돈 없는 텍스트 출력할지 여부
    show_success_money_text = False # 땅 구매 완료 텍스트 출력할지 여부
    show_no_money_time = 0 # 텍스트 출력할 시간
    show_success_money_time = 0 # 텍스트 출력할 시간

# 에셋 불러오기
def load_assets():
    if UIs: return
    UIs.update({
        "ui1": assets.load_image("UI1.png"),
        "ui2": assets.load_image("UI2.png"),
        "ui3": assets.load_image("UI3.png"),
        "tree_button": assets.load_image("button1.png", (250, 250)),
        "shovel_button": assets.load_image("button2.png", (250, 250)),
        "manual_button": assets.load_image("button3.png"),
        "setting_button": assets.load_image("button4.png"),
        "back": assets.load_image("back.png", (150, 150)),
        "manual_screen": assets.load_image("manual_screen.png", (config.WIDTH, config.HEIGHT)),
        "popup1": assets.load_image("tree_upgrade_popup.png", (614, 326)),
        "popup2": assets.load_image("tree_upgrade_popup2.png", (614, 326)),
        "trashpopup": assets.load_image("trash_throwout_popup.png", (540, 207)),
        "firepopup": assets.load_image("fire_putout_popup.png", (540, 207))
    })

# 이벤트 처리 함수
def handle_events(buttons):
    for event in pygame.event.get():
        if event.type == QUIT: # 창을 닫는 이벤트 발생 시 종료 신호 반환
            return "exit"
        elif event.type == pygame.MOUSEBUTTONDOWN: # 마우스 버튼이 눌렸을 때 클릭된 위치에서 이벤트 처리
            handle_mouse_click(event.pos, buttons)
    return None # 이벤트 없으면 None 반환

# 버튼 클래스 정의
class Button:
    # rect부터 순서대로 버튼 위치 및 크기, 버튼 클릭 시 실행 될 함수, 버튼 텍스트, 버튼 이미지, 배경 색, 글씨 색
    def __init__(self, rect, action, text=None, image=None, bg_color=config.GREEN, text_color=config.WHITE):
        self.rect = pygame.Rect(rect)
        self.action = action
        self.text = text
        self.image = image
        self.bg_color = bg_color
        self.text_color = text_color

    # 버튼 그리기 함수
    def draw(self, surface):
        if self.image: # 이미지 그려야 하는 버튼이면 이미지 출력
            surface.blit(self.image, self.rect.topleft)
        elif self.text: # 텍스트 그려야 하는 버튼이면 사각형 그린 뒤 텍스트 출력. 사각형에는 테두리 존재
            pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=10)
            pygame.draw.rect(surface, config.BLACK, self.rect, width=3, border_radius=10)
            text_surf = BUTTON_FONT.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    # 버튼 클릭 체크 함수
    def check_click(self):
        self.action()

# UI 버튼 생성 함수
def create_buttons(screen):
    return [
        Button((40, 300, 250, 250), lambda: go_to_tree_planting(screen), image=UIs["tree_button"]),
        Button((40, 600, 250, 250), land_editor.toggle_mode, image=UIs["shovel_button"]),
        Button((1325, 19, 150, 150), request_manual, image=UIs["manual_button"]),
        Button((1525, 19, 150, 150), request_setting, image=UIs["setting_button"]),
        Button((1735, 25, 150, 150), handle_back_button, image=UIs["back"])
    ]

# 버튼 화면에 출력하는 함수
def draw_buttons(screen, buttons):
    for btn in buttons:
        btn.draw(screen)

# 나무 심기 화면으로 이동하는 함수
def go_to_tree_planting(screen):
    import Scripts.screens.tree_planting_screen as tree_planting_screen
    tree_planting_screen.run_tree_planting(screen)

# 매뉴얼 열기 함수(플래그 설정)
def request_manual():
    State.is_manual_open = True

# 설정 열기 함수(플래그 설정)
def request_setting():
    State.setting_requested = True

# 뒤로 가기 버튼 처리 함수
def handle_back_button():
    if State.is_manual_open: # 매뉴얼이 열려있으면 닫고 플래그 설정
        State.is_manual_open = False
    else: # 매뉴얼이 열러있지 않다면 타이틀로 돌아가기 요청(플래그 설정)
        State.back_to_title_requested = True
        State.running = False
        
# 팝업 이미지 그리기 함수
def draw_popup(screen):
    # 매뉴얼 오픈 상태가 아닐 때만 팝업 그리고 버튼 생성
    if not State.is_manual_open: 
        if State.tree_upgrade_popup_requested and State.popup_position: # 나무 팝업 띄워졌다면
            if State.popup_type == "popup2":
                popup_image = UIs["popup2"]
            else:
                popup_image = UIs["popup1"]
            popup_rect = popup_image.get_rect(topleft=State.popup_position)
            screen.blit(popup_image, popup_rect) # 화면에 나무 팝업 이미지 그리기
            draw_buttons(screen, State.popup_buttons) # 나무 팝업 버튼 그리기
            tree_editor.draw_popup_tree_info(screen, popup_rect, State.popup_type)
            
        elif State.trash_throwout_popup_requested: # 쓰레기 팝업 띄워졌다면
            popup_rect = UIs["trashpopup"].get_rect(topleft=State.popup_position)
            screen.blit(UIs["trashpopup"], popup_rect) # 화면에 쓰레기 팝업 이미지 그리기
            draw_buttons(screen, State.trash_popup_buttons) # 쓰레기 팝업 버튼 그리기
            
        elif State.fire_putout_popup_requested: # 불 팝업 띄워졌다면
            popup_rect = UIs["firepopup"].get_rect(topleft=State.popup_position)
            screen.blit(UIs["firepopup"], popup_rect) # 화면에 불 팝업 이미지 그리기
            draw_buttons(screen, State.fire_popup_buttons) # 불 팝업 버튼 그리기

# 팝업 버튼 데이터 생성 함수
# 버튼은 기본적으로 팝업의 오른쪽에 세로로 정렬
def create_popup_buttons(popup_rect):
    # 나무 업그레이드 팝업일 경우
    if State.tree_upgrade_popup_requested:
        if State.popup_type == "popup2": # popup2라면
            State.popup_buttons = [
                Button((popup_rect.right + 20, popup_rect.bottom - 246, 180, 60), remove_tree_action, "제거", bg_color=config.RED),
                Button((popup_rect.right + 20, popup_rect.bottom - 134, 180, 60), upgrade_tree_action, "업그레이드", bg_color=config.BLUE)
            ]
        else: # popup1이라면
            State.popup_buttons = [
                Button((popup_rect.right + 20, popup_rect.bottom - 260, 180, 60), remove_tree_action, "제거", bg_color=config.RED),
                Button((popup_rect.right + 20, popup_rect.bottom - 148, 180, 60), upgrade_tree_action, "업그레이드", bg_color=config.BLUE)
            ]
    # 불 끄기 팝업일 경우
    elif State.fire_putout_popup_requested:
        State.fire_popup_buttons = [
            Button((popup_rect.left + 20, popup_rect.bottom - 125, 180, 60), remove_fire_action, "제거", bg_color=config.BLUE),
            Button((popup_rect.left + 335, popup_rect.bottom - 125, 180, 60), close_trash_popup, "취소", bg_color=config.RED)
        ]
    # 쓰레기 버리기 팝업일 경우
    elif State.trash_throwout_popup_requested:
        State.trash_popup_buttons = [
            Button((popup_rect.left + 20, popup_rect.bottom - 125, 180, 60), remove_trash_action, "제거", bg_color=config.BLUE),
            Button((popup_rect.left + 335, popup_rect.bottom - 125, 180, 60), close_trash_popup, "취소", bg_color=config.RED)
        ]

# 나무 업그레이드 함수(미구현)
def upgrade_tree_action():
    print("업그레이드 버튼 클릭됨")

# 나무 제거 함수(미구현)
def remove_tree_action():
    print("제거 버튼 클릭됨")

# 쓰레기 제거 함수
def remove_trash_action():
    if State.popup_position is None:
        return
    #돈 부족하면 그냥 리턴
    if resource_manager.resources["stored_money"] < 20:
        return
    popup_x, popup_y = State.popup_position
    x = popup_x // config.TILE_SIZE
    y = popup_y + 210
    y = y // config.TILE_SIZE

    tilemap_drawer.tile_objects[y][x] = 0
    trash_editor.trash_count, resource_manager.resources["stored_money"] = trash_editor.remove_trash(x,y,tilemap_drawer.t_to_f, trash_editor.trash_count, resource_manager.resources["stored_money"])
    close_trash_popup()

# 불 제거 함수
def remove_fire_action():
    if State.popup_position is None:
        return
    #산소 부족하면 그냥 리턴
    if resource_manager.resources["stored_oxygen"] < 20:
        return
    popup_x, popup_y = State.popup_position
    x = popup_x // config.TILE_SIZE
    popup_y = popup_y + 210
    y = popup_y // config.TILE_SIZE

    tilemap_drawer.tile_objects[y][x] = 0
    resource_manager.resources["stored_oxygen"] = fire_editor.remove_fire(x,y, tilemap_drawer.fspread, resource_manager.resources["stored_oxygen"])
    close_fire_popup()
    
# 쓰레기 제거와 불 제거 팝업에서 취소 버튼을 눌렀을 때 호출되는 함수
def cancel_popup_action():
    print("쓰레기 & 불 취소 버튼 클릭됨")

# 타일을 클릭했을 때 해당 타일이 나무/불/쓰레기인지 확인하고, 이에 맞는 팝업을 띄우거나 닫는 함수
def toggle_popup(mouse_pos):
    col, row = mouse_pos[0] // config.TILE_SIZE, mouse_pos[1] // config.TILE_SIZE # 마우스 클릭 시 위치 저장
    if not (0 <= row < config.GRID_HEIGHT and 0 <= col < config.GRID_WIDTH): # 타일을 클릭한 것이 아니면 return
        return

    tile_value = tilemap_drawer.tile_objects[row][col] # 클릭한 타일의 상태값 불러오기. 나무/불/쓰레기인지 확인한다.
    clicked_pos = (col * config.TILE_SIZE, row * config.TILE_SIZE - 330) # 나무 팝업이 띄워질 위치
    fire_and_trash_clicked_pos = (col * config.TILE_SIZE, row * config.TILE_SIZE - 210) # 불 팝업 & 쓰레기 팝업이 띄워질 위치

    if tile_value >= 3: # 나무 타일 클릭 시
        # 이미 열린 나무 팝업을 다시 클릭했으면 닫기
        if State.tree_upgrade_popup_requested and State.popup_position == clicked_pos:
            close_tree_popup()
        else: # 아니라면 다른 팝업 다 닫고 나무 팝업만 열기
            close_fire_popup()
            close_trash_popup()
            open_tree_popup(clicked_pos)

    elif tile_value == 2: # 불 타일 클릭 시
        # 이미 열린 불 팝업을 다시 클릭했으면 닫기
        if State.fire_putout_popup_requested and State.popup_position == fire_and_trash_clicked_pos:
            close_fire_popup()
        else: # 아니라면 다른 팝업 다 닫고 불 팝업만 열기
            close_tree_popup()
            close_trash_popup()            
            open_fire_popup(fire_and_trash_clicked_pos)

    elif tile_value == 1: # 쓰레기 타일 클릭 시
        # 이미 열린 쓰레기 팝업을 다시 클릭했으면 닫기
        if State.trash_throwout_popup_requested and State.popup_position == fire_and_trash_clicked_pos:
            close_trash_popup()
        else: # 아니라면 다른 팝업 다 닫고 쓰레기 팝업만 열기
            close_tree_popup()
            close_fire_popup()
            open_trash_popup(fire_and_trash_clicked_pos)

    else: # 그 외에 다른 곳 클릭 시 열려있는 팝업 전부 닫기
        close_tree_popup()
        close_fire_popup()
        close_trash_popup() 

# 나무 팝업 열고 버튼 생성
def open_tree_popup(position):
    # 나무가 위쪽에 있으면 팝업을 아래쪽으로, 아니라면 위쪽으로 띄우기
    if position[1] < 100:
        adjusted_position = (position[0], position[1] + 392)
        popup_image = UIs["popup2"]
    else:
        adjusted_position = position
        popup_image = UIs["popup1"]

    State.tree_upgrade_popup_requested = True
    State.popup_position = adjusted_position # 팝업이 띄워질 위치 정하기
    State.popup_type = "popup2" if popup_image == UIs["popup2"] else "default"

    popup_rect = popup_image.get_rect(topleft=adjusted_position) # 팝업 크기에 맞게 좌표 지정
    create_popup_buttons(popup_rect) # 지정한 좌표로 팝업 버튼 생성

# 나무 팝업 닫기
def close_tree_popup():
    State.tree_upgrade_popup_requested = False  # 팝업이 띄워졌는지 여부 False로 변경
    State.popup_position = None # 팝업 띄워질 위치 초기화
    State.popup_buttons.clear() # 팝업과 함께 띄워지는 버튼 리스트 삭제 (버튼 지우기)

# 나머지 open_fire_popup, open_trash_popup / close_fire_popup, close_trash_popup도 비슷하게 동작한다.

def open_fire_popup(position):
    State.fire_putout_popup_requested = True
    State.popup_position = position
    popup_rect = UIs["firepopup"].get_rect(topleft=position)
    create_popup_buttons(popup_rect)

def close_fire_popup():
    State.fire_putout_popup_requested = False
    State.popup_position = None
    State.fire_popup_buttons.clear()
    
def open_trash_popup(position):
    State.trash_throwout_popup_requested = True
    State.popup_position = position
    popup_rect = UIs["trashpopup"].get_rect(topleft=position)
    create_popup_buttons(popup_rect)

def close_trash_popup():
    State.trash_throwout_popup_requested = False
    State.popup_position = None
    State.trash_popup_buttons.clear()

def handle_mouse_click(pos, buttons):
    # 버튼 클릭 우선
    for btn in buttons:
        if State.is_manual_open and btn.action != handle_back_button:
            continue
        if btn.rect.collidepoint(pos):
            btn.check_click()
            return

    # 나무 팝업 버튼
    if State.tree_upgrade_popup_requested:
        for btn in State.popup_buttons:
            if btn.rect.collidepoint(pos):
                btn.check_click()
                return
    
    # 불 팝업 버튼
    elif State.fire_putout_popup_requested:
        for btn in State.fire_popup_buttons:
            if btn.rect.collidepoint(pos):
                btn.check_click()
                return
            
    # 쓰레기 팝업 버튼
    elif State.trash_throwout_popup_requested:
        for btn in State.trash_popup_buttons:
            if btn.rect.collidepoint(pos):
                btn.check_click()
                return

    toggle_popup(pos)

    if land_editor.is_editing():
        land_editor.open_tile(tilemap_drawer.tile_map, pos, config.TILE_SIZE)
        resource_manager.check_resource(tilemap_drawer.tile_objects)
    elif tree_editor.planting_mode:
        tree_editor.plant_tree(tilemap_drawer.tile_map, tilemap_drawer.tile_objects, pos, config.TILE_SIZE, config.SELECTED_TREE_INDEX)
        resource_manager.check_resource(tilemap_drawer.tile_objects)

# 항상 출력하는 UI 3개 출력
def draw_UI(screen):
    screen.blit(UIs["ui1"], (50, 20))
    screen.blit(UIs["ui2"], (675, 20))
    screen.blit(UIs["ui3"], (1650, 450))

# 게임 전체 화면 그리는 함수
def draw_game(screen):
    pygame.mouse.set_visible(not tree_editor.planting_mode) # 나무 심기 모드에서는 마우스 커서 숨기기
    screen.fill(config.SKY) # 배경색 채우기
    global show_no_money_text, no_money_start_time

    # 매뉴얼 열기를 요청받으면(=매뉴얼 버튼 클릭되면) 매뉴얼 이미지 출력하고 그리기 종료
    if State.is_manual_open:
        screen.blit(UIs["manual_screen"], (0, 0))
        return

    # 아니면 매뉴얼 외 다른 UI 그리기
    else:
        draw_UI(screen)
        draw_UI(screen)
        tilemap_drawer.draw_tilemap(screen) # 타일 맵 그리기
        trash_editor.draw_trash_count(screen, trash_editor.trash_count) # 쓰레기 개수 출력
        land_editor.draw_editing_text(screen) # 땅 확장 기능 사용중인지 출력
        if State.show_no_money_text:
            elapsed = time.time() - State.show_no_money_time
            if elapsed < 0.75:
                land_editor.draw_no_money_text(screen)
            else:
                State.show_no_money_text = False
        if State.show_success_money_text:
            elapsed = time.time() - State.show_success_money_time
            if elapsed < 0.75:
                land_editor.draw_success_text(screen)
            else :
                State.show_success_money_text = False
        tree_editor.draw_editing_text(screen) # 나무 심기 기능 사용 중인지 출력
        tree_editor.draw_tree_preview(screen) # 나무 심기 전 투명하게 보이도록
        tilemap_drawer.draw_tile_objects(screen, tilemap_drawer.tile_objects, tilemap_drawer.tiles) # 타일 맵 위 오브젝트 그리기
        resource_manager.draw_resources(screen) # 재화 보유량 및 생산량 출력

def run_game(screen):
    State.running = True
    load_assets()
    tilemap_drawer.load_assets()
    buttons = create_buttons(screen)
    clock = pygame.time.Clock()
    resource_manager.check_resource(tilemap_drawer.tile_objects)

    while State.running:
        result = handle_events(buttons)
        if result == "exit":
            return "exit"

        resource_manager.update_resources()
        draw_game(screen)

        # 매뉴얼 열려있으면 뒤로가기 버튼만, 아니면 전체 버튼 그리기
        draw_buttons(screen, [btn for btn in buttons if State.is_manual_open and btn.action == handle_back_button] if State.is_manual_open else buttons)
        draw_popup(screen)
        pygame.display.flip()
        clock.tick(60)

        if State.setting_requested:
            State.setting_requested = False
            return "setting"

    # while 종료 후
    if State.back_to_title_requested:
        State.back_to_title_requested = False
        return "title"

    return None