import sys

def _adc(processor, value):
    processor.A.value += value + processor.FLAGS.is_C()

    if processor.A.check_overflow():
        processor.A.value -= 255
        processor.FLAGS.set_C()
        processor.FLAGS.set_V()
    if processor.A.is_negative():
        processor.FLAGS.set_N()
    if processor.A.value == 0:
        processor.FLAGS.set_Z()

def _and(processor, value):
    processor.A.value = processor.A.value & value
    if processor.A.is_negative():
        processor.FLAGS.set_N()
    if processor.A.value == 0:
        processor.FLAGS.set_Z()

def _asl(processor, value):
    processor.A.value = value << 1
    if processor.A.check_overflow():
        processor.A.value -= 255
        processor.FLAGS.set_C()
    if processor.A.is_negative():
        processor.FLAGS.set_N()
    if processor.A.value == 0:
        processor.FLAGS.set_Z()

def _bit(processor, value):
    testValue = processor.A.value & value
    processor.FLAGS.set_N() if value & (1 << 7) else processor.FLAGS.clear_N()
    processor.FLAGS.set_V() if value & (1 << 6) else processor.FLAGS.clear_V()
    if testValue == 0:
        processor.FLAGS.set_Z()

def _bcc(processor, memory_position):
    if(processor.FLAGS.is_C() == 0):
        processor.PC = memory_position
def _bcs(processor, memory_position):
    if(processor.FLAGS.is_C()):
        processor.PC = memory_position
def _beq(processor, memory_position):
    if(processor.FLAGS.is_Z()):
        processor.PC = memory_position
def _bmi(processor, memory_position):
    if(processor.FLAGS.is_N()):
        processor.PC = memory_position
def _bne(processor, memory_position):
    if(processor.FLAGS.is_Z() == 0):
        processor.PC = memory_position
def _bpl(processor, memory_position):
    if(processor.FLAGS.is_N() == 0):
        processor.PC = memory_position
def _bvc(processor, memory_position):
    if(processor.FLAGS.is_V() == 0):
        processor.PC = memory_position
def _bvs(processor, memory_position):
    if(processor.FLAGS.is_V()):
        processor.PC = memory_position

def _lda(processor, value, immediate=False):
    if not immediate:
        processor.A.value = processor.memory.read_memo(value)
    else:
        processor.A.value = value

def _ldx(processor, value, immediate=False):
    if not immediate:
        processor.X.value = processor.memory.read_memo(value)
    else:
        processor.X.value = value

def _ldy(processor, value, immediate=False):
    if not immediate:
        processor.Y.value = processor.memory.read_memo(value)
    else:
        processor.Y.value = value

def _lsr(processor, memory_position):
    if isinstance(memory_position, str) and memory_position == 'A':
        c = processor.A.value & 1 # get carry
        processor.A.value = processor.A.value >> 1 # shift and store to Acc
    else:
        v = processor.memory.read_memo(memory_position)
        c = v & 1 # get carry
        v = v >> 1 # shift right
        processor.memory.write_memo(memory_position, v) # store to memo

    # store bit 7 to carry
    if c == 0:
        processor.FLAGS.clear_C()
    else:
        processor.FLAGS.set_C()

def _nop():
    pass

def _ora(processor, value, immediate=False):
    if not immediate:
        v = processor.memory.read_memo(value)
        processor.A.value = processor.A.value | v
    else:
        processor.A.value = processor.A.value | value

def _cli(processor, instruction_param):
    processor.FLAGS.clear_I()

def _cld(processor, instruction_param):
    processor.FLAGS.clear_D()

def _clv(processor, instruction_param):
    processor.FLAGS.clear_V()

def _cmp(processor, instruction_param, is_immediate=False):
    # Load value to be compared from memory if not using an immediate
    if not is_immediate:
        value = processor.memory.read_memo(instruction_param)
    else:
        value = instruction_param

    result = processor.A.value - value
    # Set comparissons flag
    if processor.A.value >= value:
        processor.FLAGS.set_C()
    if processor.A.value == value:
        processor.FLAGS.set_Z()
    if result >= int('80', 16):
        processor.FLAGS.set_N()

def _cpx(processor, instruction_param, is_immediate=False):
    # Load value to be compared from memory if not using an immediate
    if not is_immediate:
        value = processor.memory.read_memo(instruction_param)
    else:
        value = instruction_param

    result = processor.X.value - value
    # Set comparissons flag
    if processor.X.value >= value:
        processor.FLAGS.set_C()
    if processor.X.value == value:
        processor.FLAGS.set_Z()
    if result >= int('80', 16):
        processor.FLAGS.set_N()

def _cpy(processor, instruction_param, is_immediate=False):
    # Load value to be compared from memory if not using an immediate
    if not is_immediate:
        value = processor.memory.read_memo(instruction_param)
    else:
        value = instruction_param

    result = processor.Y.value - value
    # Set comparissons flag
    if processor.Y.value >= value:
        processor.FLAGS.set_C()
    if processor.Y.value == value:
        processor.FLAGS.set_Z()
    if result >= int('80', 16):
        processor.FLAGS.set_N()

def _dec(processor, instruction_param):
    value = processor.memory.read_memo(instruction_param)
    value -= 1

    if value <= -1:
        value += 256

    processor.memory.write_memo(instruction_param, value)

    # Set flags
    if value == 0:
        processor.FLAGS.set_Z()
    if value >= int('80', 16):
        processor.FLAGS.set_N()

def _dex(processor, instruction_param):
    processor.X.value -= 1
    
    if processor.X.value <= -1:
        processor.X.value += 256
    
    # Set flags
    if processor.X.value == 0:
        processor.FLAGS.set_Z()
    if processor.X.value >= int('80', 16):
        processor.FLAGS.set_N()

def _dey(processor, instruction_param):
    processor.Y.value -= 1
    
    if processor.Y.value <= -1:
        processor.Y.value += 256
    
    # Set flags
    if processor.Y.value == 0:
        processor.FLAGS.set_Z()
    if processor.Y.value >= int('80', 16):
        processor.FLAGS.set_N()

def _eor(processor, instruction_param, is_immediate=False):
    # Load value to be XORed from memory if not using an immediate
    if not is_immediate:
        value = processor.memory.read_memo(instruction_param)
    else:
        value = instruction_param

    processor.A.value = processor.A.value ^ value
    # Set flags
    if processor.A.value == value:
        processor.FLAGS.set_Z()
    if processor.A.value >= int('80', 16):
        processor.FLAGS.set_N()

def _inc(processor, instruction_param):
    value = processor.memory.read_memo(instruction_param)
    value += 1

    if value > 255:
        value -= 256

    processor.memory.write_memo(instruction_param, value)

    # Set flags
    if value == 0:
        processor.FLAGS.set_Z()
    if value >= int('80', 16):
        processor.FLAGS.set_N()

def _inx(processor, instruction_param):
    processor.X.value += 1
    
    if processor.X.value > 255:
        processor.X.value -= 256
    
    # Set flags
    if processor.X.value == 0:
        processor.FLAGS.set_Z()
    if processor.X.value >= int('80', 16):
        processor.FLAGS.set_N()

def _iny(processor, instruction_param):
    processor.Y.value += 1
    
    if processor.Y.value > 255:
        processor.Y.value -= 256
    
    # Set flags
    if processor.Y.value == 0:
        processor.FLAGS.set_Z()
    if processor.Y.value >= int('80', 16):
        processor.FLAGS.set_N()

def _jmp(processor, value):
    processor.PC.value = value

def _jsr(processor, address, next_instruction):
    processor.memory.push_stack(processor.STACK, next_instruction)
    processor.PC.value = address

def _brk(processor, exit_status):
    sys.exit(exit_status)

def _pha(processor):
    processor.memory.push_stack(processor.STACK, processor.A.value)

def _pla(processor):
    processor.memory.pop_stack(processor.STACK, processor.A.value)

def _php(processor):
    processor.memory.push_stack(processor.STACK, processor.FLAGS.value)

def _plp(processor):
    processor.memory.pop_stack(processor.STACK, processor.FLAGS.value)

def _rol(processor, memory_position):
    if isinstance(memory_position, str) and memory_position == 'A':
        c = processor.A.value & 128 # get bit 7
        processor.A.value = processor.A.value << 1 # shift left and store
        processor.A.value = processor.A.value | processor.FLAGS.is_C() # store carry to bit 0
    else:
        v = processor.memory.read_memo(memory_position)
        c = v & 128 # get bit 7
        v = v << 1 # shift left
        v = v | processor.FLAGS.is_C() # store carry to bit 0
        processor.memory.write_memo(memory_position, v) # store to memo
    
    # store bit 7 to carry
    if c == 0:
        processor.FLAGS.clear_C()
    else:
        processor.FLAGS.set_C()
        

def _ror(processor, memory_position):
    if isinstance(memory_position, str) and memory_position == 'A':
        c = processor.A.value & 1 # get bit 0
        processor.A.value = processor.A.value >> 1 # shift right and store
        processor.A.value = processor.A.value | (processor.FLAGS.is_C()*128) # store carry to bit 7
    else:
        v = processor.memory.read_memo(memory_position)
        c = v & 1 # get bit 0
        v = v >> 1 # shift right
        v = v | (processor.FLAGS.is_C()*128) # store carry to bit 7
        processor.memory.write_memo(memory_position, v) # store to memo
    
    # store bit 7 to carry
    if c == 0:
        processor.FLAGS.clear_C()
    else:
        processor.FLAGS.set_C()
    

def _rti(processor):
    processor.FLAGS.value = processor.memory.pop_stack(processor.STACK)
    processor.PC.value = processor.memory.pop_stack(processor.STACK)
def _rts(processor, memory_position):
    processor.PC.value = memory_position

def _sbc(processor, value):
    processor.A.value -= value - processor.FLAGS.is_C()

    if processor.A.value < -128:
        processor.A.value += 255
        processor.FLAGS.set_C()
        processor.FLAGS.set_V()
    if processor.A.is_negative():
        processor.FLAGS.set_N()
    if processor.A.value == 0:
        processor.FLAGS.set_Z()

def _sec(processor):
    processor.FLAGS.set_C()

def _sed(processor):
    processor.FLAGS.set_D()

def _sei(processor):
    processor.FLAGS.set_I()

def _sta(processor, memory_position):
    processor.memory.write_memo(memory_position, processor.A.value)

def _stx(processor, memory_position):
    processor.memory.write_memo(memory_position, processor.X.value)

def _sty(processor, memory_position):
    processor.memory.write_memo(memory_position, processor.Y.value)

def _tax(processor):
    processor.X.value = processor.A.value
    if processor.X.value == 0:
        processor.FLAGS.set_Z()
    if processor.X.value & 128 == 0:
        processor.FLAGS.set_N()

def _tay(processor):
    processor.Y.value = processor.A.value
    if processor.Y.value == 0:
        processor.FLAGS.set_Z()
    if processor.Y.value & 128 == 0:
        processor.FLAGS.set_N()

def _tsx(processor):
    processor.X.value = processor.memory[processor.memory.stack_offset + processor.STACK.value]

def _txs(processor):
    processor.memory[processor.memory.stack_offset + processor.STACK.value] = processor.X.value

def _txa(processor):
    processor.A.value = processor.X.value
    if processor.A.value == 0:
        processor.FLAGS.set_Z()
    if processor.A.value & 128 == 0:
        processor.FLAGS.set_N()

def _tya(processor):
    processor.A.value = processor.Y.value
    if processor.A.value == 0:
        processor.FLAGS.set_Z()
    if processor.A.value & 128 == 0:
        processor.FLAGS.set_N()
