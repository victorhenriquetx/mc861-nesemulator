from Memory import Memory
import pygame
import numpy as np

from Register import Register8bit, Register16bit

class PPU():
    def __init__(self, cpu_memory):
        self.memory = Memory(0, 16* 1024)
        self.rom_memory = Memory(-8 * 1024, 8 * 1024)

        chr_filename = '/home/previato/Dropbox/Unicamp/MC861/mc861-nesemulator/img/smb.nes'
        self.init_rom_memo(chr_filename)

        self.PPUCTRL_value = 0

        self.CPU_memory = cpu_memory
        
        self.PPUCTRL = int('2000', 16)
        self.PPUMASK = int('2001', 16)
        self.PPUSTATUS = int('2002', 16)
        self.OAMADDR = int('2003', 16)
        self.OAMDTA = int('2004', 16)
        self.PPUSCROLL = int('2005', 16)
        self.PPUADDR = int('2006', 16)
        self.PPUDATA = int('2007', 16)
        self.OAMDMA = int('4014', 16)

        self._bit_pointer = 0
        self.PPU_pointer = Register16bit()
    
        self.screen_width = 256
        self.screen_height = 256

        self.screen_data = np.zeros((self.screen_width, self.screen_height, 3))
    
    def init_rom_memo(self, chr_filename):
        self.rom_memory.read_file(chr_filename)
    

    def set_PPUCTRL(self, value):
        self.PPUCTRL = value
        if self._bit_pointer % 2:
            self.PPU_pointer.set_value(self.PPU_pointer.value + value)
        else:
            self.PPU_pointer.set_value(value * 256)
        self._bit_pointer += 1

    def set_PPUMASK(self, value):
        self.PPUMASK = value
    def set_PPUSTATUS(self, value):
        self.PPUSTATUS = value
    def set_OAMADDR(self, value):
        self.OAMADDR = value
    def set_OAMDTA(self, value):
        self.OAMDTA = value
    def set_PPUSCROLL(self, value):
        self.PPUSCROLL = value
    def set_PPUADDR(self, value):
        self.PPUADDR = value
    def set_PPUDATA(self, value):
        self.PPUDATA = value
    def set_OAMDMA(self, value):
        self.OAMDMA =  value

    def get_PPUMASK(self, value):
        return self.CPU_memory.read_memo(self.PPUMASK)
    def get_PPUSTATUS(self, value):
        return self.CPU_memory.read_memo(self.PPUSTATUS)
    def get_OAMADDR(self, value):
        return self.CPU_memory.read_memo(self.OAMADDR)
    def get_OAMDTA(self, value):
        return self.CPU_memory.read_memo(self.OAMDTA)
    def get_PPUSCROLL(self, value):
        return self.CPU_memory.read_memo(self.PPUSCROLL)
    def get_PPUADDR(self, value):
        return self.CPU_memory.read_memo(self.PPUADDR)
    def get_PPUDATA(self, value):
        return self.CPU_memory.read_memo(self.PPUDATA)
    def get_OAMDMA(self, value):
        return self.CPU_memory.read_memo(self.OAMDMA)

    def PPUDATA_signal(self, value):
        self.memory.write_memo(self.PPU_pointer, value)
        self.increment_PPUADDR()
    
    def increment_PPUADDR(self):
        if self.PPU_pointer & (1 << 2):
            self.PPU_pointer -= 32
        else:
            self.PPU_pointer += 1

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

                self.screen_data[i*8:i*8 + 8, j*8:j*8 + 8, :] = stacked_pattern_table + attr

if __name__ == "__main__":
    p = PPU()

    p.start()

    p.refresh_background()
    p.render()

    p.quit()
