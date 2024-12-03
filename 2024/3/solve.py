#!/usr/bin/python3
"""AOC 3rd day."""

import re

def getInstructions(program, removeDisabled):
    if removeDisabled:
        program = removeDisabledFrom(program)
    return re.findall(r'mul\([0-9]+,[0-9]+\)', program)

def getValuesToMultiply(instruction):
    return list(map(int, re.findall(r'\d+', instruction)))

def removeDisabledFrom(program):
    program = re.sub('don\'t\(\).*?do\(\)', '', program)
    last_dont = re.search(r'don\'t\(\)', program)
    if last_dont:
        program = program[:last_dont.start()]
    return program

def multiply(pair):
    a, b = pair
    return a*b

def main():

    file = open('01.txt', 'r')
    program = file.read().replace('\n', '')

    # part 1
    instructions = getInstructions(program, False)
    toMultiply = list(map(getValuesToMultiply, instructions))
    multiplied = list(map(multiply, toMultiply))
    print('part 1: ', sum(multiplied))

    # part 2
    instructions = getInstructions(program, True)
    toMultiply = list(map(getValuesToMultiply, instructions))
    multiplied = list(map(multiply, toMultiply))
    print('part 2: ', sum(multiplied))

main()

