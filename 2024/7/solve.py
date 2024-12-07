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
    file = open('01.txt', 'r')
    lines = file.read().splitlines()
    
    sum = 0
    sum_with_concat = 0
    for line in lines:
        test_value_txt, numbers_txt = line.split(":")
        expected = int(test_value_txt)
        numbers  = list(map(int, numbers_txt.split()))

        if isPossiblyTrue(numbers, expected, [mul, add]):
            sum += expected
        if isPossiblyTrue(numbers, expected, [mul, add, concat]):
            sum_with_concat += expected
                
    print(sum)
    print(sum_with_concat)

main()