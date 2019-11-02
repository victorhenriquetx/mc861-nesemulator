from Memory import Memory
import pygame
import numpy as np

class PPU():
    def __init__(self):
        
        self.memory = Memory(0, 16 * 1024)
        self.rom_memory = Memory(0, 8 * 1024)

        chr_filename = '../img/mario.chr'
        self.init_rom_memo(chr_filename)

        self.PPUCTRL_value = 0

        self.PPUADDR_first = True
        self.PPUADDR_value = 0
    
        self.screen_width = 256*2
        self.screen_height = 256*2

        self.screen_data = np.zeros((self.screen_width, self.screen_height, 3))
    
    def init_rom_memo(self, chr_filename):
        self.rom_memory.read_file(chr_filename)
    
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

    def get_nametable(self):
        return self.PPUCTRL_value & 3
    
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
        icon = pygame.image.load('../img/Controller-512.png')
        pygame.display.set_icon(icon)
    
    def quit(self):
        pygame.quit()

    def render(self):
        running = True
        
        s = np.zeros((self.screen_width, self.screen_height, 3))
        s[:] = (255, 0, 0)
        s[:40] = (255, 255, 0)


        s[:64, :64, 0] = np.array(self.rom_memory.mem[:int('1000', 16)]).reshape(64, 64)
        while running:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    running = False
            # self.screen.blit(surf, (0, 0))

            pygame.surfarray.blit_array(self.screen, s)

            pygame.display.update()


    def update(self, x, y, width, height, color=(0,0,0)):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.display.update()

    def render_frame(self, memory:Memory, memory_position):
        for i in range(64):
            y = memory.read_memo(memory_position + i)
            p_tile = memory.read_memo(memory_position + i)
            p_color = memory.read_memo(memory_position + i)
            x = memory.read_memo(memory_position + i)
            
            tile = x
            # for pixel in 
            self.update(x, y, 1, 1, color)

    def refresh_background(self):
        bg_tiles = self.background_pattern_table()
        backgroud_figs = self.memory.read_range_memo(bg_tiles, int('1000', 16))
        backgroud_figs = np.array(backgroud_figs, dtype=np.uint8).reshape(256, )

        background_list_index = self.get_nametable()
        backgroud_list_pos = background_list_index * int('400', 16) + int('2000', 16)

        backgroud_list = []
        for i in range(32):
            for j in range(30):
                backgroud_list.append(backgroud_list_pos + i * 30 + j)

                self.screen_data[i*8:i*8 + 8, j*8:j*8 + 8] = 


