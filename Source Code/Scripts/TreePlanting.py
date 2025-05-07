import pygame
import sys
import ctypes

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

# 색상
SKY = (220, 245, 255)
LIGHTGREEN = (143, 217, 119)
WHITE = (255, 255, 255)
GREEN = (57, 150, 82)
BLACK = (0, 0, 0)

# 폰트
FONT = pygame.font.Font("fonts/Jalnan.ttf", 50)
BUTTON_FONT = pygame.font.Font("fonts/Jalnan.ttf", 38)

# 카드 정보
trees = [
    {"name": "가문비나무", "increase": 10},
    {"name": "참나무", "increase": 20},
    {"name": "자작나무", "increase": 30},
    {"name": "상수리나무", "increase": 50},
]

# 이미지 로드
circle_images = [pygame.transform.scale(pygame.image.load(f"assets/Tree{i+1}.png"), (180, 180)) for i in range(4)]
info_button_image = pygame.image.load("assets/button3.png").convert_alpha()
settings_button_image = pygame.image.load("assets/button4.png").convert_alpha()
header1_image = pygame.image.load("assets/UI1.png").convert_alpha()
header2_image = pygame.image.load("assets/UI2.png").convert_alpha()
back_button_image = [pygame.transform.scale(pygame.image.load("assets/back.png").convert_alpha(), (150, 150))]

# 카드 버튼 클래스
class card_button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect, border_radius=10)
        text_image = BUTTON_FONT.render(self.text, True, WHITE)
        text_place = text_image.get_rect(center=self.rect.center)
        surface.blit(text_image, text_place)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# 매뉴얼/설정 버튼 클래스
class info_settings_button:
    def __init__(self, topleft, image, callback):
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
        self.callback = callback

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# 나무 카드 그리기 함수
def draw_tree_card(screen, x, y, tree, button, circle_image):  # screen 인자 추가
    card_rect = pygame.Rect(x, y, 430, 650)
    pygame.draw.rect(screen, LIGHTGREEN, card_rect, border_radius=20)

    # 나무 그림의 원형 배경
    circle_center = (x + 215, y + 180)
    pygame.draw.circle(screen, GREEN, circle_center, 150)

    # 이미지 그리기
    circle_rect = circle_image.get_rect(center=circle_center)
    screen.blit(circle_image, circle_rect)

    # 텍스트
    name_surf = FONT.render(tree["name"], True, WHITE)
    name_rect = name_surf.get_rect(center=(x + 215, y + 400))
    screen.blit(name_surf, name_rect)

    info_surf = BUTTON_FONT.render(f"산소 생산량 {tree['increase']} 증가", True, WHITE)
    info_rect = info_surf.get_rect(center=(x + 215, y + 460))
    screen.blit(info_surf, info_rect)

    button.draw(screen)

# 콜백 함수
def plant_tree(name):
    print(f"{name}를 심었습니다!")

def on_info():
    print("정보 버튼 클릭됨")

def on_settings():
    print("설정 버튼 클릭됨")



def run_tree_planting(screen):  # screen 인자 추가
    WIDTH = 1920
    card_width, card_height, card_margin = 430, 650, 40
    card_y = 350
    total_width = 4 * card_width + 3 * card_margin
    start_x = (WIDTH - total_width) // 2
    card_positions = [start_x + i * (card_width + card_margin) for i in range(4)]

    buttons = [
        card_button((card_positions[i] + (card_width - 200) / 2, card_y + card_height - 120, 200, 70),
                    "심기", lambda t=tree["name"]: plant_tree(t))
        for i, tree in enumerate(trees)
    ]

    image_buttons = [
        info_settings_button((1525, 19), info_button_image, on_info),
        info_settings_button((1725, 19), settings_button_image, on_settings),
    ]

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(SKY)

        for i, tree in enumerate(trees):
            draw_tree_card(screen, card_positions[i], card_y, tree, buttons[i], circle_images[i])

        screen.blit(header1_image, (50, 20))
        screen.blit(header2_image, (675, 20))

        for btn in image_buttons:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for button in buttons:
                button.handle_event(event)
            for btn in image_buttons:
                btn.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()