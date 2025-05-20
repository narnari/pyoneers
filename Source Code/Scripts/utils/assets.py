import pygame
import os
from Scripts.utils import config

# 이미지 로딩 함수
def load_image(name, scale=None):
    path = os.path.join(config.IMG_DIR, name)
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# 폰트 로딩 함수
def load_font(name, size):
    path = os.path.join(config.FONT_DIR, name)
    return pygame.font.Font(path, size)

# 사운드 로딩 함수
def load_sound(name):
    path = os.path.join(config.SFX_DIR, name)
    return pygame.mixer.Sound(path)

# # 실제 로딩된 자산 저장
# images = {
#     "tile": load_image("Tile04.png"),
#     "title": load_image("Title.png"),
#     "tree1": load_image("Tree1.png"),
#     "tile_tree1": load_image("Tree1Plant.png"),
#     "tree2": load_image("Tree2.png"),
#     "tile_tree2": load_image("Tree2Plant.png"),
#     "tree3": load_image("Tree3.png"),
#     "tile_tree3": load_image("Tree3Plant.png"),
#     "tree4": load_image("Tree4.png"),
#     "tile_tree4": load_image("Tree4Plant.png"),
#     "ui1": load_image("UI1.png"),
#     "ui2": load_image("UI2.png"),
#     "ui3": load_image("UI3.png"),
#     "back": load_image("back.png"),
#     "tree_button": load_image("button1.png"),
#     "shovel_button": load_image("button2.png"),
#     "manual_button": load_image("button3.png"),
#     "setting_button": load_image("button4.png"),
#     "fire": load_image("fire01.png"),
#     "logo": load_image("logo.png"),
#     "trash": load_image("trash03.png")
# }

# fonts = {
#     "jalnan38": load_font("Jalnan.ttf", 38),
#     "jalnan70": load_font("Jalnan.ttf", 70),
# }

# sounds = {
# }
