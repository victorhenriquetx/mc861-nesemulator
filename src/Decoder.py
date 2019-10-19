
class Decoder():
    def __init__(self, processor):
        self.processor = processor


    def brk(self): # bin_instruction == int('00', 16): # BRK
        methods._brk(self.processor, 0)
    #---------------------- ADC Instruction----------------------------------
    def adc_immediate(self): # bin_instruction == int('69', 16): # ADC Immediate
        value = self.processor.read_immediate()
        methods._adc(self.processor, value)

    def adc_zero_page(self): # bin_instruction == int('65', 16): # ADC Zero Page
        zero_position = self.processor.read_zero_page()
        value = self.processor.memory.read_memo(zero_position)
        methods._adc(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def adc_zero_page_x(self): # bin_instruction == int('75', 16): # ADC Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        value = self.processor.memory.read_memo(zero_position)
        methods._adc(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def adc_absolute(self): # bin_instruction == int('6D', 16): # ADC Absolute
        absolute_position = self.processor.read_absolute()
        value = self.processor.memory.read_memo(absolute_position)
        methods._adc(self.processor,value)
        self.processor.mem_print(absolute_position, value)

    def adc_absolute_x(self): # bin_instruction == int('7D', 16): # ADC Absolute,X
        absolute_position = self.processor.read_absolute_x()
        value = self.processor.memory.read_memo(absolute_position)
        methods._adc(self.processor, value)
        self.processor.mem_print(absolute_position, value)

    def adc_absolute_y(self): # bin_instruction == int('79', 16): # ADC Absolute,Y
        absolute_position = self.processor.read_absolute_y()
        value = self.processor.memory.read_memo(absolute_position)
        methods._adc(self.processor, value)
        self.processor.mem_print(absolute_position, value)   

    def adc_indirect_x(self): # bin_instruction == int('61', 16): # ADC Indirect,X
        final_memory, indirect_position = self.processor.read_indirect_x()
        methods._adc(self.processor, final_memory)
        self.processor.mem_print(indirect_position, final_memory)   

    def adc_indirect_y(self): # bin_instruction == int('71', 16): # ADC Indirect,Y
        final_memory, indirect_position = self.processor.read_indirect_y()
        methods._adc(self.processor, final_memory)
        self.processor.mem_print(indirect_position, final_memory)   

    #---------------------- AND Instruction----------------------------------
    def (self): # bin_instruction == int('29', 16): # AND Immediate
        value = self.processor.read_immediate() #immediate
        methods._and(self.processor, value)

    def (self): # bin_instruction == int('25', 16): # AND Zero Page
        zero_position = self.processor.read_zero_page()
        value = self.processor.memory.read_memo(zero_position)
        methods._and(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def (self): # bin_instruction == int('35', 16): # AND Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        value = self.processor.memory.read_memo(zero_position)
        methods._and(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def (self): # bin_instruction == int('2D', 16): # AND Absolute
        absolute_position = self.processor.read_absolute()
        value = self.processor.memory.read_memo(absolute_position)
        methods._and(self.processor,value)
        self.processor.mem_print(absolute_position, value)

    def (self): # bin_instruction == int('3D', 16): # AND Absolute,X
        absolute_position = self.processor.read_absolute_x()
        value = self.processor.memory.read_memo(absolute_position)
        methods._and(self.processor, value)
        self.processor.mem_print(absolute_position, value)

    def (self): # bin_instruction == int('39', 16): # AND Absolute,Y
        absolute_position = self.processor.read_absolute_y()
        value = self.processor.memory.read_memo(absolute_position)
        methods._and(self.processor, value)
        self.processor.mem_print(absolute_position, value)   

    def (self): # bin_instruction == int('21', 16): # AND Indirect,X
        final_memory, indirect_position = self.processor.read_indirect_x()
        methods._and(self.processor, final_memory)
        self.processor.mem_print(indirect_position, final_memory)   

    def (self): # bin_instruction == int('31', 16): # AND Indirect,Y
        final_memory, indirect_position = self.processor.read_indirect_y()
        methods._and(self.processor, final_memory)
        self.processor.mem_print(indirect_position, final_memory)   

    #---------------------- AND Instruction----------------------------------
    def (self): # bin_instruction == int('0A', 16): # ASL Accumulator
        methods._asl(self.processor, self.processor.A)

    def (self): # bin_instruction == int('06', 16): # ASL Zero Page
        zero_position = self.processor.read_zero_page()
        value = self.processor.memory.read_memo(zero_position)
        methods._asl(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def (self): # bin_instruction == int('16', 16): # ASL Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        value = self.processor.memory.read_memo(zero_position)
        methods._asl(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def (self): # bin_instruction == int('0E', 16): # ASL Absolute
        absolute_position = self.processor.read_absolute()
        value = self.processor.memory.read_memo(absolute_position)
        methods._asl(self.processor,value)
        self.processor.mem_print(absolute_position, value)

    def (self): # bin_instruction == int('1E', 16): # ASL Absolute,X
        absolute_position = self.processor.read_absolute_x()
        value = self.processor.memory.read_memo(absolute_position)
        methods._asl(self.processor, value)
        self.processor.mem_print(absolute_position, value)

    #---------------------- BIT Instruction-------------------------------------
    def (self): # bin_instruction == int('24', 16): # BIT Zero Page
        zero_position = self.processor.read_zero_page()
        value = self.processor.memory.read_memo(zero_position)
        methods._bit(self.processor, value)
        self.processor.mem_print(zero_position, value)
    def (self): # bin_instruction == int('2C', 16): # BIT Absolute
        absolute_position = self.processor.read_absolute()
        value = self.processor.memory.read_memo(absolute_position)
        methods._bit(self.processor,value)
        self.processor.mem_print(absolute_position, value)   

    #---------------------- Branch Instruction---------------------------------- 
    def (self): # bin_instruction == int('10', 16):
        branch_increment = self.processor.read_relative()
        
        methods._bpl(self.processor, branch_increment)
    def (self): # bin_instruction == int('30', 16):
        branch_increment = self.processor.read_relative()
        
        methods._bmi(self.processor, branch_increment)
    def (self): # bin_instruction == int('50', 16):
        branch_increment = self.processor.read_relative()
        
        methods._bvc(self.processor, branch_increment)
    def (self): # bin_instruction == int('70', 16):
        branch_increment = self.processor.read_relative()
        
        methods._bvs(self.processor, branch_increment)
    def (self): # bin_instruction == int('90', 16):
        branch_increment = self.processor.read_relative()
        
        methods._bcc(self.processor, branch_increment)
    def (self): # bin_instruction == int('B0', 16):
        branch_increment = self.processor.read_relative()
        
        methods._bcs(self.processor, branch_increment)
    def (self): # bin_instruction == int('D0', 16):
        branch_increment = self.processor.read_relative()
        
        methods._bne(self.processor, branch_increment)
    def (self): # bin_instruction == int('F0', 16):
        branch_increment = self.processor.read_relative()
        
        methods._beq(self.processor, branch_increment)

    def (self): # bin_instruction == int('60', 16): # RTS
        absolute_position_lo = self.processor.memory.pop_stack(self.processor.STACK)
        absolute_position_hi = self.processor.memory.pop_stack(self.processor.STACK)
        methods._rts(self.processor, absolute_position_hi * 256 + absolute_position_lo)

    def (self): # bin_instruction == int('E9', 16): # SBC Immediate
        value = self.processor.read_immediate()
        methods._sbc(self.processor, value)

    def (self): # bin_instruction == int('E5', 16): # SBC Zero Page
        zero_position = self.processor.read_zero_page()
        value = self.processor.memory.read_memo(zero_position)
        methods._sbc(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def (self): # bin_instruction == int('F5', 16): # SBC Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        value = self.processor.memory.read_memo(zero_position)
        methods._sbc(self.processor, value)
        self.processor.mem_print(zero_position, value)

    def (self): # bin_instruction == int('ED', 16): # SBC Absolute
        absolute_position = self.processor.read_absolute()
        value = self.processor.memory.read_memo(absolute_position)
        methods._sbc(self.processor,value)
        self.processor.mem_print(absolute_position, value)

    def (self): # bin_instruction == int('FD', 16): # SBC Absolute,X
        absolute_position = self.processor.read_absolute_x()
        value = self.processor.memory.read_memo(absolute_position)
        methods._sbc(self.processor, value)
        self.processor.mem_print(absolute_position, value)

    def (self): # bin_instruction == int('F9', 16): # SBC Absolute,Y
        absolute_position = self.processor.read_absolute_y()
        value = self.processor.memory.read_memo(absolute_position_hi * 256 + absolute_position_lo)
        methods._sbc(self.processor, value)
        self.processor.mem_print(absolute_position, value) 

    def (self): # bin_instruction == int('E1', 16): # SBC Indirect,X
        value, memory_position = self.processor.read_indirect_x()
        methods._sbc(self.processor, value)
        self.processor.mem_print(memory_position, value)

    def (self): # bin_instruction == int('F1', 16): # SBC Indirect,Y
        value, memory_position = self.processor.read_indirect_y()
        methods._sbc(self.processor, value)
        self.processor.mem_print(memory_position, value)

    def (self): # bin_instruction == int('38', 16): # SEC
        methods._sec(self.processor)

    def (self): # bin_instruction == int('F8', 16): # SED
        methods._sed(self.processor)

    def (self): # bin_instruction == int('78', 16): # SEI
        methods._sei(self.processor)

    def (self): # bin_instruction == int('85', 16): # STA Zero Page
        memory_position = self.processor.read_zero_page()
        methods._sta(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)
        
    def (self): # bin_instruction == int('18', 16): # CLC
        methods._clc(self.processor, None)

    def (self): # bin_instruction == int('58', 16): # CLI
        methods._cli(self.processor, None)

    def (self): # bin_instruction == int('D8', 16): # CLD
        methods._cld(self.processor, None)

    def (self): # bin_instruction == int('B8', 16): # CLV
        methods._clv(self.processor, None)

    def (self): # bin_instruction == int('C9', 16): # CMP Immediate
        immediate = self.processor.read_immediate()
        methods._cmp(self.processor, immediate, is_immediate=True)

    def (self): # bin_instruction == int('C5', 16): # CMP Zero Page
        zero_position = self.processor.read_zero_page()
        methods._cmp(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('D5', 16): # CMP Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        methods._cmp(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('CD', 16): # CMP Absolute
        absolute_position = self.processor.read_absolute()
        methods._cmp(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('DD', 16): # CMP Absolute,X
        absolute_position = self.processor.read_absolute_x()
        methods._cmp(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('D9', 16): # CMP Absolute,Y
        absolute_position = self.processor.read_absolute_y()
        methods._cmp(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('C1', 16): # CMP (Indirect,X)
        absolute_position, memory_position = self.processor.read_indirect_x()
        methods._cmp(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('D1', 16): # CMP (Indirect),Y
        absolute_position, memory_position = self.processor.read_indirect_y()
        methods._cmp(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('E0', 16): # CPX Immediate
        immediate = self.processor.read_immediate()
        methods._cpx(self.processor, immediate, is_immediate=True)

    def (self): # bin_instruction == int('E4', 16): # CPX Zero Page
        zero_position = self.processor.read_zero_page()
        methods._cpx(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('EC', 16): # CPX Absolute
        absolute_position = self.processor.read_absolute()
        methods._cpx(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('C0', 16): # CPY Immediate
        immediate = self.processor.read_immediate()
        methods._cpy(self.processor, immediate, is_immediate=True)

    def (self): # bin_instruction == int('C4', 16): # CPY Zero Page
        zero_position = self.processor.read_zero_page()
        methods._cpy(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('CC', 16): # CPY Absolute
        absolute_position = self.processor.read_absolute()
        methods._cpy(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('C6', 16): # DEC Zero Page
        zero_position = self.processor.read_zero_page()
        methods._dec(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('D6', 16): # DEC Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        methods._dec(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('CE', 16): # DEC Absolute
        absolute_position = self.processor.read_absolute()
        methods._dec(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('DE', 16): # DEC Absolute,X
        absolute_position = self.processor.read_absolute_x()
        methods._dec(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('CA', 16): # DEX
        methods._dex(self.processor, None)

    def (self): # bin_instruction == int('88', 16): # DEY
        methods._dey(self.processor, None)

    def (self): # bin_instruction == int('49', 16): # EOR Immediate
        immediate = self.processor.read_immediate()
        methods._eor(self.processor, immediate, is_immediate=True)

    def (self): # bin_instruction == int('45', 16): # EOR Zero Page
        zero_position = self.processor.read_zero_page()
        methods._eor(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('55', 16): # EOR Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        methods._eor(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('4D', 16): # EOR Absolute
        absolute_position = self.processor.read_absolute()
        methods._eor(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('5D', 16): # EOR Absolute,X
        absolute_position = self.processor.read_absolute_x()
        methods._eor(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('59', 16): # EOR Absolute,Y
        absolute_position = self.processor.read_absolute_y()
        methods._eor(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('41', 16): # EOR (Indirect,X)
        absolute_position, memory_position = self.processor.read_indirect_x()
        methods._eor(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('51', 16): # EOR (Indirect),Y
        absolute_position, memory_position = self.processor.read_indirect_y()
        methods._eor(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('E6', 16): # INC Zero Page
        zero_position = self.processor.read_zero_page()
        methods._inc(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('F6', 16): # INC Zero Page,X
        zero_position = self.processor.read_zero_page_x()
        methods._inc(self.processor, zero_position)
        self.processor.mem_print(zero_position, self.processor.memory.read_memo(zero_position))

    def (self): # bin_instruction == int('EE', 16): # INC Absolute
        absolute_position = self.processor.read_absolute()
        methods._inc(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('FE', 16): # INC Absolute,X
        absolute_position = self.processor.read_absolute_x()
        methods._inc(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('E8', 16): # INX
        methods._inx(self.processor, None)

    def (self): # bin_instruction == int('C8', 16): # INY
        methods._iny(self.processor, None)

    def (self): # bin_instruction == int('4C', 16): # JMP Absolute
        absolute_position = self.processor.read_absolute()
        methods._jmp(self.processor, absolute_position)

    def (self): # bin_instruction == int('6C', 16): # JMP Indirect
        # indirect_position points to low indirect value, a subsequent
        # read in the memory for indirect_position + 1 is needed
        # for the memory high position
        indirect_position_lo = self.processor.read_memo_pc()
        indirect_position_hi = self.processor.read_memo_pc()
        
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

        memory_position_lo = self.processor.memory.read_memo(indirect_position_hi * 256 + indirect_position_lo)
        memory_position_hi = self.processor.memory.read_memo(indirect_position_hi * 256 + indirect_position_lo_plus_one)
        memory_position = memory_position_hi * 256 + memory_position_lo
        methods._jmp(self.processor, memory_position)

    def (self): # bin_instruction == int('95', 16): # STA Zero Page, X
        memory_position = self.processor.read_zero_page_x()
        methods._sta(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position)) 

    def (self): # bin_instruction == int('8D', 16): # STA Absolute
        absolute_position = self.processor.read_absolute()
        methods._sta(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('9D', 16): # STA Absolute,X
        absolute_position = self.processor.read_absolute_x()
        methods._sta(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('99', 16): # STA Absolute,Y
        absolute_position = self.processor.read_absolute_y()
        methods._sta(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('81', 16): # STA Indirect,X
        actual_memory, memory_position = self.processor.read_indirect_x()
        methods._sta(self.processor, actual_memory)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(actual_memory))

    def (self): # bin_instruction == int('91', 16): # STA Indirect,Y
        actual_memory, memory_position = self.processor.read_indirect_y()
        methods._sta(self.processor, actual_memory)
        self.processor.mem_print(actual_memory, self.processor.memory.read_memo(actual_memory))

    def (self): # bin_instruction == int('86', 16): # STX Zero Page
        memory_position = self.processor.read_zero_page()
        methods._stx(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('96', 16): # STX Zero Page, Y
        memory_position = self.processor.read_zero_page_y()
        methods._stx(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('8E', 16): # STX Absolute
        absolute_position = self.processor.read_absolute()
        methods._stx(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('84', 16): # STY Zero Page
        memory_position = self.processor.read_zero_page()
        methods._sty(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('94', 16): # STY Zero Page, X
        memory_position = self.processor.read_zero_page_x()
        methods._sty(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('8C', 16): # STY Absolute
        absolute_position = self.processor.read_absolute()
        methods._sty(self.processor, absolute_position)
        self.processor.mem_print(absolute_position, self.processor.memory.read_memo(absolute_position))

    def (self): # bin_instruction == int('AA', 16): # TAX
        methods._tax(self.processor)

    def (self): # bin_instruction == int('A8', 16): # TAY
        methods._tay(self.processor)

    def (self): # bin_instruction == int('BA', 16): # TSX
        methods._tsx(self.processor)

    def (self): # bin_instruction == int('9A', 16): # TXS
        methods._txs(self.processor)

    def (self): # bin_instruction == int('8A', 16): # TXA
        methods._txa(self.processor)

    def (self): # bin_instruction == int('98', 16): # TYA
        methods._tya(self.processor)

    # ********* Third Line - Willian Hayashida ********************************    
    def (self): # bin_instruction == int('20', 16): # JSR
        address = self.processor.read_absolute()
        next_instruction =  self.processor.PC.value
        methods._jsr(self.processor, address, next_instruction)

    def (self): # bin_instruction == int('A9', 16): # LDA Immediate
        value = self.processor.read_immediate()
        methods._lda(self.processor, value, immediate=True)

    def (self): # bin_instruction == int('A5', 16): # LDA zero page
        absolute_position_lo = self.processor.read_zero_page()
        methods._lda(self.processor, absolute_position_lo)
        self.processor.mem_print(absolute_position_lo, self.processor.A.value)

    def (self): # bin_instruction == int('B5', 16): # LDA zero page, X
        memory_position = self.processor.read_zero_page_x()
        methods._lda(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)

    def (self): # bin_instruction == int('AD', 16): # LDA Absolute
        memory_position = self.processor.read_absolute()
        methods._lda(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)
        

    def (self): # bin_instruction == int('BD', 16): # LDA Absolute,X
        memory_position = self.processor.read_absolute_x()
        methods._lda(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)

    def (self): # bin_instruction == int('B9', 16): # LDA Absolute, Y
        memory_position = self.processor.read_absolute_y()
        methods._lda(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)

    def (self): # bin_instruction == int('A1', 16): # LDA Indirect, X
        memory_position, _ = self.processor.read_indirect_x()

        methods._lda(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)

    def (self): # bin_instruction == int('B1', 16): # LDA Indirect, Y
        memory_position, _ = self.processor.read_indirect_y()

        methods._lda(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)

    # LDX A2, A6, B6, AE, BE
    def (self): # bin_instruction == int('A2', 16): # LDX Immediate
        value = self.processor.read_immediate()
        methods._ldx(self.processor, value, immediate=True)

    def (self): # bin_instruction == int('A6', 16): # LDX Zero Page
        absolute_position_lo = self.processor.read_zero_page()
        methods._ldx(self.processor, absolute_position_lo)
        self.processor.mem_print(absolute_position_lo, self.processor.X.value)

    def (self): # bin_instruction == int('B6', 16): # LDX Zero Page, Y
        absolute_position_lo = self.processor.read_zero_page_y()
        memory_position = absolute_position_lo + self.processor.Y.value
        methods._ldx(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.X.value)

    def (self): # bin_instruction == int('AE', 16): # LDX Absolute
        memory_position = self.processor.read_absolute()
        methods._ldx(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.X.value)

    def (self): # bin_instruction == int('BE', 16): # LDX Absolute, Y
        memory_position = self.processor.read_absolute_y()
        methods._ldx(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.X.value)
        
    # Immediate     LDY #$44      $A0  2   2
    # Zero Page     LDY $44       $A4  2   3
    # Zero Page,X   LDY $44,X     $B4  2   4
    # Absolute      LDY $4400     $AC  3   4
    # Absolute,X    LDY $4400,X   $BC  3   4+
    # LDX A2, A6, B6, AE, BE

    def (self): # bin_instruction == int('A0', 16): # LDY Immediate
        value = self.processor.read_immediate()
        methods._ldy(self.processor, value, immediate=True)

    def (self): # bin_instruction == int('A4', 16): # LDY Zero Page
        absolute_position_lo = self.processor.read_zero_page()
        methods._ldy(self.processor, absolute_position_lo)
        self.processor.mem_print(absolute_position_lo, self.processor.Y.value)

    def (self): # bin_instruction == int('B4', 16): # LDY Zero Page, X
        absolute_position_lo = self.processor.read_zero_page_x()
        memory_position = absolute_position_lo + self.processor.Y.value
        methods._ldy(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.Y.value)

    def (self): # bin_instruction == int('AC', 16): # LDY Absolute
        memory_position = self.processor.read_absolute()
        methods._ldy(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.Y.value)

    def (self): # bin_instruction == int('BC', 16): # LDY Absolute, X
        memory_position = self.processor.read_absolute_x()
        methods._ldy(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.Y.value)

    # Accumulator   LSR A         $4A  1   2
    # Zero Page     LSR $44       $46  2   5
    # Zero Page,X   LSR $44,X     $56  2   6
    # Absolute      LSR $4400     $4E  3   6
    # Absolute,X    LSR $4400,X   $5E  3   7
    def (self): # bin_instruction == int('4A', 16): # LSR A
        methods._lsr(self.processor, 'A')
    def (self): # bin_instruction == int('46', 16): # LSR Zero Page
        absolute_position_lo = self.processor.read_zero_page()
        methods._lsr(self.processor, absolute_position_lo)
        self.processor.mem_print(absolute_position_lo, self.processor.memory.read_memo(absolute_position_lo))

    def (self): # bin_instruction == int('56', 16): # LSR Zero Page, X
        absolute_position_lo = self.processor.read_zero_page_x()
        memory_position = absolute_position_lo + self.processor.Y.value
        methods._lsr(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('4E', 16): # LSR Absolute
        memory_position = self.processor.read_absolute()
        methods._lsr(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('5E', 16): # LSR Absolute, X
        memory_position = self.processor.read_absolute_x()
        methods._lsr(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    # NOP
    def (self): # bin_instruction == int('EA', 16): # NOP
        methods._nop()

    # Immediate     ORA #$44      $09  2   2
    # Zero Page     ORA $44       $05  2   3
    # Zero Page,X   ORA $44,X     $15  2   4
    # Absolute      ORA $4400     $0D  3   4
    # Absolute,X    ORA $4400,X   $1D  3   4+
    # Absolute,Y    ORA $4400,Y   $19  3   4+
    # Indirect,X    ORA ($44,X)   $01  2   6
    # Indirect,Y    ORA ($44),Y   $11  2   5+
    def (self): # bin_instruction == int('09', 16): # ORA Immediate
        value = self.processor.read_immediate()
        methods._ora(self.processor, value, immediate=True)

    def (self): # bin_instruction == int('05', 16): # ORA zero page
        absolute_position_lo = self.processor.read_zero_page()
        methods._ora(self.processor, absolute_position_lo)
        self.processor.mem_print(absolute_position_lo, self.processor.memory.read_memo(absolute_position_lo))

    def (self): # bin_instruction == int('15', 16): # ORA zero page, X
        absolute_position_lo = self.processor.read_zero_page_x()
        memory_position = absolute_position_lo + self.processor.X.value
        methods._ora(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('0D', 16): # ORA Absolute
        # TODO: Check if the HI/LOW order is right
        memory_position = self.processor.read_absolute()
        methods._ora(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('1D', 16): # ORA Absolute,X
        memory_position =  self.processor.read_absolute_x()
        methods._ora(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('19', 16): # ORA Absolute, Y
        memory_position = self.processor.read_absolute_y()
        methods._ora(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('01', 16): # ORA Indirect, X
        memory_position, _ = self.processor.read_indirect_x()

        methods._ora(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)
        

    def (self): # bin_instruction == int('11', 16): # ORA Indirect, Y
        memory_position, _ = self.processor.read_indirect_y()

        methods._ora(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.A.value)

    # PHA (Push Acc)
    def (self): # bin_instruction == int('48', 16): # Push Accumulator
        methods._pha(self.processor)
    # PLA (Pop Acc)
    def (self): # bin_instruction == int('68', 16): # Pop Accumulator
        methods._pla(self.processor)
    # PHP (Push Processor) 
    def (self): # bin_instruction == int('08', 16): # Push Flags
        methods._php(self.processor)
    # PLP (Pop Processor)
    def (self): # bin_instruction == int('28', 16): # Pop Flags
        methods._plp(self.processor)
    # Accumulator   ROL A         $2A  1   2
    # Zero Page     ROL $44       $26  2   5
    # Zero Page,X   ROL $44,X     $36  2   6
    # Absolute      ROL $4400     $2E  3   6
    # Absolute,X    ROL $4400,X   $3E  3   7
    # ROL
    def (self): # bin_instruction == int('2A', 16): # ROL A
        methods._rol(self.processor, 'A')

    def (self): # bin_instruction == int('26', 16): # ROL Zero Page
        absolute_position_lo = self.processor.read_zero_page()
        methods._rol(self.processor, absolute_position_lo)
        self.processor.mem_print(absolute_position_lo, self.processor.memory.read_memo(absolute_position_lo))

    def (self): # bin_instruction == int('36', 16): # ROL Zero Page, X
        absolute_position_lo = self.processor.read_zero_page_x()
        memory_position = absolute_position_lo + self.processor.Y.value
        methods._rol(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('2E', 16): # ROL Absolute
        memory_position = self.processor.read_absolute()
        methods._rol(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('3E', 16): # ROL Absolute, X
        memory_position = self.processor.read_absolute_x()
        methods._rol(self.processor, memory_position)   
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    # Accumulator   ROR A         $6A  1   2
    # Zero Page     ROR $44       $66  2   5
    # Zero Page,X   ROR $44,X     $76  2   6
    # Absolute      ROR $4400     $6E  3   6
    # Absolute,X    ROR $4400,X   $7E  3   7
    # ROR
    def (self): # bin_instruction == int('6A', 16): # ROR A
        methods._ror(self.processor, 'A')

    def (self): # bin_instruction == int('66', 16): # ROR Zero Page
        absolute_position_lo = self.processor.read_zero_page()
        methods._ror(self.processor, absolute_position_lo)
        self.processor.mem_print(absolute_position_lo, self.processor.memory.read_memo(absolute_position_lo))

    def (self): # bin_instruction == int('76', 16): # ROR Zero Page, X
        absolute_position_lo = self.processor.read_zero_page_x()
        memory_position = absolute_position_lo + self.processor.Y.value
        methods._ror(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('6E', 16): # ROR Absolute
        memory_position = self.processor.read_absolute()
        methods._ror(self.processor, memory_position)
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('7E', 16): # ROR Absolute, X
        memory_position = self.processor.read_absolute_x()
        methods._ror(self.processor, memory_position) 
        self.processor.mem_print(memory_position, self.processor.memory.read_memo(memory_position))

    def (self): # bin_instruction == int('40', 16): # RTI
        methods._rti(self.processor)

    else:
        methods._brk(self.processor, 1)