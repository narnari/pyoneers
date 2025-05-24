import pygame, sys, ctypes, os
from pygame.locals import QUIT
from Scripts.features import land_editor, trash_editor
from Scripts.utils import assets, config
ctypes.windll.user32.SetProcessDPIAware()

# 화면 비율 설정
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.SCALED, pygame.FULLSCREEN)

# 설정 (기본 / 사운드 / 기타)
setting = "basic"

bgm = assets.load_sound("SandCastle.mp3")

# 이전 화면
back_state = "title"

# 슬라이더 위치 및 크기
slider_x = config.WIDTH // 3
slider_y = config.HEIGHT // 3
slider_width = config.WIDTH // 2.25
slider_height = 50

# 핸들(circle)의 상태
handle_radius = 30
handle_x = slider_x + slider_width // 2
dragging = False

# 이전 설정
back_sound_setting = bgm.get_volume()
back_handle_x = handle_x

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
        
        # 선택한 버튼을 밝게 보이게 하여 강조하는 용
        def draw_lighting(self, surface):
            center = self.rect.center
            radius = self.rect.width // 2
            text_surf = self.font.render(self.text, True, config.WHITE)
            text_rect = text_surf.get_rect(center=center)

            pygame.draw.rect(surface, config.LIGHTGREEN, self.rect, radius)

            surface.blit(text_surf, text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    
    BGM_SOUND_TEXT = assets.load_font("Jalnan.ttf", 50)
    text = BGM_SOUND_TEXT.render("BGM 크기", True, config.BLACK)
                    
    # 버튼 콜백 함수들
    def basic_setting(): 
        global setting
        print("기본 설정")
        setting = "basic"

    def sound_setting(): 
        global setting
        print("사운드")
        setting = "sound"

    def etc_setting(): 
        global setting
        print("기타")
        setting = "etc"
        
    def setting_cancel():
        nonlocal result, running
        global handle_x
        result = back_state     # 시작화면에서 왔으면 시작화면으로, 게임화면에서 왔으면 게임화면으로 돌아가기
        print("설정 취소")
        bgm.set_volume(back_sound_setting)
        handle_x = back_handle_x
        running = False
        
    def setting_save():
        nonlocal result, running
        global back_sound_setting, back_handle_x
        result = back_state
        print("설정 적용")
        back_sound_setting = bgm.get_volume()
        back_handle_x = handle_x
        running = False

    button_x_size = 270
    button_y_size = 120
    buttons = [
        Button("기본 설정", config.WIDTH // 5, 370, button_x_size, button_y_size, basic_setting, font_size=56),
        Button("사운드", config.WIDTH // 5, 540, button_x_size, button_y_size, sound_setting, font_size=56),
        Button("기타", config.WIDTH // 5, 710, button_x_size, button_y_size, etc_setting, font_size=56),
        Button("취소", config.WIDTH // 3, 890, 2 * config.WIDTH // 7, button_y_size, setting_cancel, font_size=56),
        Button("적용", 2 * config.WIDTH // 3, 890, 2 * config.WIDTH // 7, button_y_size, setting_save, font_size=56)
    ]
                        
    clock = pygame.time.Clock()
    settingFont = assets.load_font("Jalnan.ttf", 100)
    settingTitle = settingFont.render("설정", True, config.WHITE)

    # Main loop
    running = True
    while running:
        clock.tick(60)
        global handle_x, dragging
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return "exit"
            if setting == "sound":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (handle_x - event.pos[0])**2 + (slider_y - event.pos[1])**2 <= handle_radius**2:
                        dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        handle_x = max(slider_x, min(event.pos[0], slider_x + slider_width))
                        volume = (handle_x - slider_x) / slider_width
                        bgm.set_volume(volume)
            for button in buttons:
                button.handle_event(event)

        screen.fill(config.SKY)
        
        # 설정 뒷배경 (초록색) 그리기
        pygame.draw.rect(screen, config.DARKGREEN, pygame.Rect(200, 75, config.WIDTH - 400, config.HEIGHT - 150))
        screen.blit(settingTitle, [config.WIDTH // 2 - 100, 108])

        for button in buttons:
            button.draw(screen)
            
            # 선택한 설정만 밝은 색으로 강조함
            if setting == "basic":
                buttons[0].draw_lighting(screen)
            elif setting == "sound":
                buttons[1].draw_lighting(screen)
                # 슬라이더 그리기
                screen.blit(text, (slider_x, slider_y - 90))
                pygame.draw.rect(screen, config.GREEN, (slider_x, slider_y - slider_height // 2, slider_width, slider_height))
                pygame.draw.circle(screen, config.WHITE, (handle_x, slider_y), handle_radius)
            elif setting == "etc":
                buttons[2].draw_lighting(screen)
            
        pygame.display.flip() 
              
    print("result = " + result)
    return result
