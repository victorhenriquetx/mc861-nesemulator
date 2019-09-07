import os
from . import Switcher as s


def emula():
    memo = readFile()
    pc = init_pos

    while True:
        instruction = read_memo(pc)
        decod_instruction = decodeInstruction(instruction)

        a = s.Switcher()
        err = a.which_instruction(decod_instruction)



def readFile():
    return ""

def decodeInstruction():
    return ""


emula()
