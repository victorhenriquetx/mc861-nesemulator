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
        


        self.header = Memory(0,16)
        self.memory = Memory(16,-1)
        self.header.read_file(self.filename)
        self.memory.read_file(self.filename)
        # print(len(self.memory.mem))
        i_lo = self.memory.read_memo(int('fffc', 16))
        i_hi = self.memory.read_memo(int('fffd', 16))
        i = i_hi*256 + i_lo
        # print(hex(i))
        self.PC = Register16bit(i_hi*256 + i_lo)

    def emula(self, init_pos):
        # Emulation
        while True:
            instruction = self.read_memo()
            # print(instruction)
            # Log instruction - ONLY FOR TESTING PURPOSES
            # print('| instruction = ' + hex(instruction), end = ' ')

            # Log registers
            
            decode = self.decode_instruction(instruction)
            # print(decode)
            
            # Finishes log print (there may be memory logs while decoding specific instructions)
            debug_print('| pc = ' + hex(self.PC.value-1) + ' | a = ' + hex(self.A.value) + ' | x = ' + hex(self.X.value) + ' | y = ' + hex(self.Y.value) + ' | sp = ' + hex(self.STACK.value) +' | p[NV-BDIZC] = ' + str(self.FLAGS.is_N()) + str(self.FLAGS.is_V()) + '1' + str(self.FLAGS.is_B()) + str(self.FLAGS.is_D()) + str(self.FLAGS.is_I()) + str(self.FLAGS.is_Z()) + str(self.FLAGS.is_C()) + ' |')
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
            if zero_position > 255:
                zero_position -= 256
            value = self.memory.read_memo(zero_position)
            return methods._adc(self, value)

        elif bin_instruction == int('6D', 16): # ADC Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._adc(self,value)

        elif bin_instruction == int('7D', 16): # ADC Absolute,X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.X.value)
            return methods._adc(self, value)

        elif bin_instruction == int('79', 16): # ADC Absolute,Y
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._and(self,value)

        elif bin_instruction == int('3D', 16): # AND Absolute,X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.X.value)
            return methods._and(self, value)

        elif bin_instruction == int('39', 16): # AND Absolute,Y
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._asl(self,value)

        elif bin_instruction == int('1E', 16): # ASL Absolute,X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.X.value)
            return methods._asl(self, value)
        
        #---------------------- BIT Instruction-------------------------------------
        elif bin_instruction == int('24', 16): # BIT Zero Page
            zero_position = self.read_memo()
            value = self.memory.read_memo(zero_position)
            return methods._bit(self, value)
        elif bin_instruction == int('2C', 16): # BIT Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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

        # elif bin_instruction == int('A9', 16): # LDA Immediate
        #     immediate = self.read_memo()
        #     return methods._lda(self, immediate, is_immediate=True)

        # elif bin_instruction == int('A5', 16): # LDA Zero Page
        #     zero_position = self.read_memo()
        #     return methods._lda(self, zero_position)

        # elif bin_instruction == int('B5', 16): # LDA Zero Page,X
        #     zero_position = self.read_memo() + self.X.value
        #     return methods._lda(self, zero_position)

        # elif bin_instruction == int('AD', 16): # LDA Absolute
        #     # TODO: Check if the HI/LOW order is right
        #     absolute_position_lo = self.read_memo()
        #     absolute_position_hi = self.read_memo()
        #     return methods._lda(self, absolute_position_hi * 256 + absolute_position_lo)

        # elif bin_instruction == int('BD', 16): # LDA Absolute,X
        #     absolute_position_lo = self.read_memo()
        #     absolute_position_hi = self.read_memo()
        #     return methods._lda(self, absolute_position_hi * 256 + absolute_position_lo + self.X.value)

        elif bin_instruction == int('00', 16): # BRK
            # TODO: Set flagas and move PC
            return methods._brk(self, 0)

        elif bin_instruction == int('60', 16): # RTS
            absolute_position_lo = self.memory.pop_stack(self.STACK)
            absolute_position_hi = self.memory.pop_stack(self.STACK)
            return methods._rts(self, absolute_position_hi * 256 + absolute_position_lo +1)

        if bin_instruction == int('E9', 16): # SBC Immediate
            value = self.read_memo()
            return methods._sbc(self, value)

        elif bin_instruction == int('E5', 16): # SBC Zero Page
            zero_position = self.read_memo()
            value = self.memory.read_memo(zero_position)
            return methods._sbc(self, value)

        elif bin_instruction == int('F5', 16): # SBC Zero Page,X
            zero_position = self.read_memo() + self.X.value
            value = self.memory.read_memo(zero_position)
            return methods._sbc(self, value)

        elif bin_instruction == int('ED', 16): # SBC Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
            return methods._sbc(self,value)

        elif bin_instruction == int('FD', 16): # SBC Absolute,X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.X.value)
            return methods._sbc(self, value)

        elif bin_instruction == int('F9', 16): # SBC Absolute,Y
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            value = self.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo + self.Y.value)
            return methods._sbc(self, value)   

        elif bin_instruction == int('E1', 16): # SBC Indirect,X
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)
            value = self.memory.read_memo(memory_position)
            return methods._sbc(self, value)   

        elif bin_instruction == int('F1', 16): # SBC Indirect,Y
            indirect_memory = self.read_memo()
            memory_position = self.memory.read_memo(indirect_memory) + self.Y.value
            value = self.memory.read_memo(memory_position)
            return methods._sbc(self, value)

        elif bin_instruction == int('38', 16): # SEC
            return methods._sec(self)

        elif bin_instruction == int('F8', 16): # SED
            return methods._sed(self)

        elif bin_instruction == int('78', 16): # SEI
            return methods._sei(self)

        elif bin_instruction == int('85', 16): # STA Zero Page
            memory_position = self.read_memo()
            return methods._sta(self, memory_position)
        elif bin_instruction == int('18', 16): # CLI
            return methods._clc(self, None)

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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._cmp(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('DD', 16): # CMP Absolute,X
            absolute_position_lo = self.read_memo() + self.X.value
            absolute_position_hi = self.read_memo()
            return methods._cmp(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('D9', 16): # CMP Absolute,Y
            absolute_position_lo = self.read_memo() + self.Y.value
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._cpx(self, absolute_position_hi * 256 + absolute_position_lo)
        
        elif bin_instruction == int('C0', 16): # CPY Immediate
            immediate = self.read_memo()
            return methods._cpy(self, immediate, is_immediate=True)

        elif bin_instruction == int('C4', 16): # CPY Zero Page
            zero_position = self.read_memo()
            return methods._cpy(self, zero_position)

        elif bin_instruction == int('CC', 16): # CPY Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._cpy(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('C6', 16): # DEC Zero Page
            zero_position = self.read_memo()
            return methods._dec(self, zero_position)

        elif bin_instruction == int('D6', 16): # DEC Zero Page,X
            zero_position = self.read_memo() + self.X.value
            return methods._dec(self, zero_position)

        elif bin_instruction == int('CE', 16): # DEC Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._dec(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('DE', 16): # DEC Absolute,X
            absolute_position_lo = self.read_memo() + self.X.value
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._eor(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('5D', 16): # EOR Absolute,X
            absolute_position_lo = self.read_memo() + self.X.value
            absolute_position_hi = self.read_memo()
            return methods._eor(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('59', 16): # EOR Absolute,Y
            absolute_position_lo = self.read_memo() + self.Y.value
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._inc(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('FE', 16): # INC Absolute,X
            absolute_position_lo = self.read_memo() + self.X.value
            absolute_position_hi = self.read_memo()
            return methods._inc(self, absolute_position_hi * 256 + absolute_position_lo)
        
        elif bin_instruction == int('E8', 16): # INX
            return methods._inx(self, None)
        
        elif bin_instruction == int('C8', 16): # INY
            return methods._iny(self, None)
        
        elif bin_instruction == int('4C', 16): # JMP Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            # absolute_position_lo = self.read_memo()
            return methods._jmp(self, absolute_position_hi * 256 + absolute_position_lo)
        
        elif bin_instruction == int('6C', 16): # JMP Indirect
            # indirect_position points to low indirect value, a subsequent
            # read in the memory for indirect_position + 1 is needed
            # for the memory high position
            indirect_position_lo = self.read_memo()
            indirect_position_hi = self.read_memo()
            
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
            return methods._jmp(self, memory_position_hi * 256 + memory_position_lo)

        elif bin_instruction == int('00', 16): # BRK
            # TODO: Set flagas and move PC
            return methods._brk(self, 0)

        elif bin_instruction == int('95', 16): # STA Zero Page, X
            memory_position = self.read_memo()
            return methods._sta(self, memory_position + self.X.value)

        elif bin_instruction == int('8D', 16): # STA Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._sta(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('9D', 16): # STA Absolute,X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._sta(self, absolute_position_hi * 256 + absolute_position_lo + self.X.value)

        elif bin_instruction == int('99', 16): # STA Absolute,Y
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._sta(self, absolute_position_hi * 256 + absolute_position_lo + self.Y.value)

        elif bin_instruction == int('81', 16): # STA Indirect,X
            indirect_memory = self.read_memo() + self.X.value
            memory_position = self.memory.read_memo(indirect_memory)
            actual_memory = self.memory.read_memo(memory_position)
            return methods._sta(self, actual_memory)

        elif bin_instruction == int('91', 16): # STA Indirect,Y
            indirect_memory = self.read_memo()
            memory_position = self.memory.read_memo(indirect_memory) + self.Y.value
            actual_memory = self.memory.read_memo(memory_position)
            return methods._sta(self, actual_memory)

        elif bin_instruction == int('86', 16): # STX Zero Page
            memory_position = self.read_memo()
            return methods._stx(self, memory_position)

        elif bin_instruction == int('96', 16): # STX Zero Page, Y
            memory_position = self.read_memo()
            return methods._stx(self, memory_position + self.Y.value)

        elif bin_instruction == int('8E', 16): # STX Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            return methods._stx(self, absolute_position_hi * 256 + absolute_position_lo)

        elif bin_instruction == int('84', 16): # STY Zero Page
            memory_position = self.read_memo()
            return methods._sty(self, memory_position)

        elif bin_instruction == int('94', 16): # STY Zero Page, X
            memory_position = self.read_memo()
            return methods._sty(self, memory_position + self.X.value)

        elif bin_instruction == int('8C', 16): # STY Absolute
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
# ********************** Third Line - Willian Hayashida ******************************************************    
        elif bin_instruction == int('20', 16): # JSR
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()

            address = absolute_position_hi * 256 + absolute_position_lo + self.X.value
            next_instruction =  self.PC.value - 1
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._lda(self, memory_position)

        elif bin_instruction == int('BD', 16): # LDA Absolute,X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position =  absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._lda(self, memory_position)

        elif bin_instruction == int('B9', 16): # LA Absolute, Y
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ldx(self, memory_position)

        elif bin_instruction == int('BE', 16): # LDX Absolute, Y
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ldy(self, memory_position)

        elif bin_instruction == int('BC', 16): # LDY Absolute, X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._lsr(self, memory_position)

        elif bin_instruction == int('5E', 16): # LSR Absolute, X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ora(self, memory_position)

        elif bin_instruction == int('1D', 16): # ORA Absolute,X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position =  absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._ora(self, memory_position)

        elif bin_instruction == int('19', 16): # LA Absolute, Y
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._rol(self, memory_position)

        elif bin_instruction == int('3E', 16): # ROL Absolute, X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
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
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo
            return methods._ror(self, memory_position)

        elif bin_instruction == int('7E', 16): # ROR Absolute, X
            absolute_position_lo = self.read_memo()
            absolute_position_hi = self.read_memo()
            memory_position = absolute_position_hi * 256 + absolute_position_lo + self.X.value
            return methods._ror(self, memory_position) 

        elif bin_instruction == int('40', 16): # ROR Absolute, X
            return methods._rti(self)

        else:
            # TODO: Add error to log
            return methods._brk(self, 1)

    def log(self, err):
        return ""

    def debug_print(self, args):
        if _DEBUG:
            print(args)
            
def debug_print(args):
    if _DEBUG:
        print(args)

def main():
    filename = sys.argv[1]
    processor = Processor(filename)
    processor.emula(0)

if __name__ == "__main__":
    main()
