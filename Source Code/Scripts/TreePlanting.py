import pygame
from pygame.locals import *

class TreePlanter:
    def __init__(self, screen, tile_map, tile_size):
        self.screen = screen
        self.tile_map = tile_map
        self.tile_size = tile_size
        self.running = True
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        """Run tree planting mode"""
        instructions = self.font.render("Click on open land to plant a tree (ESC to cancel)", True, (0, 0, 0))
        
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return None
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        pos = self.plant_tree(event.pos)
                        if pos:
                            return pos
            
            self.draw_planting_mode()
            self.screen.blit(instructions, (20, 20))
            pygame.display.flip()
        
        return None
    
    def plant_tree(self, pos):
        """Returns (row, col) if planted successfully, None otherwise"""
        col = pos[0] // self.tile_size
        row = pos[1] // self.tile_size
        
        # Check boundaries and if land is open
        if (0 <= row < len(self.tile_map) and (0 <= col < len(self.tile_map[0])) and self.tile_map[row][col]):
            return (row, col)
        return None
        
    def draw_planting_mode(self):
        """Draw the planting interface"""
        self.screen.fill((220, 245, 255))  # Sky background
        for row in range(len(self.tile_map)):
            for col in range(len(self.tile_map[0])):
                rect = pygame.Rect(col * self.tile_size, row * self.tile_size, 
                                 self.tile_size, self.tile_size)
                color = (200, 255, 200) if self.tile_map[row][col] else (200, 200, 200)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

                # Show small tree preview where mouse hovers over plantable area
                mouse_pos = pygame.mouse.get_pos()
                # if (rect.collidepoint(mouse_pos) and self.tile_map[row][col]):
                #     self.screen.blit(self.tree_img, 
                #               (rect.x + self.tile_size//4, 
                #                rect.y + self.tile_size//4))
        
        # Draw instructions
        text = self.font.render("Click on green areas to plant trees (ESC to cancel)", True, (0, 0, 0))
        self.screen.blit(text, (20, 20))

def run_tree_planting(screen, tile_map, tile_size):
    """Main function to start tree planting mode"""
    planter = TreePlanter(screen, tile_map, tile_size)
    return planter.run()