"""
TitlePage.py, Game_UI에 맞춰 제작한 trash.py 파일

[현재 구현 성공/실패 목록]
쓰레기 생성(O)
쓰레기 갯수 증가(O)
쓰레기 출력(X)
쓰레기 갯수 출력(O)

game_UI 많이 편집해놔서 새로 커밋해야하는데 일단 game_UI는 커밋 안했음음
"""

import pygame
import random
from Scripts.utils import assets, config
pygame.init()
#---------------Global Variable----------------------------
#SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
trash_count = 0
TRASH_TEXT = assets.load_font("Jalnan.ttf", 38)
#is_trash_on_tile = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

def generate_trash(trash_gen_tick, tile_objects, tile_map, trash_count):
    trash_gen_tick += 1
    if (trash_gen_tick >= config.TRASH_TICK_INTERVAL):
        trash_gen_tick = 0
        a = random.randint(0, (config.GRID_WIDTH)-1)
        b = random.randint(0, (config.GRID_HEIGHT)-1)
        if is_full_trash(tile_objects, tile_map):
            return trash_gen_tick, trash_count
        
        while True:
             a = random.randint(0, (config.GRID_WIDTH) - 1)
             b = random.randint(0, (config.GRID_HEIGHT) - 1)
             if (tile_map[b][a] and tile_objects[b][a] == 0):
                  break

        tile_objects[b][a] = 1
        trash_count += 1
        
    return trash_gen_tick, trash_count

def is_full_trash(tile_objects, tile_map):
    for i in  range(config.GRID_HEIGHT):
        for j in range(config.GRID_WIDTH):
             if (tile_map[i][j] and tile_objects[i][j] == 0):
                  return False
    return True

def draw_trash_count(screen, trash_count):
        trash_count_text = TRASH_TEXT.render(str(trash_count), True, config.BLACK)
        screen.blit(trash_count_text, (1760, 545))
