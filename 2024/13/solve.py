#!/usr/bin/python3
"""AOC 13th day."""
import sys
from sympy import symbols, Eq, solve 
import re

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)


def countTokens(configs, price_position_correction=Vec2D(0, 0)):
    regx_pattern= r'\d+\.\d+|\d+'
    totalCost = 0

    for config in configs:
        a, b, p = config.split("\n")

        a = Vec2D(*map(int, re.findall(regx_pattern, a)))
        b = Vec2D(*map(int, re.findall(regx_pattern, b)))
        p = Vec2D(*map(int, re.findall(regx_pattern, p))) + price_position_correction

        x, y = symbols('x,y') 
        eq1 = Eq((a.x * x + b.x * y), p.x)
        eq2 = Eq((a.y * x + b.y * y), p.y)  
        x, y = solve((eq1, eq2), (x, y)).values()

        if x.is_Integer and y.is_Integer:
            totalCost += 3 * x + y
    return totalCost


def main(input_file):

    configs = input_file.read().split("\n\n")

    print("Part 1:", countTokens(configs))
    print("Part 2:", countTokens(configs, Vec2D(10000000000000, 10000000000000)))


if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))