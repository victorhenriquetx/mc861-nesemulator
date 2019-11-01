from Memory import Memory
import pygame


class PPU():
    def __init__(self):
        self.memory = Memory(0, 16)

    def start(self):
        # inicialize the pygame
        pygame.init()

        # create the screen
        self.screen = pygame.display.set_mode((256, 256))

        # perfumaria
        pygame.display.set_caption("The Best NES ever")
        icon = pygame.image.load('..\\img\\Controller-512.png')
        pygame.display.set_icon(icon)
    
    def quit(self):
        pygame.quit()


    def update(self, x, y, width, height, color=(0,0,0)):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.display.update()

    def render_frame(self, memory:Memory, memory_position):
        for i in range(64):
            y = memory.read_memo(memory_position + i)
            p_tile = memory.read_memo(memory_position + i)
            p_color = memory.read_memo(memory_position + i)
            x = memory.read_memo(memory_position + i)
            
            
            # for pixel in 
            self.update(x, y, 1, 1, color)
