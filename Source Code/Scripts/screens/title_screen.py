import pygame, sys, ctypes
from Scripts.screens import game_screen
from Scripts.utils import assets, config

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

#화면 비율 설정\
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.SCALED, pygame.FULLSCREEN)
pygame.display.set_caption("Tree Planting UI")

def run_title(screen):
    # 타이틀 이미지
    title_image = assets.load_image("Title.png", (920, 460))
    title_rect = title_image.get_rect(center=(config.WIDTH // 2, 200))

    # 상태 변수
    result = None

    #버튼 클래스
    class Button:
        def __init__(self, text, x, y, width, height, callback, font_size=72):
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

            if self.text == "게임 시작":
                pygame.draw.ellipse(surface, config.GREEN, self.rect)
                pygame.draw.ellipse(surface, config.GREEN, self.rect, 4)
            else:
                pygame.draw.circle(surface, config.GREEN, center, radius)
                pygame.draw.circle(surface, config.GREEN, center, radius, 4)

            surface.blit(text_surf, text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                dx = event.pos[0] - self.rect.centerx
                dy = event.pos[1] - self.rect.centery
                if (dx**2 + dy**2)**0.5 <= self.rect.width // 2:
                    self.callback()
                    
    # 버튼 콜백 함수들
    def start_game(): 
        nonlocal result, running
        result = "start"
        print("시작!")
        running = False

    def on_setting(): 
        nonlocal result, running
        result = "setting"
        print("설정!")
        running = False

    def quit_game(): 
        nonlocal result, running
        result = "exit"
        print("종료!")
        running = False

    button_size = 250
    y_pos = 700
    buttons = [
        Button("설정", config.WIDTH // 6, y_pos, 280, 280, on_setting, font_size=70),
        Button("게임 시작", config.WIDTH // 2, y_pos, 800, 400, start_game, font_size=90),
        Button("종료", 5 * config.WIDTH // 6, y_pos, 280, 280, quit_game, font_size=70)
    ]

    clock = pygame.time.Clock()

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
        screen.blit(title_image, title_rect)
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
    return result
