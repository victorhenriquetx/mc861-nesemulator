import os
import sys
from src.Register import Register8bit, Register16bit, RegisterFlag
from src.Memory import Memory
import src.Methods as methods

_DEBUG = False

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

        elif bin_instruction == int('81', 16): # STA Indirect,X
            # TODO: Check indirect order
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)

            return methods._sta(self, memory_position)

        elif bin_instruction == int('58', 16): # CLI
            return methods._cli(self, None)

        elif bin_instruction == int('D8', 16): # CLD
            return methods._cld(self, None)

        elif bin_instruction == int('B8', 16): # CLV
            return methods._clv(self, None)

        elif bin_instruction == int('C9', 16): # CMP Immediate
            immediate = self.read_memo()
            return methods._cmp(self, immediate, is_immediate=True)

        elif bin_instruction == int('C5', 16): # CMP Zero Page
            zero_position = self.read_memo()
            return methods._cmp(self, zero_position)

        elif bin_instruction == int('D5', 16): # CMP Zero Page,X
            zero_position = self.read_memo() + self.X.value
            return methods._cmp(self, zero_position)

        elif bin_instruction == int('CD', 16): # CMP Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._cmp(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('DD', 16): # CMP Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo() + self.X.value
            return methods._cmp(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('D9', 16): # CMP Absolute,Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo() + self.Y.value
            return methods._cmp(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('C1', 16): # CMP (Indirect,X)
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)
            return methods._cmp(self, memory_position)   

        elif bin_instruction == int('D1', 16): # CMP (Indirect),Y
            indirect_memory = self.read_memo()
            memory_position = self.memory.read_memo(indirect_memory) + self.Y.value
            return methods._cmp(self, memory_position)  

        elif bin_instruction == int('E0', 16): # CPX Immediate
            immediate = self.read_memo()
            return methods._cpx(self, immediate, is_immediate=True)

        elif bin_instruction == int('E4', 16): # CPX Zero Page
            zero_position = self.read_memo()
            return methods._cpx(self, zero_position)

        elif bin_instruction == int('EC', 16): # CPX Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._cpx(self, absolute_position_hi * 256 + absolute_position_lo)
        
        elif bin_instruction == int('C0', 16): # CPY Immediate
            immediate = self.read_memo()
            return methods._cpy(self, immediate, is_immediate=True)

        elif bin_instruction == int('C4', 16): # CPY Zero Page
            zero_position = self.read_memo()
            return methods._cpy(self, zero_position)

        elif bin_instruction == int('CC', 16): # CPY Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._cpy(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('C6', 16): # DEC Zero Page
            zero_position = self.read_memo()
            return methods._dec(self, zero_position)

        elif bin_instruction == int('D6', 16): # DEC Zero Page,X
            zero_position = self.read_memo() + self.X.value
            return methods._dec(self, zero_position)

        elif bin_instruction == int('CE', 16): # DEC Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._dec(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('DE', 16): # DEC Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo() + self.X.value
            return methods._dec(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('CA', 16): # DEX
            return methods._dex(self, None)

        elif bin_instruction == int('88', 16): # DEY
            return methods._dey(self, None)

        elif bin_instruction == int('49', 16): # EOR Immediate
            immediate = self.read_memo()
            return methods._eor(self, immediate, is_immediate=True)

        elif bin_instruction == int('45', 16): # EOR Zero Page
            zero_position = self.read_memo()
            return methods._eor(self, zero_position)

        elif bin_instruction == int('55', 16): # EOR Zero Page,X
            zero_position = self.read_memo() + self.X.value
            return methods._eor(self, zero_position)

        elif bin_instruction == int('4D', 16): # EOR Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._eor(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('5D', 16): # EOR Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo() + self.X.value
            return methods._eor(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('59', 16): # EOR Absolute,Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo() + self.Y.value
            return methods._eor(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('41', 16): # EOR (Indirect,X)
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)
            return methods._eor(self, memory_position)   

        elif bin_instruction == int('51', 16): # EOR (Indirect),Y
            indirect_memory = self.read_memo()
            memory_position = self.memory.read_memo(indirect_memory) + self.Y.value
            return methods._eor(self, memory_position)  

        elif bin_instruction == int('E6', 16): # INC Zero Page
            zero_position = self.read_memo()
            return methods._inc(self, zero_position)

        elif bin_instruction == int('F6', 16): # INC Zero Page,X
            zero_position = self.read_memo() + self.X.value
            return methods._inc(self, zero_position)

        elif bin_instruction == int('EE', 16): # INC Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._inc(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('FE', 16): # INC Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo() + self.X.value
            return methods._inc(self, absolute_position_hi * 256 + absolute_position_lo)
        
        elif bin_instruction == int('E8', 16): # INX
            return methods._inx(self, None)
        
        elif bin_instruction == int('C8', 16): # INY
            return methods._iny(self, None)
        
        elif bin_instruction == int('4C', 16): # JMP Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            return methods._jmp(self, absolute_position_hi * 256 + absolute_position_lo)
        
        elif bin_instruction == int('6C', 16): # JMP Indirect
            # indirect_position points to low indirect value, a subsequent
            # read in the memory for indirect_position + 1 is needed
            # for the memory high position
            indirect_position_hi = self.read_memo()
            indirect_position_lo = self.read_memo()
            
            # Due to 6502 implementations of additions in register
            # if the indirect low value is $FF, the value that will
            # be loaded will be not the expected.

            # For example if address $3000 contains $40, $30FF contains $80, and $3100
            # contains $50, the result of JMP ($30FF) will be a transfer of control to 
            # $4080 rather than $5080 as you intended i.e. the 6502 took the low byte 
            # of the address from $30FF and the high byte from $3000.
            indirect_position_lo_plus_one = indirect_position_lo + 1
            if indirect_position_lo_plus_one > 255:
                indirect_position_lo_plus_one -= 256

            memory_position_lo = self.memory.read_memo(indirect_position_hi * 256 + indirect_position_lo)
            memory_position_hi = self.memory.read_memo(indirect_position_hi * 256 + indirect_position_lo_plus_one)
            return methods._jmp(self, memory_position_hi * 256, memory_position_lo)

        elif bin_instruction == int('00', 16): # BRK
            # TODO: Set flagas and move PC
            return methods._brk(self, 0)

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
