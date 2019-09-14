class Memory():
    def __init__(self, size):
        self.size = size
        self.mem = []

    def read_file(self, filename):
        byte_str = open(filename, "rb").read()
        self.mem = list(byte_str)

    def read_memo(self, position):
        return self.mem[position]
    
    def write_memo(self, position, value):
        self.mem[position] = value
