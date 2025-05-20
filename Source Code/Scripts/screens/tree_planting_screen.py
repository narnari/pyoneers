import pygame
import sys
import ctypes
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

# 나무 정보
trees = [
    {"name": "가문비나무", "increase": 10},
    {"name": "아까시나무", "increase": 20},
    {"name": "자작나무", "increase": 30},
    {"name": "상수리나무", "increase": 50},
]

# 에셋 불러오기
images = {
    "manual_button": assets.load_image("button3.png"),
    "setting_button": assets.load_image("button4.png"),
    "ui1" : assets.load_image("UI1.png"),
    "ui2" : assets.load_image("UI2.png"),
    "back" : assets.load_image("back.png", (150, 150))
}

trees_image = [((assets.load_image(f"Tree{i+1}.png", (180, 180)))) for i in range(4)]

FONT = assets.load_font("Jalnan.ttf", 50)
BUTTON_FONT = assets.load_font("Jalnan.ttf", 38)

# 기본 버튼 클래스. rect는 버튼의 위치와 크기, callback은 실행할 함수
class ButtonBase:
    def __init__(self, rect, callback):
        # rect는 (x좌표, y좌표, 너비, 높이)를 담은 튜플.
        self.rect = pygame.Rect(rect)
        self.callback = callback

    def handle_event(self, event):
        # 마우스 버튼을 눌렀고, 마우스를 누른 위치가 버튼 내부일 때
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# 카드에 배치할 버튼. 기본 버튼 클래스를 상속받았다.
class CardButton(ButtonBase):
    def __init__(self, rect, text, callback):
        # rect와 callback은 그대로 기본 버튼 클래스에서 처리하도록 함.
        super().__init__(rect, callback)
        self.text = text

    # surface는 그림을 그릴 대상. 여기서는 화면이므로 screen
    def draw(self, surface):
        # 초록색 직사각형을 그린다. 모서리는 둥글다.
        pygame.draw.rect(surface, config.GREEN, self.rect, border_radius=10)
        # 글자를 버튼으로 전환하고, 이때 안티 앨리어싱을 하며 색상은 하얀색이다. 그 후 글자가 버튼의 가운데에 오도록 위치를 계산한다.
        text_image = BUTTON_FONT.render(self.text, True, config.WHITE)
        text_place = text_image.get_rect(center=self.rect.center)
        # 글자를 버튼 위에 그린다.
        surface.blit(text_image, text_place)

# 이미지 버튼
class ImageButton(ButtonBase):
    def __init__(self, topleft, image, callback):
        self.image = image
        # 이미지의 왼쪽 위를 기준으로 좌표 설정
        rect = self.image.get_rect(topleft=topleft)
        # 버튼의 위치와 클릭했을 때 실행할 행동은 ButtonBase에 전달한다.
        super().__init__(rect, callback)

    # 지정된 위치에 그림 그리기
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# 카드 그리기 함수
def draw_tree_card(screen, x, y, tree, button, image):
    card_rect = pygame.Rect(x, y, 430, 650) # 카드의 너비와 높이는 고정
    pygame.draw.rect(screen, config.LIGHTGREEN, card_rect, border_radius=20) # 연두색 직사각형을 그린다. 모서리는 둥글다.

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

# 콜백 함수
def plant_tree(name): 
    print(f"{name}를 선택!")
    config.SELECTED_TREE = name

def on_info(): print("매뉴얼 버튼 클릭됨")
def on_settings(): print("설정 버튼 클릭됨")

def run_tree_planting(screen):
    CARD_WIDTH, CARD_HEIGHT, CARD_MARGIN = 430, 650, 40
    CARD_Y = 350
    total_width = 4 * CARD_WIDTH + 3 * CARD_MARGIN
    start_x = (config.WIDTH - total_width) // 2
    positions = [start_x + i * (CARD_WIDTH + CARD_MARGIN) for i in range(4)]

    # 심기 버튼
    tree_planting_button = [
        CardButton(
            (positions[i] + (CARD_WIDTH - 200) / 2, CARD_Y + CARD_HEIGHT - 120, 200, 70),
            "심기", lambda t=tree["name"]: plant_tree(t)
        ) for i, tree in enumerate(trees)
    ]

    result = None
    running = True

    def set_exit(value):
        nonlocal running, result
        result = value
        running = False

    image_buttons = [
        ImageButton((1325, 19), images["manual_button"], on_info),
        ImageButton((1525, 19), images["setting_button"], on_settings),
        ImageButton((1735, 25), images["back"], lambda: set_exit("game")),  # 나무 심는 화면에서 나가면 게임 화면
    ]

    clock = pygame.time.Clock()

    while running:
        screen.fill(config.SKY)

        # 카드 그리기
        for i, tree in enumerate(trees):
            draw_tree_card(screen, positions[i], CARD_Y, tree, tree_planting_button[i], trees_image[i])

        # UI 상단
        screen.blit(images["ui1"], (50, 20))
        screen.blit(images["ui2"], (675, 20))

        # 버튼 그리기
        for btn in image_buttons:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"  # ← 종료는 main이 처리
            for b in tree_planting_button + image_buttons:
                b.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

    return result