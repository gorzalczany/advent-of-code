#!/usr/bin/python3
"""AOC 6th day."""
from copy import deepcopy

class Coordinate(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if self.x != other.x : return False
        return self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))

vectors = [             # ordered
    Coordinate(0, -1),  # "^": 
    Coordinate(1, 0),   # ">": 
    Coordinate(0, 1),   # "V": 
    Coordinate(-1, 0),  # "<":  
]

def changeDirection(vector):
    next_index = vectors.index(vector) + 1
    return vectors[next_index if next_index < 4 else 0]

def get_next(lab_map, current_position, vector, obstacle=None):
    p = current_position
    n = Coordinate(p.x + vector.x, y= p.y + vector.y)
    l = len(lab_map)
    if n.x < 0 or n.y < 0 or n.y > l-1 or n.x > l-1:
        return None
    if obstacle and n.x == obstacle.x and n.y == obstacle.y:
        vector = changeDirection(vector)
        return get_next(lab_map, current_position, vector, obstacle) 
    if lab_map[n.y][n.x] == "#":
        vector = changeDirection(vector)
        return get_next(lab_map, current_position, vector, obstacle)
    return (n, vector)

def get_path(lab_map, starting_position):
	current = starting_position
	path = [current]
	vector = vectors[0]
	while(True):
		next = get_next(lab_map, current, vector)
		if next != None:
			current, vector = next
			path.append(current)
		else:
			break
	return path

def count_loops(lab_map, starting_position: Coordinate, guard_path):
    loops_count = 0
    for obstacle in guard_path:
        current = deepcopy(starting_position)
        vector = vectors[0]
        been_there = set()
        while(True):
            next = get_next(lab_map, current, vector, obstacle)
            if not next: break
            current, vector = next
            if next in been_there:
                loops_count += 1
                break
            been_there.add(next)
    return loops_count

def main():
	file = open('01.txt', 'r')
	lines = file.read().splitlines()

	lab_map = []
	starting_position = Coordinate(0,0)
	for cord_y, row in enumerate(lines):
		lab_map.append([])
		for cord_x, value in enumerate(row): 
			if value == "^":
				starting_position = Coordinate(cord_x, cord_y)
			lab_map[cord_y].append(value)

	# p1
	guard_path = list(set(get_path(lab_map, starting_position)))
	print(len(guard_path))

	# pt2
	print(count_loops(lab_map, starting_position, guard_path))

main()
