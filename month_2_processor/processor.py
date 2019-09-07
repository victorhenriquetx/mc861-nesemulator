import os, sys
import src.Switcher as s


def emula(filename):
    # carrega arquivo em bytes p memo
    memo = readFile(filename)
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

def main():
    filename = sys.argv[1]
    emula(filename)


main()