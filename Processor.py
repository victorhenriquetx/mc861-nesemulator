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
            debug_print('| ' + 'pc = ' + hex(self.PC.value) + ' | ' + 'a = ' + hex(self.A.value) + ' | ' + 'x = ' + hex(self.X.value)+ ' | ' + 'y = ' + hex(self.Y.value)+ ' | ' + 'sp = ' + hex(self.STACK.value)+ ' | ' + 'p[NV-BDIZC] = ' + hex(self.FLAGS.value) + ' | ')
            # debug_print('Memory:', [hex(hex_v) for hex_v in self.memory.mem])
            instruction = self.read_memo()

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

        #---------------------- ADC Instruction----------------------------------
        if bin_instruction == int('69', 16): # ADC Immediate
            value = self.read_memo() #immediate
            return methods._adc(self, value)

        elif bin_instruction == int('65', 16): # ADC Zero Page
            zero_position = self.read_memo()
            value = self.memory.read_memo(zero_position)
            return methods._adc(self, value)

        elif bin_instruction == int('75', 16): # ADC Zero Page,X
            zero_position = self.read_memo() + self.X.value
            value = self.memory.read_memo(zero_position)
            return methods._adc(self, value)

        elif bin_instruction == int('6D', 16): # ADC Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._adc(self,value)

        elif bin_instruction == int('7D', 16): # ADC Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.X.value)
            return methods._adc(self, value)

        elif bin_instruction == int('79', 16): # ADC Absolute,Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.Y.value)
            return methods._adc(self, value)   

        elif bin_instruction == int('61', 16): # ADC Indirect,X
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)
            value = self.memory.read_memo(memory_position)
            return methods._adc(self, value)   

        elif bin_instruction == int('71', 16): # ADC Indirect,Y
            indirect_memory = self.read_memo()
            memory_position = self.memory.read_memo(indirect_memory) + self.Y.value
            value = self.memory.read_memo(memory_position)
            return methods._adc(self, value)

        #---------------------- AND Instruction----------------------------------
        if bin_instruction == int('29', 16): # AND Immediate
            value = self.read_memo() #immediate
            return methods._and(self, value)

        elif bin_instruction == int('25', 16): # AND Zero Page
            zero_position = self.read_memo()
            value = self.memory.read_memo(zero_position)
            return methods._and(self, value)

        elif bin_instruction == int('35', 16): # AND Zero Page,X
            zero_position = self.read_memo() + self.X.value
            value = self.memory.read_memo(zero_position)
            return methods._and(self, value)

        elif bin_instruction == int('2D', 16): # AND Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._and(self,value)

        elif bin_instruction == int('3D', 16): # AND Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.X.value)
            return methods._and(self, value)

        elif bin_instruction == int('39', 16): # AND Absolute,Y
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.Y.value)
            return methods._and(self, value)   

        elif bin_instruction == int('21', 16): # AND Indirect,X
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)
            value = self.memory.read_memo(memory_position)
            return methods._and(self, value)   

        elif bin_instruction == int('31', 16): # AND Indirect,Y
            indirect_memory = self.read_memo()
            memory_position = self.memory.read_memo(indirect_memory) + self.Y.value
            value = self.memory.read_memo(memory_position)
            return methods._and(self, value)

        #---------------------- AND Instruction----------------------------------
        if bin_instruction == int('0A', 16): # ASL Accumulator
            return methods._asl(self, self.A)

        elif bin_instruction == int('06', 16): # ASL Zero Page
            zero_position = self.read_memo()
            value = self.memory.read_memo(zero_position)
            return methods._asl(self, value)

        elif bin_instruction == int('16', 16): # ASL Zero Page,X
            zero_position = self.read_memo() + self.X.value
            value = self.memory.read_memo(zero_position)
            return methods._asl(self, value)

        elif bin_instruction == int('0E', 16): # ASL Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._asl(self,value)

        elif bin_instruction == int('1E', 16): # ASL Absolute,X
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.X.value)
            return methods._asl(self, value)
        
        #---------------------- BIT Instruction-------------------------------------
        elif bin_instruction == int('24', 16): # BIT Zero Page
            zero_position = self.read_memo()
            value = self.memory.read_memo(zero_position)
            return methods._bit(self, value)
        elif bin_instruction == int('2C', 16): # BIT Absolute
            absolute_position_hi = self.read_memo()
            absolute_position_lo = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._bit(self,value)    
        
        #---------------------- Branch Instruction---------------------------------- 
        elif bin_instruction == int('10', 16):
            label_position = self.read_memo()
            return methods._bpl(self, label_position)
        elif bin_instruction == int('30', 16):
            label_position = self.read_memo()
            return methods._bmi(self, label_position)
        elif bin_instruction == int('50', 16):
            label_position = self.read_memo()
            return methods._bvc(self, label_position)
        elif bin_instruction == int('70', 16):
            label_position = self.read_memo()
            return methods._bvs(self, label_position)
        elif bin_instruction == int('90', 16):
            label_position = self.read_memo()
            return methods._bcc(self, label_position)
        elif bin_instruction == int('B0', 16):
            label_position = self.read_memo()
            return methods._bcs(self, label_position)
        elif bin_instruction == int('D0', 16):
            label_position = self.read_memo()
            return methods._bne(self, label_position)
        elif bin_instruction == int('F0', 16):
            label_position = self.read_memo()
            return methods._beq(self, label_position)


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


def debug_print(args):
    if _DEBUG:
        print(args)

def main():
    filename = sys.argv[1]
    processor = Processor(filename)
    processor.emula(0)

if __name__ == "__main__":
    main()
