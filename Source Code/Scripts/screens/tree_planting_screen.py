import pygame, sys
import ctypes
from Scripts.features import tree_editor, tilemap_drawer, resource_manager
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

# 글로벌 상태 변수
result = False
is_manual_open = False

# 나무 정보
trees = [
    {"name": "가문비나무", "costs": 50, "oxygen": 15, "money": 2},
    {"name": "아까시나무", "costs": 80, "oxygen": 12, "money": 8},
    {"name": "자작나무", "costs": 80, "oxygen": 8, "money": 12},
    {"name": "상수리나무", "costs": 50, "oxygen": 2, "money": 15},
]

images = {}
trees_image = {}

# 나무 심기 화면에서 사용할 이미지 에셋 불러오기
def load_tree_planting_assets():
    global images, trees_image, result
    images = {
        "manual_button": assets.load_image("button3.png"),
        "setting_button": assets.load_image("button4.png"),
        "ui1": assets.load_image("UI1.png"),
        "ui2": assets.load_image("UI2.png"),
        "back": assets.load_image("back.png", (150, 150)),
        "tree_manual": assets.load_image("tree_manual_screen.png", (config.WIDTH, config.HEIGHT))
    }
    trees_image = [assets.load_image(f"Tree{i+1}.png", (180, 180)) for i in range(4)]
    result = True

# 폰트 설정
FONT = assets.load_font("Jalnan.ttf", 50)
INFO_FONT = assets.load_font("Jalnan.ttf", 29)
BUTTON_FONT = assets.load_font("Jalnan.ttf", 38)

# 기본 버튼 클래스. rect는 버튼의 위치와 크기, callback은 실행할 함수
# 기존에 있던 CardButton과 ButtonBase를 통합하였다.
class ButtonBase:
    def __init__(self, rect, callback, image=None, text=None):
        self.rect = pygame.Rect(rect)   # 버튼의 위치와 크기
        self.action = callback          # 클릭 시 실행할 함수
        self.image = image              # 버튼 이미지
        self.text = text                # 텍스트 버튼용 텍스트

    def draw(self, surface):
        # 이미지 버튼 그리기
        if self.image:
            surface.blit(self.image, self.rect)
            # 텍스트 버튼 그리기. 배경은 녹색, 글씨는 흰색
        elif self.text:
            pygame.draw.rect(surface, config.GREEN, self.rect, border_radius=15)
            text_surf = BUTTON_FONT.render(self.text, True, config.WHITE)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 20))

            surface.blit(text_surf, text_rect)

    # 클릭된 위치가 버튼 내부이면 콜백 함수 실행
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# 매뉴얼, 설정, 뒤로가기 버튼 생성
def create_buttons(screen):
    manual_button = ButtonBase((1325, 19, 150, 150), open_manual, images["manual_button"])
    setting_button = ButtonBase((1525, 19, 150, 150), open_settings, images["setting_button"])
    back_button = ButtonBase((1735, 25, 150, 150), handle_back_button, images["back"])
    return [back_button, setting_button, manual_button]

# UI 이미지 + 배경 화면에 그리기
def draw_button(screen):
    screen.fill(config.SKY)
    # 매뉴얼이 열려있으면 매뉴얼 이미지 그리기
    if is_manual_open:
        screen.blit(images["tree_manual"], (0, 0))
    # 매뉴얼이 열려있지 않으면 UI 이미지 그리기
    else:
        screen.blit(images["ui1"], (50, 20))
        screen.blit(images["ui2"], (675, 20))

# 뒤로가기 버튼 기능 구현
def handle_back_button():
    global is_manual_open, running
    # 매뉴얼이 열려있는 상황에서는 뒤로가기가 매뉴얼 닫기
    if is_manual_open:
        is_manual_open = False
    # 그렇지 않으면 메인 화면으로 가기
    else:
        running = False

# 매뉴얼 버튼 기능 구현
def open_manual():
    global is_manual_open
    is_manual_open = True   # 매뉴얼 이미지 그리기

# 설정 버튼 기능 구현
def open_settings():
    print("설정 버튼 클릭됨")

# 나무 카드 그리기 함수
def draw_tree_card(screen, x, y, tree, button, image):
    # 카드 배경 설정하고 그리기
    card_rect = pygame.Rect(x, y, 430, 650)
    pygame.draw.rect(screen, config.LIGHTGREEN, card_rect, border_radius=20)

    # 카드 중앙에 나무 이미지용 원과 나무 이미지 그리기. 원은 초록색이다.
    card_center = (x + 215, y + 180)
    pygame.draw.circle(screen, config.GREEN, card_center, 150)
    screen.blit(image, image.get_rect(center=card_center))

    # 카드에 쓸 글자들을 이미지로 전환하고 안티 앨리어싱을 한다. 색상은 하얀색이다. 그 후 카드 위에 그린다.
    name_surf = FONT.render(tree["name"], True, config.WHITE)
    screen.blit(name_surf, name_surf.get_rect(center=(x + 215, y + 370)))

    oxygen_surf = INFO_FONT.render(f"산소 생산량 {tree['oxygen']} 증가", True, config.WHITE)
    screen.blit(oxygen_surf, oxygen_surf.get_rect(center=(x + 215, y + 430)))

    money_surf = INFO_FONT.render(f"돈 생산량 {tree['money']} 증가", True, config.WHITE)
    screen.blit(money_surf, money_surf.get_rect(center=(x + 215, y + 470)))

    # 버튼을 그린다. 버튼의 구현은 별도로 한다.
    button.draw(screen)

    # 버튼의 중심 좌표 계산
    button_rect = button.rect
    center_x = button_rect.centerx
    center_y = button_rect.centery

    # 비용 텍스트 (버튼 아래에)
    cost_text = BUTTON_FONT.render(f"-${tree['costs']}", True, config.WHITE)
    cost_rect = cost_text.get_rect(center=(center_x, center_y + 25))  # 버튼보다 아래
    screen.blit(cost_text, cost_rect)
    
# 메인 루프 함수
def run_tree_planting(screen):
    global running
    running = True
    clock = pygame.time.Clock()
    load_tree_planting_assets()

    # 나무 카드 위치 설정
    CARD_WIDTH, CARD_HEIGHT, CARD_MARGIN = 430, 650, 40
    CARD_Y = 350
    total_width = 4 * CARD_WIDTH + 3 * CARD_MARGIN
    start_x = (config.WIDTH - total_width) // 2
    positions = [start_x + i * (CARD_WIDTH + CARD_MARGIN) for i in range(4)]

    # 심기 버튼 생성
    tree_planting_button = [
        ButtonBase(
            (positions[i] + (CARD_WIDTH - 300) / 2, CARD_Y + CARD_HEIGHT - 140, 300, 110),
            lambda t=tree["name"]: select_tree(t),
            text="비용"
        )
        for i, tree in enumerate(trees)
    ]


    # 루프를 종료하기 위한 함수
    def set_exit(value):
        global running, result
        result = value
        running = False

    # 콜백 함수. 선택한 나무에 따라 다른 텍스트가 출력된다.
    def select_tree(name): 
        print(f"{name}를 선택!")
        tree_editor.planting_mode = True
        config.SELECTED_TREE = name
        
        # trees 리스트에서 선택한 나무 이름에 따라 인덱스를 저장
        for i, tree in enumerate(trees):
            if tree["name"] == name:
                config.SELECTED_TREE_INDEX = i
                break

        # 현재 마우스의 위치에 나무 심기
        tree_editor.plant_tree(
            tilemap_drawer.tile_map,
            tilemap_drawer.tile_objects,
            pygame.mouse.get_pos(),
            config.TILE_SIZE,
            config.SELECTED_TREE_INDEX)
        set_exit("game")

    # 매뉴얼, 설정, 뒤로가기 버튼 생성
    ui_buttons = create_buttons(screen)

    # 메인 이벤트 루프
    while running:
        screen.fill(config.SKY)

        # 이벤트 처리 부분
        for event in pygame.event.get():
            # 창 닫기를 누르면 종료된다.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 마우스를 클릭했을 때 발생하는 이벤트들을 처리하는 부분    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 매뉴얼이 열려 있을 땐 뒤로가기 버튼의 기능만 적용하고 다른 버튼의 기능은 무시한다.
                for btn in ui_buttons:
                    if is_manual_open and btn.action != handle_back_button:
                        continue
                    btn.check_click(event.pos)

                # 마찬가지로 나무 심기 버튼도 매뉴얼이 열려있지 않은 상황에서만 적용한다.
                for btn in tree_planting_button:
                    if not is_manual_open:
                        btn.check_click(event.pos)

        # 매뉴얼과 배경, UI를 그린다.
        draw_button(screen)

        # 매뉴얼이 닫혀 있다면, 나무 카드와 심기 버튼을 그린다.
        if not is_manual_open:
            for i, tree in enumerate(trees):
                draw_tree_card(screen, positions[i], CARD_Y, tree, tree_planting_button[i], trees_image[i])

        # 매뉴얼, 설정, 뒤로가기 버튼을 그린다. 매뉴얼이 열려 있을 땐 뒤로가기 버튼만 그리고 다른 버튼은 그리지 않는다다.
        for btn in ui_buttons:
            if is_manual_open and btn.action != handle_back_button:
                continue
            btn.draw(screen)

        resource_manager.check_resource(tilemap_drawer.tile_objects)
        resource_manager.update_resources()
        resource_manager.draw_resources(screen)

        # 화면 1초에 60 프레임으로 유지
        pygame.display.flip()
        clock.tick(60)
