import os
import src.Switcher as s


def emula():
    # carrega arquivo em bytes p memo
    memo = readFile()
    pc = init_pos

    while True:
        instruction = read_memo(pc)
        decod_instruction = decodeInstruction(instruction) # reconverter p strings?

        a = s.Switcher()
        err = a.which_instruction(decod_instruction) # tratativa da instrucao no metodo de classe

        log(err)

#TODO implementar funcoes auxiliares


def readFile(filename):
    return open(filename, "rb").read()  

def decodeInstruction():
    return ""

def log():
    return ""

emula()
