#!/usr/bin/python3
"""AOC 4th day."""

import re
import numpy as np

def getDiags(a):
    a = np.array(a)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
    return [n.tolist() for n in diags]

def get_column(matrix, index):
    return [row[index] for row in matrix]

def getColumns(matrix):
    columns = []
    for i in range(0, len(matrix[0])):
        column = get_column(matrix, i)
        columns.append(column)
    return columns

def part1(matrix):
    columns = getColumns(matrix)
    diags = getDiags(matrix)
    diags = filter(lambda diag: len(diag) >= len("XMAS"), diags)

    strings = []
    for i in matrix:
        string = "".join(i)
        strings.append(string)
        strings.append(string[::-1])
    for i in columns:
        string = "".join(i)
        strings.append(string)
        strings.append(string[::-1])
    for i in diags:
        string = "".join(i)
        strings.append(string)
        strings.append(string[::-1])

    count = 0
    for string in strings:
        count += len(re.findall(r'XMAS', string))
    return count

def part2(matrix):
    def checkAtIndex(matrix, s_r, s_c, searching):
        """check if `searching` array is inside of `matrix` at index (s_r, s_c)"""
        if len(matrix[0]) < s_c + len(searching[0]):
            return False
        if len(matrix) < s_r + len(searching):
            return False
        
        for r, row in enumerate(searching):
            for c, value in enumerate(row):
                if value == ".":
                    continue
                if matrix[s_r + r][s_c + c] != value:
                    return False
        return True
    
    def count_sub(subArray, array):
        """count occurences of 2d array in another (bigger) 2d array"""
        count = 0
        for r, row in enumerate(array):
            for c, value in enumerate(row):
                if value != subArray[0][0]:
                    continue
                if checkAtIndex(array, r, c, subArray):
                    count += 1
        return count
    
    searching = [
        ["M", ".", "S"],
        [".", "A", "."],
        ["M", ".", "S"]
    ]

    count = 0
    for i in range(0, 4):
        searching = list(np.rot90(np.array(searching)))
        count += count_sub(searching, matrix)

    return count

def main():
    file = open('01.txt', 'r')
    lines = file.readlines()

    matrix = []
    for idx, row in enumerate(lines):
        matrix.append([])
        for value in row: 
            if value == '\n':
                continue
            matrix[idx].append(value)

    print("part 1:", part1(matrix))
    print("part 2:", part2(matrix))

main()

