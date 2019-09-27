class Register():
    def __init__(self):
        self.value = 0

    # def __get__(self, instance, owner):
    #     return instance.value

    # def __set__(self, instance, new_value):
    #     instance.value = new_value

    # def __add__(self, value):
    #     return self.value + value

    # def __iadd__(self, value):
    #     self.value += value


class Register8bit(Register):
    def is_negative(self):
        return self.value > 127

    def check_overflow(self):
        return self.value > 255


class RegisterFlag(Register8bit):
    def set_N(self):
        self.value = self.value | 128

    def clear_N(self):
        self.value = self.value & 128

    def set_V(self):
        self.value = self.value | 64

    def clear_V(self):
        self.value = self.value & 64
    
    def set_B(self):
        self.value = self.value | 16

    def clear_B(self):
        self.value = self.value & 16
    
    def set_D(self):
        self.value = self.value | 8
    
    def clear_D(self):
        self.value = self.value & 8
    
    def set_I(self):
        self.value = self.value | 4

    def clear_I(self):
        self.value = self.value & 4

    def set_Z(self):
        self.value = self.value | 2

    def clear_Z(self):
        self.value = self.value & 2

    def set_C(self):
        self.value = self.value | 1
    
    def clear_N(self):
        self.value &= ~(1 << 7)

    def clear_V(self):
        self.value &= ~(1 << 6)

    def clear_B(self):
        self.value &= ~(1 << 5)

    def clear_D(self):
        self.value &= ~(1 << 4)

    def clear_I(self):
        self.value &= ~(1 << 3)

    def clear_Z(self):
        self.value &= ~(1 << 2)

    def clear_C(self):
        self.value &= ~(1 << 1)

    def is_N(self):
        return 1 if self.value & 128 == 128 else 0

    def is_V(self):
        return 1 if self.value & 64 == 64 else 0

    def is_B(self):
        return 1 if self.value & 16 == 16 else 0

    def is_D(self):
        return 1 if self.value & 8 == 8 else 0

    def is_I(self):
        return 1 if self.value & 4 == 4 else 0

    def is_Z(self):
        return 1 if self.value & 2 == 2 else 0

    def is_C(self):
        return 1 if self.value & 1 == 1 else 0

class Register16bit(Register):
    def is_negative(self):
        return self.value > 32767

    def check_overflow(self):
        return self.value > 65535

    def increment(self):
        self.value += 1


class RegistersList():
    def __init__(self):
        self.X = Register8bit()
        self.Y = Register8bit()
        self.A = Register8bit()
        self.F = RegisterFlag()
        
        self.PC = Register16bit()