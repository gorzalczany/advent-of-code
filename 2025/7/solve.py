#!/usr/bin/python3
"""AOC 7th day."""
import sys
from collections import deque

moves = [(0,1)]

def applyVector(a, ab):
    ax, ay = a
    dx, dy = ab
    return (ax+dx, ay+dy)

def floodFill(matrix, start):
    fillQue = [start]
    flooded = set()
    splits = 0
    oob = lambda x, y:  x < 0 or x >= len(matrix[0]) or y < 0 or y >= len(matrix)
    
    while(len(fillQue)>0):
        x, y = fillQue.pop(0)
        if oob(x, y):
            continue
        if (matrix[y][x] == "." or matrix[y][x] == "S") and (x, y) not in flooded:
            flooded.add((x, y))
            for dx, dy in moves:
                fillQue.append((x + dx, y + dy))   
        if matrix[y][x] == '^' and (x, y):
            flooded.add((x, y))
            splits += 1
            fillQue.append((x + 1, y + 1))        
            fillQue.append((x - 1, y + 1))  
    print("splits: ", splits)      
    return flooded


def possiblePaths(matrix, start, paths_to_node = {}):
    next_node = (start[0], start[1]+1)
    if next_node[1] >= len(matrix):
        return 1
    next_node_symbol = matrix[ny][nx]
    if next_node_symbol == '^':
        if next_node in paths_to_node:
            return paths_to_node[next_node]
        paths_to_node[next_node] = 0
        nx, ny = next_node
        left_node = (nx-1, ny+1)
        right_node = (nx+1, ny+1)
        paths_to_node[next_node] += possiblePaths(matrix, left_node, paths_to_node)
        paths_to_node[next_node] += possiblePaths(matrix, right_node, paths_to_node)
        return paths_to_node[next_node]
    elif next_node_symbol == '.':
        return possiblePaths(matrix, next_node, paths_to_node)


def main(input_file):
    lines =  input_file.read().splitlines()

    diagram = []
    start = None
    for coord_y, row in enumerate(lines):
        diagram.append([])
        for coord_x, value in enumerate(row): 
            diagram[coord_y].append(value)
            if value == 'S':
                start = (coord_x, coord_y)
    floodFill(diagram, start)
    print(possiblePaths(diagram, start))            
        
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))