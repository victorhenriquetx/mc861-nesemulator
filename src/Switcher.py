import os
from .registers import registers


class Switcher(object):
    def which_instruction(self, method_name, instruction_param):

        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid month")
        # Call the method as we return it
        return method(instruction_param)

    def _adc(self):
        return "add with carry"

    def _and(self):
        return "and logic op"

    def _asl(self):
        return "shift left"

    def _inx(self, instruction_param):
        registers.X += 1
        # TODO set flags (this is only an example)
        registers.FLAGS = registers.FLAGS | 8

    # TODO all instructions
