from PPU import PPU

p = PPU()

p.start()

p.refresh_background()
p.render()

p.quit()

# print(p.rom_memory.mem[:100])