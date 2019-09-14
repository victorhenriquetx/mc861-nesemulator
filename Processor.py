import os
import sys
from src.Register import Register8bit, Register16bit, RegisterFlag
from src.Memory import Memory

_DEBUG = True

class Processor():
    def __init__(self, filename):
        self.filename = filename

        self.X = Register8bit()
        self.Y = Register8bit()
        self.A = Register8bit()
        self.FLAGS = RegisterFlag()
        
        self.PC = Register16bit()

        self.memory = Memory(10)
        self.memory.read_file(self.filename)

    def emula(self, init_pos):
        # Emulation Loop
        while True:
            # Debug registers
            debug_print('======')
            debug_print('X:', hex(self.X.value))
            debug_print('Y:', hex(self.Y.value))
            debug_print('A:', hex(self.A.value))
            debug_print('PC:', hex(self.PC.value))
            debug_print('Memory:', [hex(hex_v) for hex_v in self.memory.mem])
            debug_print('======')

            instruction = self.read_memo()

            # Debug instruction
            debug_print('Instruction', hex(instruction))

            # TODO: Check PC increment oerflow

            decod_instruction, instruction_param = self.decode_instruction(instruction)
            
            decod_instruction(instruction_param)

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
            return self._adc, immediate
        
        elif bin_instruction == int('AD', 16): # LDA Absolute
            # TODO: Check if the HI/LOW order is right
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return self._lda, absolute_position_hi * 256 + absolute_position_lo

        elif bin_instruction == int('BD', 16): # LDA Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return self._lda, absolute_position_hi * 256 + absolute_position_lo + self.X.value

        elif bin_instruction == int('81', 16): # STA Indirect,X
            # TODO: Check indirect order
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)

            return self._sta, memory_position

        elif bin_instruction == int('00', 16): # BRK
            # TODO: Set flagas and move PC
            return self._brk, 0

        else:
            # TODO: Add error to log
            return self._brk, 1


    def log(self, err):
        return ""

    # Instructions
    def _adc(self, instruction_param):
        self.A.value += instruction_param

        if self.A.check_overflow():
            self.A.value -= 255
            self.FLAGS.set_C()
            self.FLAGS.set_V()
        if self.A.is_negative():
            self.FLAGS.set_N()
        if self.A.value == 0:
            self.FLAGS.set_Z()

    def _lda(self, memory_position):
        debug_print(memory_position)
        self.A.value = self.memory.read_memo(memory_position)
        # TODO: Set flags

    def _sta(self, memory_position):
        debug_print(memory_position)
        self.memory.write_memo(memory_position, self.A.value)
        # TODO: Set flags

    def _brk(self, exit_status):
        print("Exit with status", exit_status)
        sys.exit(exit_status)

def debug_print(*args):
    if _DEBUG:
        print(args)

def main():
    filename = sys.argv[1]

    processor = Processor(filename)
    processor.emula(0)

if __name__ == "__main__":
    main()
