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

def _sta(processor, memory_position):
        processor.memory.write_memo(memory_position, processor.A.value)
        # TODO: Set flags

<<<<<<< HEAD
def _jsr(processor, address, next_instruction):
    processor.memory.push_stack(processor.STACK, next_instruction)
    processor.PC.value = address
=======

def _jsr(processor, memory_position):
    
>>>>>>> 0d77432e91c2f79a0fae82e3c63894baadef85c4

def _brk(processor, exit_status):
    print("Exit with status", exit_status)
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