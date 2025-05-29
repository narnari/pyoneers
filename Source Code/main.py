import pygame
import sys
import os

# 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), "Scripts"))

from Scripts.screens import game_screen, title_screen, setting_screen
from Scripts.utils import config
from Scripts.features import save_editor, resource_manager, tilemap_drawer

def main():
    pygame.init()
    
    setting_screen.bgm.play(-1)    # 무한 반복
    setting_screen.bgm.set_volume(0.5)
    
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.SCALED, pygame.FULLSCREEN)
    pygame.display.set_caption("Terrabloom")

    state = "title"
    running = True
    clock = pygame.time.Clock()

    while running:
        if state == "title":
            result = title_screen.run_title(screen)
            if result == "start":
                state = "game"
            elif result == "exit":
                save_editor.file_save(resource_manager.resources["stored_money"], resource_manager.resources["stored_oxygen"], tilemap_drawer.tile_map, tilemap_drawer.tile_objects, resource_manager.land_count)
                running = False
            elif result == "setting":
                setting_screen.back_state = "title"
                state = "setting"
        elif state == "game":
            # 게임 루프 내에서 이 코드 추가 (예: while running 루프 안)
            save_editor.auto_save(resource_manager.resources["stored_money"], resource_manager.resources["stored_oxygen"], tilemap_drawer.tile_map, tilemap_drawer.tile_objects, config.AUTO_SAVE_INTERVAL)
            
            result = game_screen.run_game(screen)
            if result == "title":
                state = "title"
            elif result == "exit":
                running = False
            elif result == "setting":
                setting_screen.back_state = "game"
                state = "setting"
        elif state == "setting":
            # 처음 설정 창 실행 시 기본 설정이 가장 먼저 보이게
            setting_screen.setting = "basic"
            result = setting_screen.run_setting(screen)
            if result == "title":
                state = "title"
            elif result == "game":
                state = "game"
            elif result == "exit":
                running = False
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
