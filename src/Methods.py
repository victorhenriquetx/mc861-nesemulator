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

def _lda(processor, memory_position):
    processor.A.value = processor.memory.read_memo(memory_position)

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

def _jmp(processor, instruction_param):
    pass

def _brk(processor, exit_status):
    sys.exit(exit_status)

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
    processor.X.value = processor.memory.read_stack(processor.STACK.value)

def _txs(processor):
    processor.memory.write_stack(processor.STACK.value, processor.X.value)

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
