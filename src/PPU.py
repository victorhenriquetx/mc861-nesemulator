from Memory import Memory
import pygame
import numpy as np

class PPU():
    def __init__(self):
        
        self.rom_memory = Memory(0, 16*1024)

        # chr_filename = ''
        # self.init_rom_memo(chr_filename)

        self.PPUCTRL_value = 0

        self.PPUADDR_first = True
        self.PPUADDR_value = 0

        self._adjust = 2

        self.screen_width = 256 * self._adjust
        self.screen_height = 256 * self._adjust

        self.screen_data = np.zeros((self.screen_width, self.screen_height, 3))
    
    def init_rom_memo(self, chr_filename):
        self.rom_memory.read_file(chr_filename)
    
    def get_nametable(self):
        return self.PPUCTRL_value & 3
    
    def PPUADDR_signal(self, value):
        if self.PPUADDR_first:
            self.PPUADDR_value = 256 * value
        else:
            self.PPUADDR_value += value
        
        self.PPUADDR_first = not self.PPUADDR_first

    def increment_PPUADDR(self):
        if self.PPUCTRL_value & (1 << 2):
            self.PPUADDR_value -= 32
        else:
            self.PPUADDR_value += 1

    def PPUDATA_signal(self, value):
        self.memory.write_memo(self.PPUADDR_value, value)
        self.increment_PPUADDR()

    def background_pattern_table(self):
        if self.PPUCTRL_value & (1 << 4):
            return int('1000', 16)
        else:
            return 0

    def sprite_pattern_table(self):
        if self.PPUCTRL_value & (1 << 3):
            return int('1000', 16)
        else:
            return 0

    def start(self):
        # inicialize the pygame
        pygame.init()

        # create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 24)

        # perfumaria
        pygame.display.set_caption("The Best NES ever")
        icon = pygame.image.load('..\\img\\Controller-512.png')
        pygame.display.set_icon(icon)
    
    def quit(self):
        pygame.quit()

    def render(self):
        running = True
        
        s = np.zeros((self.screen_width, self.screen_height, 3))
        s[:] = (255, 0, 0)
        s[:40] = (255, 255, 0)
        while running:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    running = False
            # self.screen.blit(surf, (0, 0))

            pygame.surfarray.blit_array(self.screen, s)

            pygame.display.update()


    def update():
        # pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.surfarray.blit_array(self.screen, self.screen_data)
        pygame.display.update()

    def render_frame(self, memory:Memory, memory_position):
        for i in range(64):
            y = self.memory.read_memo(memory_position + i)
            tile_index = self.memory.read_memo(memory_position + i + 1)
            p_color = self.memory.read_memo(memory_position + i + 2)
            x = self.memory.read_memo(memory_position + i + 3)
            
            tile_pointer = tile_index * (8*8)
            tile_raw = self.memory.read_memo(tile_pointer)
            
            attrt_table = self.get_nametable() * int('400', 16) + int('23c0', 16)

            tile = tile_raw + self.memory.read_memo()


            # self.screen_data[y*4:y*4+4][x*4:x*4+4]
    
            self.update()