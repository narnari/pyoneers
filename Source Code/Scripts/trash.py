"""
TitlePage.py, Game_UI에 맞춰 제작한 trash.py 파일

[현재 구현 성공/실패 목록]
쓰레기 생성(O)
쓰레기 갯수 증가(O)
쓰레기 출력(X)
쓰레기 갯수 출력(O)

game_UI 많이 편집해놔서 새로 커밋해야하는데 일단 game_UI는 커밋 안했음음
"""


from main_code import load_assets, WIDTH, HEIGHT, TILE_SIZE, BLACK
import pygame
import random
pygame.init()
#---------------Global Variable----------------------------

#SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
TRASH_TEXT = pygame.font.Font("fonts/Jalnan.ttf", 38)

def trash_generator(trash_gen_tick, screen, tiles, tile_map, trash_count):
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
        
    return trash_gen_tick, trash_count

def trash_count_print(screen, trash_count):
        trash_count_text = TRASH_TEXT.render(str(trash_count), True, BLACK)
        screen.blit(trash_count_text, (1760, 545))
