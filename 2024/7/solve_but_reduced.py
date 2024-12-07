#!/usr/bin/python3
"""AOC 7th day."""

from operator import mul, add
from functools import reduce
from itertools import product

class Indexed:
    def __init__(self, index_and_value):
        (self.index, self.value) = index_and_value
            
def applyOperators(input, operators): 
    return reduce(lambda acc, next: operators[next.index](acc, next.value), map(Indexed, enumerate(input[1::])), input[0])

def isPossiblyTrue(input, expected, operators):
    operators_combinations = product(operators, repeat=len(input)-1)
    for operators in operators_combinations:
        if applyOperators(input, operators) == expected: return True
    return False

def concat(a, b):
    return int(f"{a}{b}")

def main():
    lines =  open('01.txt', 'r').read().splitlines()
    
    class Input:
        def __init__(self, tuple):
            self.expected = tuple[0]
            self.numbers = tuple[1]
    
    input = list(map(Input, map(lambda raw_input: (int(raw_input[0]), list(map(int, raw_input[1].split()))),map(lambda line: line.split(":"),lines))))
    print(reduce(lambda acc, next: acc + next.expected if isPossiblyTrue(next.numbers, next.expected, [mul, add]) else acc, input, 0))
    print(reduce(lambda acc, next: acc + next.expected if isPossiblyTrue(next.numbers, next.expected, [mul, add, concat]) else acc, input, 0))

main()