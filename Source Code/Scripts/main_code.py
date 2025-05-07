import sys
import pygame
from pygame.locals import QUIT
import time
import random
# Define clolr
WHITE=(255, 255, 255);
BLACK=(0, 0, 0);
RED=(255, 0, 0);
GREEN=(0, 255, 0);
BLUE=(0, 0, 255);

# Screen settings
WIDTH=1920
HEIGHT=1080
FPS=60
TILE_SIZE = 256

# Grid screen
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# ===================== 글로벌 변수(게임 상태 변수) =====================
SCREEN = None
tiles={}
add_tile_mode = False # 땅 추가 모드 상태
trash_count = [([0]*(WIDTH//64)) for height in range (HEIGHT//64)] #땅 위에 쓰레기의 갯수를 저장
BUTTON_RECT = pygame.Rect(20, 20, 120, 40) # 버튼 위치/크기
trash_tick = 0          #쓰레기 생성 틱
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
        1: pygame.image.load("assets/Tile04.png").convert_alpha(), # 땅 1 (열린 땅)
        -1: pygame.image.load("assets/Tile03.png").convert_alpha(), # 땅 2 (잠긴 땅)
        3: pygame.image.load("assets/Tree02&Shadow.png").convert_alpha(), #나무
        4: pygame.image.load("assets/trash.png").convert_alpha()    #쓰레기
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

# 일정 시간마다 랜덤위치에 쓰레기 배치 함수
#is_trash: 타일에 쓰레기가 있는지 확인 (코드 위 글로벌변수에 넣어놨음음)
#쓰레기는 한 타일에 최대 5개까지 쌓임, 많이 쌓일수록 (불이 더 빨리남)or(불 날 확률이 높아짐)
def trash_generator(trash_gen_tick):
    global trash_count
    trash_gen_tick += 1
    if (trash_gen_tick >= 240):
        trash_gen_tick = 0
        a = random.randint(0, (WIDTH//TILE_SIZE)-1)
        b = random.randint(0, (HEIGHT//TILE_SIZE)-1)
        while (trash_count[b][a] >= 5): #이미 쓰레기가 5개가 넘을경우 a, b 재조정정
            #향후 while문 안에 열려있는 땅인지 닫혀있는 땅인지 확인하는 기능을 추가해야함.
            #해결책 : 땅의 상태를 저장하는 리스트를 새로 만들어야함
            #        예를들어, ground[1][2]가 0이면 열려있고 빈 땅, -1이면 잠긴 땅, 1이면 1렙나무 심긴 땅 등등
            a = random.randint(0, (WIDTH//TILE_SIZE)-1)
            b = random.randint(0, (HEIGHT//TILE_SIZE)-1)
        SCREEN.blit(tiles[4], (a*TILE_SIZE, b*TILE_SIZE))
        #위 코드는 쓰레기를 타일에 보이게하는 코드. 쓰레기 갯수에 따라 다른 이미지 띄우도록 나중에 바꿔야함.
        #그리고 메인함수에서 while에서 draw_tilemap()이랑 같이 돌아가는데, 이때문에 쓰레기를 표시해도 바로 사라지게됨.
        #해결책: trash_generator함수와 draw_tilemap함수 안에 SCREEN.blit으로 직접 이미지 복붙하지 않고
        #       위에서 언급한대로 땅 상태를 저장하는 리스트를 새로 만들어서 땅 상태에 따라 다른 이미지(쓰레기 있는 땅, 쓰레기 없는 땅)을
        #       main함수의 while문 안에서 출력하도록 하면 좋을듯!
        trash_count[b][a] += 1
    return trash_gen_tick


#쓰레기 그리는 함수
def draw_trash():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if trash_count[row][col] > 0:
                SCREEN.blit(tiles[4], (col * TILE_SIZE, row * TILE_SIZE))

# Main game loop
def main():
    global trash_tick
    init_game()
    load_assets()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        SCREEN.fill((BLACK)) # Clear screen with black
        draw_tilemap() # Draw tile background
        trash_tick = trash_generator(trash_tick)
        draw_trash()
        pygame.display.update() # Refresh screen
        handle_events()

# Run the game
if __name__ == '__main__': # 다른 파일에서 import 했을 때 자동 실행 막아줌
    main()
