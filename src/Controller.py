ButtonA, ButtonB, ButtonSelect, ButtonStart, ButtonUp, ButtonDown, ButtonLeft, ButtonRight = range(8)

class Controller:
    def __init__(self):
        self.buttons = [False for _ in range(8)] 
        self.index = 0 
        self.strobe = 0 

    def SetButtons(self, buttons):
        self.buttons = buttons

    def Read(self):
        value = 0
        if self.index < 8 and self.buttons[self.index]:
            value = 1
        self.index += 1
        if self.strobe & 1 == 1:
            self.index = 0
        return value

    def Write(self, value):
        self.strobe = value
        if self.strobe & 1 == 1:
            self.index = 0