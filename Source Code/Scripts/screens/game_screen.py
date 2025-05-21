import pygame, sys, ctypes
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()

# ===================== 글로벌 변수 =====================
SCREEN = None
tiles = {}
UIs = {}
tile_map = [[False for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
tick = 0
trash_counts = 0
is_trash_on_tile = [[0 for _ in range(config.WIDTH)] for _ in range(config.HEIGHT)]
is_manual_open, manual_img = False, None
initialized, running = False, False

# --- 중앙 3x3 타일만 선명하게 설정 ---
center_x = config.GRID_WIDTH // 2
center_y = config.GRID_HEIGHT // 2
for row in range(center_y, center_y + 3):
    for col in range(center_x - 1, center_x + 2):
        tile_map[row][col] = True

def get_transparent_tile(tile, alpha):
    copy_tile = tile.copy()
    copy_tile.set_alpha(alpha)
    return copy_tile

initialized = False

# 에셋 불러오기
def load_assets():
    global tiles, UIs, initialized
    if not initialized:
        tiles = {
            "tile": assets.load_image("Tile04.png", (64, 64)),
            "tile_tree1": assets.load_image("Tree1Plant.png"),
            "tile_tree2": assets.load_image("Tree2Plant.png"),
            "tile_tree3": assets.load_image("Tree3Plant.png"),
            "tile_tree4": assets.load_image("Tree4Plant.png"),
            "trash": assets.load_image("trash03.png", (64, 64)),
        }
        UIs = {
            "ui1": assets.load_image("UI1.png"),
            "ui2": assets.load_image("UI2.png"),
            "ui3": assets.load_image("UI3.png"),
            "tree_button": assets.load_image("button1.png", (250, 250)),
            "shovel_button": assets.load_image("button2.png", (250, 250)),
            "manual_button": assets.load_image("button3.png"),
            "setting_button": assets.load_image("button4.png"),
            "back": assets.load_image("back.png", (150, 150)),
            "manual": assets.load_image("manual_screen.png", (config.WIDTH, config.HEIGHT))
        }
        initialized = True

# 게임 전체 화면 그리기
def draw_game(screen):
    screen.fill(config.SKY)
    if is_manual_open:
        screen.blit(UIs["manual"], (0, 0))
    else:
        draw_tilemap(screen)
        draw_button(screen)
        trash_editor.draw_trash_count(screen, trash_counts)
        trash_editor.draw_trash(screen, tiles, is_trash_on_tile)

def draw_tilemap(screen):
    faded_tile = get_transparent_tile(tiles["tile"], 100)
    for row in range(4, config.GRID_HEIGHT - 1):
        for col in range(5, config.GRID_WIDTH - 5):
            x = col * config.TILE_SIZE
            y = row * config.TILE_SIZE
            tile = tiles["tile"] if tile_map[row][col] else faded_tile
            screen.blit(tile, (x, y))

    global tick, trash_counts
    tick, trash_counts = trash_editor.generate_trash(tick, screen, tiles, tile_map, trash_counts, is_trash_on_tile)

# UI 버튼 그리기
def draw_button(screen):
    screen.blit(UIs["ui1"], (50, 20))
    screen.blit(UIs["ui2"], (675, 20))
    screen.blit(UIs["ui3"], (1650, 450))
    screen.blit(UIs["shovel_button"], (40, 600))
    screen.blit(UIs["manual_button"], (1325, 19))
    screen.blit(UIs["setting_button"], (1525, 19))

# 버튼 클래스
class Button:
    def __init__(self, rect, action, image):
        self.rect = pygame.Rect(rect)
        self.action = action
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

def create_buttons(screen):
    tree_planting_button = Button((40, 300, 250, 250), lambda: go_to_tree_planting(screen), UIs["tree_button"])
    back_button = Button((1735, 25, 150, 150), handle_back_button, UIs["back"])
    shovel_button = Button((40, 600, 250, 250), land_editor.toggle_mode, UIs["shovel_button"])
    manual_button = Button((1325, 19, 250, 250), lambda: open_manual(), UIs["manual_button"])
    return [tree_planting_button, back_button, shovel_button, manual_button]

def handle_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "exit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.check_click(event.pos)
            if land_editor.is_editing():
                land_editor.open_tile(tile_map, event.pos, config.TILE_SIZE)
    return None

def go_to_tree_planting(screen):
    import Scripts.screens.tree_planting_screen as tree_planting_screen
    tree_planting_screen.run_tree_planting(screen)

def open_manual():
    global is_manual_open
    is_manual_open = True

def handle_back_button():
    global is_manual_open, running
    if is_manual_open:
        is_manual_open = False
    else:
        running = False

def run_game(screen):
    global running
    running = True
    load_assets()
    buttons = create_buttons(screen)
    clock = pygame.time.Clock()

    while running:
        result = handle_events(buttons)
        if result == "exit":
            return "exit"

        draw_game(screen)
        for button in buttons:
            if is_manual_open and button.action != handle_back_button:
                continue
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return "title"
