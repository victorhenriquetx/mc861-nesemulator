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
    if not is_immediate:
        value = processor.memory.read_memo(instruction_param)
    else:
        value = instruction_param
    if processor.A.value >= value:
        processor.FLAGS.set_C()
    if processor.A.value == value:
        processor.FLAGS.set_Z()
    if processor.A.value >= int('80', 16):
        processor.FLAGS.set_N()

def _brk(processor, exit_status):
    sys.exit(exit_status)
