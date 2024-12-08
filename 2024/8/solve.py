#!/usr/bin/python3
"""AOC 8th day."""
import sys
from itertools import combinations

class Coordinate(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if self.x != other.x : return False
        return self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
    def __repr__(self):
        return f"Coordinate({self.x},{self.y})"
    def __str__(self):
        return f"({self.x},{self.y})"

oob = lambda p, x: p.x < 0 or p.y < 0 or p.y > len(x)-1 or p.x > len(x[0])-1

def getAligned(coords):
    return list(combinations(coords, 2))
    
def projectAntinodes(tuple, map2d, resonant=False):
    a, b = tuple
    # create vectors
    ab = Coordinate(b.x-a.x, b.y-a.y)
    ba = Coordinate(a.x-b.x, a.y-b.y)
    # antynode points
    c1 = Coordinate(b.x+ab.x, b.y+ab.y) # b+ab
    c2 = Coordinate(a.x+ba.x, a.y+ba.y) # a+ba
    nodes = [c1,c2]
    
    if not resonant: return nodes
    nodes += [a,b]
    while not oob(c1, map2d):
        c1 = Coordinate(c1.x+ab.x, c1.y+ab.y)
        nodes.append(c1)
    while not oob(c2, map2d):
        c2 = Coordinate(c2.x+ba.x, c2.y+ba.y)
        nodes.append(c2)
    return nodes

def addAntinodeToMap(point, map2d):
    if not oob(point, map2d):
        map2d[point.y][point.x] = "#"
        
def printMap(array2D):
    for row in array2D:
        row_string = ''.join(str(tile) for tile in row)
        print(row_string)

def main(input_file):
    lines =  input_file.read().splitlines()

    antenas_map = []
    antenas = { }
    for cord_y, row in enumerate(lines):
        antenas_map.append([])
        for cord_x, value in enumerate(row): 
            if value.isalnum(): 
                coord = Coordinate(cord_x, cord_y)
                coords = antenas.get(value, [])
                coords.append(coord)
                antenas[value] = coords
            antenas_map[cord_y].append(value)

    nodes_p1 = set()
    nodes_p2 = set()
    for key in antenas:
        aligned_list = getAligned(antenas[key])
        for aligned in aligned_list:
            for node in projectAntinodes(aligned, antenas_map):
                if not oob(node, antenas_map):
                    nodes_p1.add(node)
            for node in projectAntinodes(aligned, antenas_map, resonant=True):
                if not oob(node, antenas_map):
                    nodes_p2.add(node)
    print(len(nodes_p1))
    print(len(nodes_p2))

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))