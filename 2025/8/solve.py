#!/usr/bin/python3
"""AOC 8th day."""
import sys
import math
from functools import reduce
import itertools

class Circuit():
    def  __init__(self, boxes = []):
        self.boxes = set(boxes)
    
    def __repr__(self):
        return f'{list(self.boxes)}'


def get_distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2)


def find_closest_boxes(boxes):
    closest_boxes = []
    combinations = itertools.combinations(boxes, 2)
    for combo in combinations:
        box1, box2 = combo
        distance = get_distance(box1, box2)
        closest_boxes.append((box1, box2, distance))
    closest_boxes.sort(key=lambda x: x[2])
    return closest_boxes


def solve(boxes, limit):
    circuits = list(map(lambda b: Circuit([b]), boxes))
    closest_boxes = find_closest_boxes(boxes)
    connections = 0
    for jb1, jb2, d in closest_boxes:
        c1 = list(filter(lambda c: jb1 in c.boxes, circuits))[0]
        c2 = list(filter(lambda c: jb2 in c.boxes, circuits))[0]

        if c1 != c2:
            joined = Circuit(c1.boxes.union(c2.boxes))
            circuits.remove(c1)
            circuits.remove(c2)
            circuits.append(joined)
        connections += 1       

        if connections == limit:
            circuits.sort(key=lambda c: len(c.boxes), reverse=True)
            largest_circuits = circuits[:3]
            solution = reduce(lambda acc, c: acc * len(c.boxes), largest_circuits, 1)
            print("p1: ", solution)

        if len(circuits) == 1:
            print("p2: ", jb1[0] *jb2[0])
            break


def main(input_file, limit):
    lines =  input_file.read().splitlines()

    boxes = []
    for index, line in enumerate(lines):
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))
    
    solve(boxes, limit)

                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'), 1000 if not env_test_run else 10)