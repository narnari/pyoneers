import pygame, sys, ctypes
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor, tilemap_drawer, tree_editor, resource_manager, fire_editor, save_editor
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()

#튜토리얼 봤는지 확인
tutorial_complete = save_editor.file_load_tutorial()

# 화면 비율 설정
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.SCALED, pygame.FULLSCREEN)
Tutorials = {}
def run_tutorial(screen):
    global tutorial_complete
    tutorial_complete = 1
    clock = pygame.time.Clock()
    page = 1
    
    Tutorials = {
        "Tutorial01" : assets.load_image("Tutorial01.png"),
        "Tutorial02" : assets.load_image("Tutorial02.png"),
        "Tutorial03" : assets.load_image("Tutorial03.png"),
        "Tutorial04" : assets.load_image("Tutorial04.png"),
        "Tutorial05" : assets.load_image("Tutorial05.png"),
        "Tutorial06" : assets.load_image("Tutorial06.png"),
        "Tutorial07" : assets.load_image("Tutorial07.png")
    }

    # Main loop
    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                page += 1

        if page < 8:
            screen.blit(Tutorials[f"Tutorial0{page}"], (0, 0))
        else:
            return "game"
        
        pygame.display.flip() 
              
    print("tutorial")