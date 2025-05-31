"""
TitlePage.py, Game_UI에 맞춰 제작한 trash.py 파일
"""

import pygame
import random
import time
from Scripts.utils import assets, config
pygame.init()
#---------------Global Variable----------------------------
trash_count = 0
TRASH_TEXT = assets.load_font("Jalnan.ttf", 38)

def trash_on_load(trash_count, t_to_f, x, y):
     trash_count += 1
     t_to_f.append(config.Fire(x,y,time.time()))
     return trash_count

def decrease_count_when_ignite(trash_count):
     trash_count -= 1
     return trash_count

def generate_trash(trash_gen_tick, tile_objects, tile_map, trash_count, t_to_f):
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
        t_to_f.append(config.Fire(a,b,time.time()))     #t_to_f 인덱스에 현재 좌표와 시간 append
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

def remove_trash(x,y,t_to_f, trash_count, money):   #t_to_f에서 x,y좌표에 해당하는 쓰레기를 제거(리스트 컴프리헨션), 이후 카운트 1 감소
     t_to_f[:] = [t for t in t_to_f if not (t.x == x and t.y == y)]
     trash_count -= 1
     money -= 20
     return trash_count, money