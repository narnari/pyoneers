import pygame
import sys
import ctypes
import game_UI

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

#화면 비율 설정
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, pygame.FULLSCREEN)
pygame.display.set_caption("Tree Planting UI")

#색상
WHITE = (255, 255, 255)
SKY = (220, 245, 255)
GREEN = (57, 150, 82)

#상태: menu
state = "menu"

#타이틀 이미지 불러오고 크기 조정, 위치 설정
title = pygame.image.load("assets/Title.png")
title = pygame.transform.scale(title, (920, 460))
title_rect = title.get_rect(center=(WIDTH // 2, 200))

#버튼 클래스
class Button:
    def __init__(self, text, x, y, width, height, callback, font_size=72):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.rect.center = (x, y)
        self.font = pygame.font.Font("fonts/Jalnan.ttf", font_size)

    def draw(self, surface):
        center = self.rect.center
        radius = self.rect.width // 2
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=center)

        if self.text == "게임 시작":
            pygame.draw.ellipse(surface, GREEN, self.rect)
            pygame.draw.ellipse(surface, GREEN, self.rect, 4)
        else:
            pygame.draw.circle(surface, GREEN, center, radius)
            pygame.draw.circle(surface, GREEN, center, radius, 4)

        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            dx = event.pos[0] - self.rect.centerx
            dy = event.pos[1] - self.rect.centery
            if (dx**2 + dy**2)**0.5 <= self.rect.width // 2:
                self.callback()

def start_game():
    global state
    state = "game"

def open_settings(): print("설정!")

def quit_game():
    pygame.quit()
    sys.exit()

def go_to_menu():
    global state
    state = "menu"

button_size = 250
y_pos = 700
buttons = [
    Button("설정", WIDTH // 6, y_pos, 280, 280, open_settings, font_size=70),
    Button("게임 시작", WIDTH // 2, y_pos, 800, 400, start_game, font_size=90),
    Button("종료", 5 * WIDTH // 6, y_pos, 280, 280, quit_game, font_size=70)
]

clock = pygame.time.Clock()

# Main loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == "menu":
            for button in buttons:
                button.handle_event(event)

    if state == "menu":
        screen.fill(SKY)
        screen.blit(title, title_rect)
        for button in buttons:
            button.draw(screen)
    elif state == "game":
        game_result = game_UI.main(screen)
        if game_result == "menu":
            state = "menu"
        elif game_result == "exit":
            running = False  # 직접 종료

    pygame.display.flip()

pygame.quit()
sys.exit()