import os
import sys
from src.Register import Register8bit, Register16bit, RegisterFlag
from src.Memory import Memory
import src.Methods as methods

class Processor():
    def __init__(self, filename):
        self.filename = filename

        self.X = Register8bit()
        self.Y = Register8bit()
        self.A = Register8bit()
        self.STACK = Register8bit()
        self.FLAGS = RegisterFlag()
        
        self.PC = Register16bit()

        self.memory = Memory(10)
        self.memory.read_file(self.filename)

    def emula(self, init_pos):
        # Emulation Loop
        while True:
            instruction = self.read_memo()

            # Log instruction - ONLY FOR TESTING PURPOSES
            # print('| instruction = ' + hex(instruction), end = ' ')

            # Log registers
            print('| pc = ' + hex(self.PC.value), end = ' ')
            print('| a = ' + hex(self.A.value), end = ' ')
            print('| x = ' + hex(self.X.value), end = ' ')
            print('| y = ' + hex(self.Y.value), end = ' ')
            print('| sp = ' + hex(self.STACK.value), end = ' ')
            print('| p[NV-BDIZC] = ' + str(self.FLAGS.get_N()) + str(self.FLAGS.get_V()) + '1' + str(self.FLAGS.get_B()) + str(self.FLAGS.get_D()) + str(self.FLAGS.get_I()) + str(self.FLAGS.get_Z()) + str(self.FLAGS.get_C()), end = '')

            # TODO: Check PC increment overflow

            self.decode_instruction(instruction)

            # Finishes log print (there may be memory logs while decoding specific instructions)
            print(' |')

            err = ""
            self.log(err)
            
    # TODO implementar funcoes auxiliares
    def read_memo(self):
        readed_value = self.memory.read_memo(self.PC.value)
        self.PC.increment()

        return readed_value

    def decode_instruction(self, bin_instruction):
        # converte byte para string no formato do which_instruction
        # verificar qual a instrução e decidir quantos bytes a mais vai ter que ler (usando o read_memo)
        # cada instrução pode ter de 1 a 3 bytes (instrução no primeiro byte e valores no segundo/terceiro)

        if bin_instruction == int('69', 16): # ADC Immediate
            immediate = self.read_memo()
            return methods._adc(self, immediate)
        
        elif bin_instruction == int('AD', 16): # LDA Absolute
            # TODO: Check if the HI/LOW order is right
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._lda(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('BD', 16): # LDA Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._lda(self, absolute_position_hi * 256 + absolute_position_lo + self.X.value)

        elif bin_instruction == int('81', 16): # STA Indirect,X
            # TODO: Check indirect order
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)

            return methods._sta(self, memory_position)

        elif bin_instruction == int('00', 16): # BRK
            # TODO: Set flagas and move PC
            return methods._brk(self, 0)

        else:
            # TODO: Add error to log
            return methods._brk(self, 1)


    def log(self, err):
        return ""

def main():
    filename = sys.argv[1]
    processor = Processor(filename)
    processor.emula(0)

if __name__ == "__main__":
    main()
