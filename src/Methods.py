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
    if(!processor.FLAGS.is_C()):
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
    if(!processor.FLAGS.is_Z()):
        processor.PC = memory_position
def _bpl(processor, memory_position):
    if(!processor.FLAGS.is_N()):
        processor.PC = memory_position
def _bvc(processor, memory_position):
    if(!processor.FLAGS.is_V()):
        processor.PC = memory_position
def _bvs(processor, memory_position):
    if(processor.FLAGS.is_V()):
        processor.PC = memory_position

def _lda(processor, memory_position):
    processor.A.value = processor.memory.read_memo(memory_position)

def _sta(processor, memory_position):
        processor.memory.write_memo(memory_position, processor.A.value)
        # TODO: Set flags

def _brk(processor, exit_status):
    sys.exit(exit_status)
