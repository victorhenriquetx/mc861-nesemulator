import os
import sys
from src.Register import Register8bit, Register16bit, RegisterFlag
from src.Memory import Memory
import src.Methods as methods

_DEBUG = True

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

            # TODO: Check PC increment overflow

            self.decode_instruction(instruction)

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

        elif bin_instruction == int('00', 16): # BRK
            # TODO: Set flagas and move PC
            return methods._brk(self, 0)

        elif bin_instruction == int('60', 16): # RTS
            absolute_position_hi = self.memory.pop_stack(self.STACK)
            absolute_position_lo = self.memory.pop_stack(self.STACK)
            return methods._rts(self, absolute_position_hi * 256 + absolute_position_lo +1)

        #TODO: SBC

        elif bin_instruction == int('38', 16): # SEC
            return methods._sec(self)

        elif bin_instruction == int('F8', 16): # SED
            return methods._sed(self)

        elif bin_instruction == int('78', 16): # SEI
            return methods._sei(self)

        elif bin_instruction == int('85', 16): # STA Zero Page
            memory_position = self.read_memo()
            return methods._sta(self, memory_position)

        elif bin_instruction == int('95', 16): # STA Zero Page, X
            memory_position = self.read_memo()
            return methods._sta(self, memory_position + self.X.value)

        elif bin_instruction == int('8D', 16): # STA Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._sta(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('9D', 16): # STA Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._sta(self, absolute_position_hi * 256 + absolute_position_lo + self.X.value)

        elif bin_instruction == int('99', 16): # STA Absolute,Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._sta(self, absolute_position_hi * 256 + absolute_position_lo + self.Y.value)

        elif bin_instruction == int('81', 16): # STA Indirect,X
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)
            return methods._sta(self, memory_position)

        elif bin_instruction == int('91', 16): # STA Indirect,Y
            indirect_memory = self.read_memo() + self.Y.value
            memory_position = self.memory.read_memo(indirect_memory)
            return methods._sta(self, memory_position)

        elif bin_instruction == int('86', 16): # STX Zero Page
            memory_position = self.read_memo()
            return methods._stx(self, memory_position)

        elif bin_instruction == int('96', 16): # STX Zero Page, Y
            memory_position = self.read_memo()
            return methods._stx(self, memory_position + self.Y.value)

        elif bin_instruction == int('8E', 16): # STX Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._stx(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('84', 16): # STY Zero Page
            memory_position = self.read_memo()
            return methods._sty(self, memory_position)

        elif bin_instruction == int('94', 16): # STY Zero Page, X
            memory_position = self.read_memo()
            return methods._sty(self, memory_position + self.X.value)

        elif bin_instruction == int('8C', 16): # STY Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._sty(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('AA', 16): # TAX
            return methods._tax(self)

        elif bin_instruction == int('A8', 16): # TAY
            return methods._tay(self)

        elif bin_instruction == int('BA', 16): # TSX
            methods._tsx(self)

        elif bin_instruction == int('9A', 16): # TXS
            methods._txs(self)

        elif bin_instruction == int('8A', 16): # TXA
            return methods._txa(self)
        
        elif bin_instruction == int('98', 16): # TYA
            return methods._tya(self)

        else:
            # TODO: Add error to log
            return methods._brk(self, 1)


    def log(self, err):
        return ""


def debug_print(*args):
    if _DEBUG:
        print(args)

def main():
    filename = sys.argv[1]
    processor = Processor(filename)
    processor.emula(0)

if __name__ == "__main__":
    main()
