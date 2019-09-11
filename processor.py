import os
import sys
import src.Switcher as s
from src.registers import registers


def emula(filename, init_pos):
    # carrega arquivo em bytes p memo
    registers.MEMO = readFile(filename)
    registers.PC = init_pos

    while True:
        instruction = read_memo()
        decod_instruction, instruction_param = decode_instruction(instruction)

        a = s.Switcher()
        err = a.which_instruction(decod_instruction, instruction_param) # tratativa da instrucao no metodo de classe

        log(err)
        print(registers.X)
        break

# TODO implementar funcoes auxiliares


def readFile(filename):
    byte_str = open(filename, "rb").read()
    return list(byte_str)


def read_memo():
    registers.PC += 1
    return registers.MEMO[registers.PC - 1]


def decode_instruction(bin_instruction):
    # converte byte para string no formato do which_instruction
    # verificar qual a instrução e decidir quantos bytes a mais vai ter que ler (usando o read_memo)
    # cada instrução pode ter de 1 a 3 bytes (instrução no primeiro byte e valores no segundo/terceiro)
    if bin_instruction == int('01010000', 2): # 01010000 valor de exemplo
        memo_hi = read_memo()
        memo_lo = read_memo()
        return "_lda", memo_hi*256 + memo_lo
    elif bin_instruction == int('11011110', 2):
        return "_inx", False
    return ""


def log(err):
    return ""


def main():
    filename = sys.argv[1]
    emula(filename, 0)


if __name__ == "__main__":
    main()
