#!/usr/bin/python3
"""AOC 17th day."""
import sys
  
def getCombo(operand, registers):
    assert(operand != 7)
    if operand in range(4): return operand
    if operand == 4: return registers['A']
    if operand == 5: return registers['B']
    if operand == 6: return registers['C']
 
def adv(operand, registers, output):
    combo = getCombo(operand, registers)
    registers['A'] = int(registers['A']/(2**combo))

def bxl(operand, registers, output):
    registers['B'] = registers['B']^operand

def bst(operand, registers, output):
    combo = getCombo(operand, registers)
    registers['B'] = combo%8

def jnz(operand, registers, output):
    if registers['A'] == 0:
        return None
    else: return operand
    
def bxc(operand, registers, output):
    registers['B'] = registers['B']^registers['C']

def out(operand, registers, output):
    combo = getCombo(operand, registers)
    output.append(combo%8)

def bdv(operand, registers, output):
    combo = getCombo(operand, registers)
    registers['B'] =  int(registers['A']/(2**combo))
    
def cdv(operand, registers, output):
    combo = getCombo(operand, registers)
    registers['C'] =  int(registers['A']/(2**combo))
    
def run(program, instructions, registers, braker=False):
    output = []
    pointer = 0
    while True:
        if braker and len(output) > len(program):
            break
        if pointer+1 > len(program)-1:
            break
        instruction = instructions[program[pointer]]
        operand = program[pointer+1]
        jump = instruction(operand, registers, output)
        pointer = jump if jump is not None else pointer+2
    return output

def main(input_file):
    lines = input_file.read().splitlines()
    
    registers = {
        'A': 0,
        'B': 0,
        'C': 0
    }
    
    for i in range (3):
        register = lines[i].split(":")
        registers[register[0][-1]] = int(register[1])
     
    program = list(map(int, lines[4].split(":")[1].split(",")))
    
    instructions = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }
    
    # pt1 
    output = run(program, instructions, registers)
    print(",".join(map(str, output)))


if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))