#!/usr/bin/python3
"""AOC 6th day."""
import sys
from functools import reduce

def get_column(matrix, index):
    return [row[index] for row in matrix]

def main(input_file):
    lines = input_file.readlines()

    last_row = lines[-1].rstrip('\n')
    col_lenghts = []
    current_col_length = 1
    for i in range(1,len(last_row)):
        if last_row[i] == ' ':
            current_col_length += 1
        else:
            col_lenghts.append(current_col_length-1)
            current_col_length = 1
        if i == len(last_row)-1:
            col_lenghts.append(current_col_length)
 
    matrix = []
    col_index = 0
    for idx, row in enumerate(lines):
        matrix.append([])
        while len(row) > 0:
            value = ''
            if col_index < len(col_lenghts):
                value = row[:col_lenghts[col_index]]
                row = row[col_lenghts[col_index]+1:]
            else:
                value = row
                row = ''
            matrix[idx].append(value)
            col_index += 1
        col_index = 0

    solution = 0
    solution_2 = 0
    for c_index in range(len(matrix[0])):
        column = get_column(matrix, c_index)
        operator = column.pop(-1).strip()
        if operator == '+':
            result = reduce(lambda a, b: int(a) + int(b), column)
        elif operator == '*':
            result = reduce(lambda a, b: int(a) * int(b), column)
        solution += result

        columnd_2d = []
        for value in column:
            columnd_2d.append(list(value))
        
        values = []
        for single_line_index in range(len(columnd_2d[0])):
            column_line = get_column(columnd_2d, single_line_index)
            value = int(''.join(column_line))
            values.append(value)
        if operator == '+':
            result_2 = reduce(lambda a, b: int(a) + int(b), values)
        elif operator == '*':
            result_2 = reduce(lambda a, b: int(a) * int(b), values)
        solution_2 += result_2
            
            
    print(solution)
    print(solution_2)
        
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))