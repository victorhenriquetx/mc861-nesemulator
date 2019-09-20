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