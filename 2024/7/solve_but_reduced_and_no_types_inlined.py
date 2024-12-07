#!/usr/bin/python3
"""AOC 7th day."""

import sys
from operator import mul, add
from functools import reduce
from itertools import product, takewhile

def main(input_file):
    lines =  input_file.read().splitlines()
    input = list(map(lambda raw_input: (int(raw_input[0]), list(map(int, raw_input[1].split()))),map(lambda line: line.split(":"),lines)))
    test = lambda i,e,o: len(list(takewhile(lambda op: reduce(lambda acc, v: op[v[0]](acc, v[1]), enumerate(i[1::]), i[0]) != e, o))) < len(o)
    print(reduce(lambda acc, input: acc + input[0] if test(input[1], input[0], list(product([mul, add], repeat=len(input[1])-1))) else acc, input, 0))
    print(reduce(lambda acc, input: acc + input[0] if test(input[1], input[0], list(product([mul, add, lambda a,b: int(f"{a}{b}")], repeat=len(input[1])-1))) else acc, input, 0))

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))