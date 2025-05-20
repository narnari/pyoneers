# tree_plot_plant.py
import pygame

TREE_BUTTON_SIZE = 200
TREE_MARGIN = 50
TREE_IMAGES = [
    "assets/Tree1.png",
    "assets/Tree2.png",
    "assets/Tree3.png",
    "assets/Tree4.png",
]

def run_tree_planting(screen):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    tree_images = [pygame.transform.scale(pygame.image.load(img), (TREE_BUTTON_SIZE, TREE_BUTTON_SIZE)) for img in TREE_IMAGES]

    buttons = []
    start_x = (screen.get_width() - ((TREE_BUTTON_SIZE + TREE_MARGIN) * len(tree_images) - TREE_MARGIN)) // 2
    y = (screen.get_height() - TREE_BUTTON_SIZE) // 2
    for i, img in enumerate(tree_images):
        rect = pygame.Rect(start_x + i * (TREE_BUTTON_SIZE + TREE_MARGIN), y, TREE_BUTTON_SIZE, TREE_BUTTON_SIZE)
        buttons.append((rect, img, i))

    selected_tree = None
    running = True
    while running:
        screen.fill((200, 255, 200))
        title = font.render("Choose a tree to plant", True, (0, 100, 0))
        screen.blit(title, ((screen.get_width() - title.get_width()) // 2, 50))

        for rect, img, _ in buttons:
            screen.blit(img, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, _, tree_index in buttons:
                    if rect.collidepoint(event.pos):
                        return "plant_tree", tree_index

        clock.tick(60)
