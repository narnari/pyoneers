import pygame, sys, ctypes
from pygame.locals import QUIT
from land_editor import toggle_mode, is_editing, open_tile

ctypes.windll.user32.SetProcessDPIAware()

# Define color
SKY = (220, 245, 255)

# Screen settings
WIDTH = 1920
HEIGHT = 1080
FPS = 60
TILE_SIZE = 64

GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# ===================== 글로벌 변수(게임 상태 변수) =====================
SCREEN = None
tiles = {}
UIs = {}
tile_map = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# --- 중앙 3x3 타일만 선명하게 설정 ---
center_x = GRID_WIDTH // 2
center_y = GRID_HEIGHT // 2
for row in range(center_y, center_y + 3):
    for col in range(center_x - 1, center_x + 2):
        tile_map[row][col] = True

# 게임 자원 초기화 플래그
initialized = False

# 타일 흐리게 복사
def get_transparent_tile(tile, alpha):
    copy_tile = tile.copy()
    copy_tile.set_alpha(alpha)
    return copy_tile

def load_assets():
    global tiles, UIs, initialized
    if not initialized:
        tiles = {
            0: pygame.image.load("assets/Tile03.png").convert_alpha(),
            1: pygame.image.load("assets/Tile04.png").convert_alpha(),
            2: pygame.image.load("assets/tree03.png").convert_alpha(),
            3: pygame.image.load("assets/trash.png").convert_alpha(),
        }
        UIs = {
            0: pygame.image.load("assets/UI1.png").convert_alpha(),
            1: pygame.image.load("assets/UI2.png").convert_alpha(),
            2: pygame.image.load("assets/UI3.png").convert_alpha(),
            3: pygame.image.load("assets/button1.png").convert_alpha(),
            4: pygame.image.load("assets/button2.png").convert_alpha(),
            5: pygame.image.load("assets/button3.png").convert_alpha(),
            6: pygame.image.load("assets/button4.png").convert_alpha(),
            7: pygame.image.load("assets/back.png").convert_alpha()
        }

        tiles[0] = pygame.transform.scale(tiles[0], (64, 64))
        tiles[1] = pygame.transform.scale(tiles[1], (64, 64))
        tiles[2] = pygame.transform.scale(tiles[2], (64, 64))
        tiles[3] = pygame.transform.scale(tiles[3], (64, 64))
        UIs[3] = pygame.transform.scale(UIs[3], (250, 250))
        UIs[4] = pygame.transform.scale(UIs[4], (250, 250))
        UIs[7] = pygame.transform.scale(UIs[7], (150, 150))

        initialized = True

def draw_game(screen):
    screen.fill(SKY)
    draw_tilemap(screen)
    draw_button(screen)

def draw_tilemap(screen):
    faded_tile = get_transparent_tile(tiles[1], 100)
    for row in range(4, GRID_HEIGHT - 1):
        for col in range(5, GRID_WIDTH - 5):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[1] if tile_map[row][col] else faded_tile
            screen.blit(tile, (x, y))

def draw_button(screen):
    screen.blit(UIs[0], (50, 20))
    screen.blit(UIs[1], (675, 20))
    screen.blit(UIs[2], (1650, 450))
    # screen.blit(UIs[3], (40, 300))  # 여기서 그리지 않음
    screen.blit(UIs[4], (40, 600))  # UIs[4] 다시 그림
    screen.blit(UIs[5], (1325, 19))
    screen.blit(UIs[6], (1525, 19))

# Button class for managing buttons and click events
class Button:
    def __init__(self, rect, action, image):  # image 인자 추가
        self.rect = pygame.Rect(rect)
        self.action = action
        self.image = image  # image 저장

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # image 그림

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

def create_buttons(screen):
    tree_planting_button = Button((40, 300, 250, 250), lambda: go_to_tree_planting(screen), UIs[3])
    back_button = Button((1735, 25, 150, 150), lambda: setattr(sys.modules[__name__], 'running', False), UIs[7])
    shovel_button = Button((40, 600, 250, 250), toggle_mode, UIs[4])
    return [tree_planting_button, back_button, shovel_button]

def handle_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "exit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 모든 버튼에 대해 클릭 감지
            for button in buttons:
                button.check_click(event.pos)
            if is_editing(): # 현재 '땅 열기 모드'
                open_tile(tile_map, event.pos, TILE_SIZE) # 클릭된 타일 열기
    return None

def start_game():
    print("게임 시작!")

def go_to_tree_planting(screen):
    import TreePlanting
    TreePlanting.run_tree_planting(screen)

#뒤로가기
def go_to_title():
    global SCREEN
    pygame.quit()
    return "menu"

def main(screen):
    global SCREEN
    pygame.init()
    SCREEN = screen
    load_assets()
    buttons = create_buttons(screen)

    global running
    running = True
    clock = pygame.time.Clock()
    while running:
        result = handle_events(buttons)
        if result == "exit":
            return result

        draw_game(screen)
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return "menu"  # 뒤로가기 클릭 시
