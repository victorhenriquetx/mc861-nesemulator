import sys


def _adc(processor, instruction_param):
        processor.A.value += instruction_param

        if processor.A.check_overflow():
            processor.A.value -= 255
            processor.FLAGS.set_C()
            processor.FLAGS.set_V()
        if processor.A.is_negative():
            processor.FLAGS.set_N()
        if processor.A.value == 0:
            processor.FLAGS.set_Z()

def _lda(processor, memory_position):
    processor.A.value = processor.memory.read_memo(memory_position)

def _sta(processor, memory_position):
        processor.memory.write_memo(memory_position, processor.A.value)
        # TODO: Set flags

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
