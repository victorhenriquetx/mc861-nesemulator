import os
import sys
from src.Register import Register8bit, Register16bit, RegisterFlag
from src.Memory import Memory
from src.Decoder import Decoder
from src.HashFunctions import HashInstructions
import src.Methods as methods

_DEBUG = True

class Processor():
    def __init__(self, filename):
        self.filename = filename

        self.X = Register8bit()
        self.Y = Register8bit()
        self.A = Register8bit()
        self.STACK = Register8bit(int('ff', 16))
        self.FLAGS = RegisterFlag()
        
        self.header = Memory(0,16)
        self.memory = Memory(16,-1)
        self.header.read_file(self.filename)
        self.memory.read_file(self.filename)

        start_pc_addr_lo = self.memory.read_memo(int('fffc', 16))
        start_pc_addr_hi = self.memory.read_memo(int('fffd', 16))
        self.PC = Register16bit(start_pc_addr_hi*256 + start_pc_addr_lo)
        self.fake_PC = Register16bit(self.PC.value)

        self.print_mem = ''

        self.decoder = Decoder(self)
        self.hash_instructions = HashInstructions(self.decoder)

    def emula(self, init_pos):
        # Emulation
        while True:
            self.fake_PC.value = self.PC.value
            instruction = self.read_memo_pc()
            decode = self.decode_instruction(instruction)
            self.print_log()

    # TODO implementar funcoes auxiliares
    def read_memo_pc(self):
        readed_value = self.memory.read_memo(self.PC.value)
        self.PC.increment()
        return readed_value

    def read_immediate(self):
        immediate = self.read_memo_pc()
        return immediate
    
    def read_relative(self):
        value = self.read_memo_pc()
        branch_increment = 127 - value if value > 127 else value
        return branch_increment
    
    def read_zero_page(self):
        zero_position = self.read_memo_pc()
        return zero_position
    
    def read_zero_page_x(self):
        zero_position_x = self.read_memo_pc() + self.X.value
        return zero_position_x
    
    def read_zero_page_y(self):
        zero_position_y = self.read_memo_pc() + self.Y.value
        return zero_position_y
    
    def read_absolute(self):
        absolute_position_lo = self.read_memo_pc()
        absolute_position_hi = self.read_memo_pc()
        absolute_position = absolute_position_hi * 256 + absolute_position_lo

        return absolute_position
    
    def read_absolute_x(self):
        absolute_position_lo = self.read_memo_pc() + self.X.value
        absolute_position_hi = self.read_memo_pc()
        absolute_position = absolute_position_hi * 256 + absolute_position_lo

        return absolute_position

    def read_absolute_y(self):
        absolute_position_lo = self.read_memo_pc() + self.Y.value
        absolute_position_hi = self.read_memo_pc()
        absolute_position = absolute_position_hi * 256 + absolute_position_lo

        return absolute_position
    
    def read_indirect_x(self):
        indirect_memory = self.read_memo_pc() + self.X.value
        
        memory_position = self.memory.read_memo(indirect_memory)
        value_lo = self.memory.read_memo(memory_position)
        value_hi = self.memory.read_memo(memory_position + 1)
        final_memory = value_hi * 256 + value_lo

        return final_memory, memory_position
    
    def read_indirect_y(self):
        indirect_memory = self.read_memo_pc()
        
        memory_position = self.memory.read_memo(indirect_memory) + self.Y.value
        value_lo = self.memory.read_memo(memory_position)
        value_hi = self.memory.read_memo(memory_position + 1)
        final_memory = value_hi * 256 + value_lo

        return final_memory, memory_position

    def decode_instruction(self, bin_instruction):
        self.hash_instructions[bin_instruction]()

    def mem_print(self,memory_position,value):
        self.print_mem = ' MEM['+str(hex(memory_position))+'] = ' + str(hex(value)) + ' |'

    def print_log(self):
        print('| pc = ' + hex(self.fake_PC.value) + ' | a = ' + hex(self.A.value) + ' | x = ' + hex(self.X.value) + ' | y = ' + hex(self.Y.value) + ' | sp = ' + hex(self.STACK.value) +' | p[NV-BDIZC] = ' + str(self.FLAGS.is_N()) + str(self.FLAGS.is_V()) + '1' + str(self.FLAGS.is_B()) + str(self.FLAGS.is_D()) + str(self.FLAGS.is_I()) + str(self.FLAGS.is_Z()) + str(self.FLAGS.is_C()) + ' |' + self.print_mem)
        self.print_mem = ''

def main():
    filename = sys.argv[1]
    processor = Processor(filename)
    processor.emula(0)

if __name__ == "__main__":
    main()
