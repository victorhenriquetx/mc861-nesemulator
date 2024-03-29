class Memory():
    def __init__(self, initial, size):
        self.initial = initial
        self.size = size
        self.mem = [0] * (int('ffff', 16) + 1)
        self.stack_offset = int('100', 16)
        self.prg_size = 16384
    
    def set_prg_size(self, size):
        self.prg_size = size

    def read_file(self, filename):
        with open(filename, 'rb') as file:
            byte_str = file.read()
        if self.size != -1:
            if self.initial + self.size == 0:
                self.mem = list(byte_str)[self.initial:]
            else:
                self.mem = list(byte_str)[self.initial:self.initial + self.size]
        else:
            
            # a = list(byte_str)[self.initial:]
            # print(len(a))
            # print([hex(i) for i in a[:20]])
            # print([hex(i) for i in a[-20:]])
            
            
            self.mem[int('ffff', 16) - self.prg_size +1:] = list(byte_str)[self.initial:]
            # print('size: ', end=' ')
            # print(len(list(byte_str)[self.initial:]))
            

    def read_memo(self, position):
        return self.mem[position]
    
    def read_range_memo(self, position, p_range):
        return self.mem[position:position+p_range]

    def pop_stack(self, stack_register):
        stack_register.value += 1
        return self.mem[self.stack_offset + stack_register.value]

    def push_stack(self, stack_register, value):
        self.mem[self.stack_offset + stack_register.value] = value
        stack_register.value -= 1
    
    def write_memo(self, position, value):
        self.mem[position] = value
        
    def write_stack(self, stack_register, value):
        self.mem[self.stack_offset + stack_register] = value

    def read_stack(self, stack_register):
        return self.mem[self.stack_offset + stack_register]