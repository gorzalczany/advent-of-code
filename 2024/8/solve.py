#!/usr/bin/python3
"""AOC 8th day."""
import sys
from collections import defaultdict
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

oob = lambda p, x: p.x < 0 or p.y < 0 or p.y > len(x)-1 or p.x > len(x[0])-1    
    
def projectAntinodes(tuple, map2d, resonant=False):
    a, b = tuple
    # create vectors
    ab = Coordinate(b.x-a.x, b.y-a.y)
    ba = Coordinate(a.x-b.x, a.y-b.y)
    # antinodes coordinates
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


def main(input_file):
    lines =  input_file.read().splitlines()

    antenas_map = []
    antenas = defaultdict(list)
    for coord_y, row in enumerate(lines):
        antenas_map.append([])
        for coord_x, value in enumerate(row): 
            antenas_map[coord_y].append(value)
            if value.isalnum(): 
                antenas[value].append(Coordinate(coord_x, coord_y))

    nodes_p1 = set()
    nodes_p2 = set()
    for frequency in antenas:
        alignment_list = list(combinations(antenas[frequency], 2))
        for aligned_points in alignment_list:
            for node in projectAntinodes(aligned_points, antenas_map):
                if not oob(node, antenas_map):
                    nodes_p1.add(node)
            for node in projectAntinodes(aligned_points, antenas_map, resonant=True):
                if not oob(node, antenas_map):
                    nodes_p2.add(node)
    print(len(nodes_p1))
    print(len(nodes_p2))

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))