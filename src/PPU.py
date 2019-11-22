from Memory import Memory
import pygame
import numpy as np

class PPU():
    def __init__(self):
        
        self.memory = Memory(0, 16 * 1024)
        self.rom_memory = Memory(-8 * 1024, 8 * 1024)

        chr_filename = '/home/previato/Dropbox/Unicamp/MC861/mc861-nesemulator/img/smb.nes'
        self.init_rom_memo(chr_filename)

        self.PPUCTRL_value = 0

        self.PPUADDR_first = True
        self.PPUADDR_value = 0
    
        self.screen_width = 256
        self.screen_height = 256

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
        icon = pygame.image.load('/home/previato/Dropbox/Unicamp/MC861/mc861-nesemulator/img/Controller-512.png')
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

            # pygame.surfarray.blit_array(self.screen, s)
            pygame.surfarray.blit_array(self.screen, self.screen_data)

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
        backgroud_figs = self.rom_memory.read_range_memo(bg_tiles, int('1000', 16))
        backgroud_figs = np.array(backgroud_figs, dtype=np.uint8).reshape(256 * 16, )

        background_nametable_index = self.get_nametable()
        backgroud_list_pos = background_nametable_index * int('400', 16) + int('2000', 16)
        backgroud_attr_pos = backgroud_list_pos + int('3C0', 16)

        backgroud_palette = self.memory.read_range_memo(int('3F00', 16), 16)

        vec_map_palette = np.vectorize(map_palette, excluded=['palette'])

        backgroud_list = []
        for i in range(32):
            for j in range(32):
                backgroud_list.append(backgroud_list_pos + i * 32 + j)

                pattern_table_index = self.memory.read_memo(backgroud_list_pos + i * 32 + j)

                pattern_table_entry = backgroud_figs[pattern_table_index:pattern_table_index + 17]
                attribute_table_entry = self.memory.read_range_memo(backgroud_attr_pos, 64)

                pattern_table = np.zeros(64)
                
                for k in range(64):
                    pattern_table[k] = (pattern_table_entry[k // 4] & (3 << (k % 4) * 2)) / (1 << (k % 4) * 2)
                
                pattern_table = pattern_table.reshape(8, 8)
                stacked_pattern_table = np.stack((pattern_table,)*3, axis=-1)
                print(pattern_table.shape)
                print(stacked_pattern_table.shape)

                attr_byte = attribute_table_entry[(i // 8) * 8 + j // 8]
                
                attr_mask = 0
                if i % 8 >= 4:
                    attr_mask += 2
                if j % 8 >= 4:
                    attr_mask += 1

                attr = (attr_byte & (3 << attr_mask)) / (1 << attr_mask)

                self.screen_data[i*8:i*8 + 8, j*8:j*8 + 8, :] = vec_map_palette(value=(stacked_pattern_table + attr), palette=backgroud_palette)
    
def map_palette(value, palette):
    return palette[int(value)]

if __name__ == "__main__":
    p = PPU()

    p.start()

    p.refresh_background()
    p.render()

    p.quit()
