class Memory():
    def __init__(self, initial, size):
        self.initial = initial
        self.size = size
        self.mem = []
        self.stack_offset = int('100', 16)

    def read_file(self, filename):
        with open(filename, 'rb') as file:
            byte_str = file.read()
        if self.size != -1:
            self.mem = list(byte_str)[self.initial:self.size]
        else:
            self.mem = list(byte_str)[self.initial:]

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
