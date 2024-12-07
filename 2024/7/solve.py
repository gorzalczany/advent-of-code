#!/usr/bin/python3
"""AOC 7th day."""

from copy import deepcopy
from operator import mul, add
import itertools

def isCorrect(input, output, operators):
    operations_options = list(itertools.product(operators, repeat=len(input)-1))
    for operations in operations_options:
        numbers = deepcopy(input)
         # reduce numbers with operation
        acc = numbers.pop(0)
        for operation in operations: 
            acc = operation(acc, numbers.pop(0))
        if acc == output:
            print(output)
            return True
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
        test = int(test_value_txt)
        numbers  = list(map(int, numbers_txt.split()))

        if isCorrect(numbers, test, [mul, add]):
            sum += test
        if isCorrect(numbers, test, [mul, add, concat]):
            sum_with_concat += test
                
    print(sum)
    print(sum_with_concat)

main()