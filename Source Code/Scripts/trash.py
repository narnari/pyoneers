"""
TitlePage.py, Game_UI에 맞춰 제작한 trash.py 파일
열린 땅에만 쓰레기 생성, 쓰레기 갯수 세기는 정상적으로 작동하나, 출력이 제대로 되지 않는 문제

from trash import trash_generator, TRASH_TEXT <- game_UI에 작성해야함함
"""


from main_code import load_assets, WIDTH, HEIGHT, TILE_SIZE, BLACK
import pygame
import random
pygame.init()
#---------------Global Variable----------------------------
trash_count =0
#SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
TRASH_TEXT = pygame.font.Font("fonts/Jalnan.ttf", 38)

def trash_generator(trash_gen_tick, screen, tiles, tile_map):
    global trash_count
    trash_gen_tick += 1
    if (trash_gen_tick >= 20):
        trash_gen_tick = 0
        a = random.randint(0, (WIDTH//TILE_SIZE)-1)
        b = random.randint(0, (HEIGHT//TILE_SIZE)-1)
        while (tile_map[b][a] == False):
            a = random.randint(0, (WIDTH//TILE_SIZE)-1)
            b = random.randint(0, (HEIGHT//TILE_SIZE)-1)
        screen.blit(tiles[3], (a*TILE_SIZE, b*TILE_SIZE))
        trash_count += 1
        trash_count_text = TRASH_TEXT.render(str(trash_count), True, BLACK)
        screen.blit(trash_count_text, (30, 400))
        
    return trash_gen_tick
