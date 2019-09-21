class Memory():
    def __init__(self, size):
        self.size = size
        self.mem = []
        self.stack_offset = int('100', 16)

    def read_file(self, filename):
        byte_str = open(filename, "rb").read()
        self.mem = list(byte_str)

    def read_memo(self, position):
        return self.mem[position]

    def pop_stack(self, stack_register):
        stack_register.value -= 1
        return self.mem[self.stack_offset + stack_register.value]

    def push_stack(self, stack_register, value):
        self.mem[self.stack_offset + stack_register] = value
        stack_register.value += 1
    
    def write_memo(self, position, value):
        self.mem[position] = value
