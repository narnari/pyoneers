import pygame, sys
import ctypes
from Scripts.screens import game_screen
from Scripts.features import tree_editor, tilemap_drawer
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

# 글로벌 상태 변수
result = False
is_manual_open = False

# 나무 정보
trees = [
    {"name": "가문비나무", "increase": 10},
    {"name": "아까시나무", "increase": 20},
    {"name": "자작나무", "increase": 30},
    {"name": "상수리나무", "increase": 50},
]

images = {}
trees_image = {}
def load_tree_planting_assets():
    global images, trees_image, result
    # 에셋 불러오기
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

FONT = assets.load_font("Jalnan.ttf", 50)
BUTTON_FONT = assets.load_font("Jalnan.ttf", 38)

# 기본 버튼 클래스. rect는 버튼의 위치와 크기, callback은 실행할 함수
# 기존에 있던 CardButton과 ButtonBase를 통합하였다.
class ButtonBase:
    def __init__(self, rect, callback, image=None, text=None):
        self.rect = pygame.Rect(rect)
        self.action = callback
        self.image = image
        self.text = text

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        elif self.text:
            pygame.draw.rect(surface, config.GREEN, self.rect, border_radius=10)
            text_surf = BUTTON_FONT.render(self.text, True, config.WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

def create_buttons(screen):
    manual_button = ButtonBase((1325, 19, 150, 150), open_manual, images["manual_button"])
    setting_button = ButtonBase((1525, 19, 150, 150), open_settings, images["setting_button"])
    back_button = ButtonBase((1735, 25, 150, 150), handle_back_button, images["back"])
    return [back_button, setting_button, manual_button]

def draw_button(screen):
    screen.fill(config.SKY)
    if is_manual_open:
        screen.blit(images["tree_manual"], (0, 0))
    else:
        screen.blit(images["ui1"], (50, 20))
        screen.blit(images["ui2"], (675, 20))

# UI 버튼 콜백
def handle_back_button():
    global is_manual_open, running
    if is_manual_open:
        is_manual_open = False
    else:
        running = False

def open_manual():
    global is_manual_open
    is_manual_open = True

def open_settings():
    print("설정 버튼 클릭됨")

# 카드 그리기 함수
def draw_tree_card(screen, x, y, tree, button, image):
    card_rect = pygame.Rect(x, y, 430, 650)
    pygame.draw.rect(screen, config.LIGHTGREEN, card_rect, border_radius=20)

    # 카드의 나무 이미지를 둘 장소를 찾는다. 그 장소에 초록색 원을 그리고 이미지도 그린다.
    card_center = (x + 215, y + 180)
    pygame.draw.circle(screen, config.GREEN, card_center, 150)
    screen.blit(image, image.get_rect(center=card_center))

    # 카드에 쓸 글자들을 이미지로 전환하고 안티 앨리어싱을 한다. 색상은 하얀색이다. 그 후 카드 위에 그린다.
    name_surf = FONT.render(tree["name"], True, config.WHITE)
    screen.blit(name_surf, name_surf.get_rect(center=(x + 215, y + 400)))
    info_surf = BUTTON_FONT.render(f"산소 생산량 {tree['increase']} 증가", True, config.WHITE)
    screen.blit(info_surf, info_surf.get_rect(center=(x + 215, y + 460)))
    # "심기" 버튼을 그린다. 버튼의 구현은 별도로 한다.
    button.draw(screen)

# 메인 루프
def run_tree_planting(screen):
    global running
    running = True
    clock = pygame.time.Clock()
    load_tree_planting_assets()

    # 나무 카드 위치 계산
    CARD_WIDTH, CARD_HEIGHT, CARD_MARGIN = 430, 650, 40
    CARD_Y = 350
    total_width = 4 * CARD_WIDTH + 3 * CARD_MARGIN
    start_x = (config.WIDTH - total_width) // 2
    positions = [start_x + i * (CARD_WIDTH + CARD_MARGIN) for i in range(4)]

    # 심기 버튼
    tree_planting_button = [
        ButtonBase(
            (positions[i] + (CARD_WIDTH - 200) / 2, CARD_Y + CARD_HEIGHT - 120, 200, 70),
            lambda t=tree["name"]: select_tree(t),
            text="심기"
        )
        for i, tree in enumerate(trees)
    ]

    def set_exit(value):
        global running, result
        result = value
        running = False

    # 콜백 함수
    def select_tree(name): 
        print(f"{name}를 선택!")
        tree_editor.planting_mode = True
        config.SELECTED_TREE = name
        
        # trees 리스트에서 선택한 나무 이름의 인덱스 저장
        for i, tree in enumerate(trees):
            if tree["name"] == name:
                config.SELECTED_TREE_INDEX = i
                break
        tree_editor.plant_tree(tilemap_drawer.tile_map, tilemap_drawer.tile_objects, pygame.mouse.get_pos(), config.TILE_SIZE, config.SELECTED_TREE_INDEX)
        set_exit("game")

    ui_buttons = create_buttons(screen)
    while running:
        screen.fill(config.SKY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in ui_buttons:
                    if is_manual_open and btn.action != handle_back_button:
                        continue
                    btn.check_click(event.pos)
                for btn in tree_planting_button:
                    if not is_manual_open:
                        btn.check_click(event.pos)

        draw_button(screen)

        if not is_manual_open:
            for i, tree in enumerate(trees):
                draw_tree_card(screen, positions[i], CARD_Y, tree, tree_planting_button[i], trees_image[i])

        for btn in ui_buttons:
            if is_manual_open and btn.action != handle_back_button:
                continue
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)
