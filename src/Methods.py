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

def _brk(processor, exit_status):
    sys.exit(exit_status)

def _rts(processor, memory_position):
    processor.PC.value = memory_position

#TODO: SBC

def _sec(processor):
    processor.FLAGS.set_C