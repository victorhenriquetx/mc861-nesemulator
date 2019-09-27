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

        elif bin_instruction == int('81', 16): # STA Indirect,X
            # TODO: Check indirect order
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)

            return methods._sta(self, memory_position)

        elif bin_instruction == int('00', 16): # BRK
            # TODO: Set flagas and move PC
            return methods._brk(self, 0)

        # ********************** Third Line - Willian Hayashida ******************************************************    
        elif bin_instruction == int('20', 16): # JSR
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()

            address = absolute_position_hi * 256 + absolute_position_lo + self.X.value
            next_instruction =  self.PC.value + 1
            return methods._jsr(self, address, next_instruction)

        elif bin_instruction == int('A9', 16): # LDA Immediate
            value = self.read_memo()
            return methods._lda(self, value, immediate=True)
        
        elif bin_instruction == int('A5', 16): # LDA zero page
            absolute_position_lo = self.read_memo()
            return methods._lda(self, absolute_position_lo)

        elif bin_instruction == int('B5', 16): # LDA zero page, X
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_lo + self.X.value
            return methods._lda(self, memory_position)

        elif bin_instruction == int('AD', 16): # LDA Absolute
            # TODO: Check if the HI/LOW order is right
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._lda(self, memory_position)

        elif bin_instruction == int('BD', 16): # LDA Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position =  absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._lda(self, memory_position)

        elif bin_instruction == int('B9', 16): # LA Absolute, Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position =  absolute_position_hi * 256 + absolute_position_lo + self.Y.value
            return methods._lda(self, memory_position)
        
        elif bin_instruction == int('A1', 16): # LDA Indirect, X
            pass
        
        elif bin_instruction == int('B1', 16): # LDA Indirect, Y
            pass
        # LDX A2, A6, B6, AE, BE
        elif bin_instruction == int('A2', 16): # LDX Immediate
            value = self.read_memo()
            return methods._ldx(self, value, immediate=True)

        elif bin_instruction == int('A6', 16): # LDX Zero Page
            absolute_position_lo = self.read_memo()
            return methods._ldx(self, absolute_position_lo)

        elif bin_instruction == int('B6', 16): # LDX Zero Page, Y
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_lo + self.Y.value
            return methods._ldx(self, memory_position)

        elif bin_instruction == int('AE', 16): # LDX Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ldx(self, memory_position)

        elif bin_instruction == int('BE', 16): # LDX Absolute, Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo + self.Y.value
            return methods._ldx(self, memory_position)
            
# Immediate     LDY #$44      $A0  2   2
# Zero Page     LDY $44       $A4  2   3
# Zero Page,X   LDY $44,X     $B4  2   4
# Absolute      LDY $4400     $AC  3   4
# Absolute,X    LDY $4400,X   $BC  3   4+
# LDX A2, A6, B6, AE, BE

        elif bin_instruction == int('A0', 16): # LDY Zero Page
            value = self.read_memo()
            return methods._ldy(self, value, immediate=True)

        elif bin_instruction == int('A4', 16): # LDY Zero Page
            absolute_position_lo = self.read_memo()
            return methods._ldy(self, absolute_position_lo)

        elif bin_instruction == int('B4', 16): # LDY Zero Page, X
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_lo + self.Y.value
            return methods._ldy(self, memory_position)

        elif bin_instruction == int('AC', 16): # LDY Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ldy(self, memory_position)

        elif bin_instruction == int('BC', 16): # LDY Absolute, X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._ldy(self, memory_position)

# Accumulator   LSR A         $4A  1   2
# Zero Page     LSR $44       $46  2   5
# Zero Page,X   LSR $44,X     $56  2   6
# Absolute      LSR $4400     $4E  3   6
# Absolute,X    LSR $4400,X   $5E  3   7
        elif bin_instruction == int('4A', 16): # LSR A
            return methods._lsr(self, 'A')
        elif bin_instruction == int('46', 16): # LSR Zero Page
            absolute_position_lo = self.read_memo()
            return methods._lsr(self, absolute_position_lo)

        elif bin_instruction == int('56', 16): # LSR Zero Page, X
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_lo + self.Y.value
            return methods._lsr(self, memory_position)

        elif bin_instruction == int('4E', 16): # LSR Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._lsr(self, memory_position)

        elif bin_instruction == int('5E', 16): # LSR Absolute, X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._lsr(self, memory_position)
        
        # NOP
        elif bin_instruction == int('EA', 16): # NOP
            return methods._nop()

# Immediate     ORA #$44      $09  2   2
# Zero Page     ORA $44       $05  2   3
# Zero Page,X   ORA $44,X     $15  2   4
# Absolute      ORA $4400     $0D  3   4
# Absolute,X    ORA $4400,X   $1D  3   4+
# Absolute,Y    ORA $4400,Y   $19  3   4+
# Indirect,X    ORA ($44,X)   $01  2   6
# Indirect,Y    ORA ($44),Y   $11  2   5+
        elif bin_instruction == int('09', 16): # ORA Immediate
            value = self.read_memo()
            return methods._ora(self, value, immediate=True)
        
        elif bin_instruction == int('05', 16): # ORA zero page
            absolute_position_lo = self.read_memo()
            return methods._ora(self, absolute_position_lo)

        elif bin_instruction == int('15', 16): # ORA zero page, X
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_lo + self.X.value
            return methods._ora(self, memory_position)

        elif bin_instruction == int('0D', 16): # ORA Absolute
            # TODO: Check if the HI/LOW order is right
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ora(self, memory_position)

        elif bin_instruction == int('1D', 16): # ORA Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position =  absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._ora(self, memory_position)

        elif bin_instruction == int('19', 16): # LA Absolute, Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position =  absolute_position_hi * 256 + absolute_position_lo + self.Y.value
            return methods._ora(self, memory_position)
        
        elif bin_instruction == int('01', 16): # ORA Indirect, X
            pass
        
        elif bin_instruction == int('11', 16): # ORA Indirect, Y
            pass

        # PHA (Push Acc)
        elif bin_instruction == int('48', 16): # Push Accumulator
            return methods._pha(self)
        # PLA (Pop Acc)
        elif bin_instruction == int('68', 16): # Pop Accumulator
            return methods._pla(self)
        # PHP (Push Processor) 
        elif bin_instruction == int('08', 16): # Push Flags
            return methods._php(self)
        # PLP (Pop Processor)
        elif bin_instruction == int('28', 16): # Pop Flags
            return methods._plp(self)
# Accumulator   ROL A         $2A  1   2
# Zero Page     ROL $44       $26  2   5
# Zero Page,X   ROL $44,X     $36  2   6
# Absolute      ROL $4400     $2E  3   6
# Absolute,X    ROL $4400,X   $3E  3   7
        # ROL
        elif bin_instruction == int('2A', 16): # ROL A
            return methods._rol(self, 'A')
        elif bin_instruction == int('26', 16): # ROL Zero Page
            absolute_position_lo = self.read_memo()
            return methods._rol(self, absolute_position_lo)

        elif bin_instruction == int('36', 16): # ROL Zero Page, X
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_lo + self.Y.value
            return methods._rol(self, memory_position)

        elif bin_instruction == int('2E', 16): # ROL Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._rol(self, memory_position)

        elif bin_instruction == int('3E', 16): # ROL Absolute, X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._rol(self, memory_position)   

# Accumulator   ROR A         $6A  1   2
# Zero Page     ROR $44       $66  2   5
# Zero Page,X   ROR $44,X     $76  2   6
# Absolute      ROR $4400     $6E  3   6
# Absolute,X    ROR $4400,X   $7E  3   7
        # ROR
        elif bin_instruction == int('6A', 16): # ROR A
            return methods._ror(self, 'A')
        elif bin_instruction == int('66', 16): # ROR Zero Page
            absolute_position_lo = self.read_memo()
            return methods._ror(self, absolute_position_lo)

        elif bin_instruction == int('76', 16): # ROR Zero Page, X
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_lo + self.Y.value
            return methods._ror(self, memory_position)

        elif bin_instruction == int('6E', 16): # ROR Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ror(self, memory_position)

        elif bin_instruction == int('7E', 16): # ROR Absolute, X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._ror(self, memory_position) 

        elif bin_instruction == int('40', 16): # ROR Absolute, X
            return methods._rti(self)

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
