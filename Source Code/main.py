import pygame
import sys
import os

# 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), "Scripts"))

from Scripts.screens import game_screen, title_screen
from Scripts.utils import config

def main():
    pygame.init()
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
                running = False
        elif state == "game":
            result = game_screen.run_game(screen)
            if result == "title":
                state = "title"
            elif result == "exit":
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
