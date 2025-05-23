import pygame, sys, ctypes, os
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()

# 화면 비율 설정
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.SCALED, pygame.FULLSCREEN)

# 이전 화면
back_state = "title"

def run_setting(screen):
    
    # 상태 변수
    result = None
    
    # 버튼 클래스
    class Button:
        def __init__(self, text, x, y, width, height, callback, font_size=64):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.callback = callback
            self.rect.center = (x, y)
            self.font = assets.load_font("Jalnan.ttf", font_size)

        def draw(self, surface):
            center = self.rect.center
            radius = self.rect.width // 2
            text_surf = self.font.render(self.text, True, config.WHITE)
            text_rect = text_surf.get_rect(center=center)

            pygame.draw.rect(surface, config.GREEN, self.rect, radius)

            surface.blit(text_surf, text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                dx = event.pos[0] - self.rect.centerx
                dy = event.pos[1] - self.rect.centery
                if (dx**2 + dy**2)**0.5 <= self.rect.width // 2:
                    self.callback()
                    
    # 버튼 콜백 함수들
    def basic_setting(): 
        print("기본 설정")

    def sound_setting(): 
        print("사운드")

    def etc_setting(): 
        print("기타")
        
    def setting_cancel():
        nonlocal result, running
        result = back_state     # 시작화면에서 왔으면 시작화면으로, 게임화면에서 왔으면 게임화면으로 돌아가기
        print("설정 취소")
        running = False
        
    def setting_save():
        nonlocal result, running
        result = back_state
        print("설정 확인")
        running = False

    button_x_size = 270
    button_y_size = 120
    buttons = [
        Button("기본 설정", config.WIDTH // 5, 370, button_x_size, button_y_size, basic_setting, font_size=56),
        Button("사운드", config.WIDTH // 5, 540, button_x_size, button_y_size, sound_setting, font_size=56),
        Button("기타", config.WIDTH // 5, 710, button_x_size, button_y_size, etc_setting, font_size=56),
        Button("취소", config.WIDTH // 3, 890, 2 * config.WIDTH // 7, button_y_size, setting_cancel, font_size=56),
        Button("확인", 2 * config.WIDTH // 3, 890, 2 * config.WIDTH // 7, button_y_size, setting_save, font_size=56)
    ]

    clock = pygame.time.Clock()
    settingFont = assets.load_font("Jalnan.ttf", 100)
    settingTitle = settingFont.render("설정", True, config.WHITE)

    # Main loop
    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return "exit"
            for button in buttons:
                button.handle_event(event)

        screen.fill(config.SKY)
        
        # 설정 뒷배경 (초록색) 그리기
        pygame.draw.rect(screen, config.DARKGREEN, pygame.Rect(200, 75, config.WIDTH - 400, config.HEIGHT - 150))
        screen.blit(settingTitle, [config.WIDTH // 2 - 100, 108])
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
    return result
