import pygame, sys, ctypes
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor, tilemap_drawer, tree_editor, resource_manager
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()

# ===================== 글로벌 변수 =====================
SCREEN = None
UIs = {}
initialized = False
is_manual_open, manual_img = False, None
initialized, running = False, False

# 에셋 불러오기
def load_assets():
    global UIs, initialized
    if not initialized:
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
        resource_manager.draw_resources(screen)
    else:
        draw_button(screen)
        tilemap_drawer.draw_tilemap(screen)
        trash_editor.draw_trash_count(screen, trash_editor.trash_count)
        land_editor.draw_editing_text(screen)
        tree_editor.draw_editing_text(screen)
        tilemap_drawer.draw_tile_objects(screen, tilemap_drawer.tile_objects, tilemap_drawer.tiles)
        resource_manager.draw_resources(screen)

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
    manual_button = Button((1325, 19, 150, 150), lambda: open_manual(), UIs["manual_button"])
    return [tree_planting_button, back_button, shovel_button, manual_button]

def handle_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "exit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.check_click(event.pos)
            # 땅 열기 모드 일 때
            if land_editor.is_editing():
                land_editor.open_tile(tilemap_drawer.tile_map, event.pos, config.TILE_SIZE)
                resource_manager.check_resource(tilemap_drawer.tile_objects)
            # 나무 심기 모드 일 때
            elif tree_editor.planting_mode:
                tree_editor.plant_tree(tilemap_drawer.tile_map, tilemap_drawer.tile_objects, event.pos, config.TILE_SIZE, config.SELECTED_TREE_INDEX)
                resource_manager.check_resource(tilemap_drawer.tile_objects)
    return None

def open_manual():
    global is_manual_open
    is_manual_open = True

def go_to_tree_planting(screen):
    import Scripts.screens.tree_planting_screen as tree_planting_screen
    tree_planting_screen.run_tree_planting(screen)

def handle_back_button():
    global is_manual_open, running
    if is_manual_open:
        is_manual_open = False
    else:
        running = False

def run_game(screen):
    global running, SCREEN
    SCREEN = screen
    running = True
    load_assets()
    tilemap_drawer.load_assets()
    buttons = create_buttons(screen)
    clock = pygame.time.Clock()

    resource_manager.check_resource(tilemap_drawer.tile_objects) # 자원 체크 함수 호출

    while running:
        result = handle_events(buttons)
        if result == "exit":
            return "exit"
        if result == "title":
            return "title"
        resource_manager.update_resources()
        
        draw_game(screen)
        for button in buttons:
            if is_manual_open and button.action != handle_back_button:
                continue
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    return "title"
