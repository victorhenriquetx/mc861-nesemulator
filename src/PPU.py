from Memory import Memory
import pygame


class PPU():
    def __init__(self):
        self.memory = Memory(0, 16)

    def render(self):
        # inicialize the pygame
        pygame.init()

        # create the screen
        screen = pygame.display.set_mode((800, 600))

        # perfumaria
        pygame.display.set_caption("The Best NES ever")
        icon = pygame.image.load('..\\img\\Controller-512.png')
        pygame.display.set_icon(icon)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False