#!/usr/bin/python3
"""AOC 4th day."""
import sys

adjacency_list = [(0,1), (0,-1), (-1,0), (1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

def applyVector(a, ab):
    ax, ay = a
    dx, dy = ab
    return (ax+dx, ay+dy)

def getAccessibleRolls(grid):
    rolls = set()
    for y, row in enumerate(grid):
        for x, type in enumerate(row):
            if type != "@":
                continue
            if isAccessible((x, y), grid):
                rolls.add((x, y))
    return rolls    

def isAccessible(roll, grid):
    adjacentRolls = 0
    for vector in adjacency_list:
        next = applyVector(roll, vector)
        x, y = next
        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
            continue
        if grid[y][x] == "@":
            adjacentRolls += 1
        if adjacentRolls >= 4:
            return False
    return True

def removeAccessibleRolls(grid, rolls):
    for roll in rolls:
        x, y = roll
        grid[y][x] = "."                 

def main(input_file):
    lines =  input_file.read().splitlines()

    diagram = []
    for coord_y, row in enumerate(lines):
        diagram.append([])
        for coord_x, value in enumerate(row): 
            diagram[coord_y].append(value)
            
    accessible_rolls = getAccessibleRolls(diagram)
    solve_1 = len(accessible_rolls)
    solve_2 = solve_1
    while len(accessible_rolls) > 0:
        removeAccessibleRolls(diagram, accessible_rolls)
        accessible_rolls = getAccessibleRolls(diagram)
        solve_2 += len(accessible_rolls)

    
    print("pt1:", solve_1)
    print("pt2:", solve_2)           
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))