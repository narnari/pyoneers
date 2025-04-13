import sys
import pygame
from pygame.locals import QUIT

# Define clolr
WHITE=(255, 255, 255);
BLACK=(0, 0, 0);
RED=(255, 0, 0);
GREEN=(0, 255, 0);
BLUE=(0, 0, 255);

# Screen settings
WIDTH=1088 #1920 종료 메뉴 만들고 나면 화면 비율 이걸로 바꾸기
HEIGHT=832 #1080
FPS=60
TILE_SIZE = 64

# Grid screen
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# ===================== 글로벌 변수(게임 상태 변수) =====================
SCREEN = None
tiles={}
add_tile_mode = False # 땅 추가 모드 상태
BUTTON_RECT = pygame.Rect(20, 20, 120, 40) # 버튼 위치/크기
# =======================================================

    # 타일 상태 False : 흐림, True 선명
tile_map = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
# --- 중앙 3x3 타일만 선명하게 설정 ---
center_x = GRID_WIDTH // 2
center_y = GRID_HEIGHT // 2
for row in range(center_y - 1, center_y + 2):
    for col in range(center_x - 1, center_x + 2):
        tile_map[row][col] = True

def init_game():
    global SCREEN
    # initialize Pygame
    pygame.init()
    # Set up the display window
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TERRABLOOM") # Game title 

def load_assets():
    global tiles
    # Load tile image
    tiles = {
        0: pygame.image.load("assets/background.png").convert_alpha(), # 배경 (민트)
        1: pygame.image.load("assets/basicTile-1.png").convert_alpha(), # 땅 1 (초록)
        2: pygame.image.load("assets/Basic Tile-1.png").convert_alpha(), # 땅 2 (연두)
        3: pygame.image.load("assets/tree.png").convert_alpha() #나무
    }

# 타일 흐리게 복사
def get_transparent_tile(tile, alpha):
    copy_tile = tile.copy() # 원본은 그대로
    copy_tile.set_alpha(alpha) # 복사본만 흐리게
    return copy_tile

def draw_background_tile():
    # 흐릿한 타일 생성
    faded_tile = get_transparent_tile(tiles[1], 100)  # 흐릿하게

    for y in range(0, HEIGHT, TILE_SIZE):
        for x in range(0, WIDTH, TILE_SIZE):
            SCREEN.blit(faded_tile, (x, y))

# Draw tiles to fill the screen
def draw_tilemap():
    faded_tile = get_transparent_tile(tiles[1], 100)
    # 타일 화면 가득 차도록 배치
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[1] if tile_map[row][col] else faded_tile
            SCREEN.blit(tile, (x, y))

# --- 버튼 그리기 ---
def draw_button():
    pygame.draw.rect(SCREEN, GREEN, BUTTON_RECT)
    font = pygame.font.SysFont(None, 24)
    text = font.render("땅 추가", True, BLACK)
    SCREEN.blit(text, (BUTTON_RECT.x + 15, BUTTON_RECT.y + 10))

# 이벤트 처리 함수
def handle_events():
    global add_tile_mode
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos() # 현재 마우스 위치
            if BUTTON_RECT.collidepoint(mx, my): # 마우스가 버튼 아에 있는지 확인
                add_tile_mode = True
                print("땅 추가 모드 ON!")
            elif add_tile_mode:
                tile_x = mx // TILE_SIZE
                tile_y = my // TILE_SIZE
                if 0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT:
                    tile_map[tile_y][tile_x] = True  # 클릭한 타일을 선명하게

# Main game loop
def main():
    init_game()
    load_assets()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        SCREEN.fill((BLACK)) # Clear screen with black
        draw_tilemap() # Draw tile background
        draw_button()
        pygame.display.update() # Refresh screen
        handle_events()

# Run the game
if __name__ == '__main__': # 다른 파일에서 import 했을 때 자동 실행 막아줌
    main()