#!/usr/bin/python3
"""AOC 7th day."""

import sys
from operator import mul, add
from functools import reduce
from itertools import product
            
def applyOperators(input, operators): 
    return reduce(lambda acc, v: operators[v[0]](acc, v[1]), enumerate(input[1::]), input[0])

def isPossiblyTrue(input, expected, operators):
    operators_combinations = product(operators, repeat=len(input)-1)
    for operators in operators_combinations:
        if applyOperators(input, operators) == expected: return True
    return False

def concat(a, b):
    return int(f"{a}{b}")

def main(input_file):
    lines =  input_file.read().splitlines()
    
    input = list(map(lambda raw_input: (int(raw_input[0]), list(map(int, raw_input[1].split()))),map(lambda line: line.split(":"),lines)))
    print(reduce(lambda acc, input: acc + input[0] if isPossiblyTrue(input[1], input[0], [mul, add]) else acc, input, 0))
    print(reduce(lambda acc, input: acc + input[0] if isPossiblyTrue(input[1], input[0], [mul, add, concat]) else acc, input, 0))

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))