#!/usr/bin/python3
"""AOC 20th day."""
import sys
from queue import Queue
from collections import Counter

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)
    
    def scale(self, scalar):
        return Vec2D(self.x * scalar, self.y * scalar)   
    
    def copy(self):
        return Vec2D(self.x, self.y)
    
    def __str__(self):
        return f"({self.x},{self.y})"
    
    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def __hash__(self):
        return hash(f"{self.x}-{self.y}")
    
    def __eq__(self, other):
        if isinstance(other, Vec2D):
            return self.x == other.x and self.y == other.y
 
    
class RaceTrack:
    
    vectors = [(0,1), (0,-1), (-1,0), (1,0)]
    wall_to_skip = None
    
    def __init__(self, size, walls):
        self.size = size
        self.walls = walls
      
      
    def shortest_path(self, start, goal, cheat=False):
        queue = Queue()
        queue.put((start,0))
        
        visited = set()
        cheat_nodes = set()
        min_distance = None
        
        while not queue.empty():
            node, distance = queue.get()
            
            if node in visited:
                continue
            
            visited.add(node)
            
            for dx, dy in self.vectors:
                next_node = node + Vec2D(dx, dy)
                if next_node == goal:
                    min_distance = distance+1 if min_distance is None else min(min_distance, distance+1)
                    
                if all([
                        next_node not in self.walls,
                        next_node not in visited,
                        next_node.x >= 0 and next_node.y >= 0,
                        next_node.x < self.size and next_node.y < self.size
                    ]) or next_node == self.wall_to_skip: 
                    queue.put((next_node, distance+1))
                    
                cheat_node_end = node + Vec2D(dx, dy).scale(2)
                if all([
                        next_node in self.walls,
                        cheat,
                        cheat_node_end not in self.walls,
                        cheat_node_end.x >= 0 and cheat_node_end.y >= 0,
                        cheat_node_end.x < self.size and cheat_node_end.y < self.size
                    ]):
                    cheat_nodes.add((next_node, cheat_node_end, distance+2))
                
        return min_distance, cheat_nodes
    
    
    def getDistanceToEveryOtherPoint(self, start):
        queue = Queue()
        queue.put((start,0))
        
        visited = set()        
        distances = {start: 0}
        
        while not queue.empty():
            node, distance = queue.get()
            
            if node in visited:
                continue
            
            visited.add(node)
            
            for dx, dy in self.vectors:
                next_node = node + Vec2D(dx, dy)
                    
                if all([
                        next_node not in self.walls,
                        next_node not in visited,
                        next_node.x >= 0 and next_node.y >= 0,
                        next_node.x < self.size and next_node.y < self.size
                    ]) or next_node == self.wall_to_skip: 
                    queue.put((next_node, distance+1))
                    distances[next_node] = distance+1                
        return distances


def main(input_file, isTest):
    lines =  input_file.read().splitlines()

    maze_graph = []
    maze_walls = set()
    start = Vec2D(0,0)
    stop = Vec2D(0,0)
    for coord_y, row in enumerate(lines):
        maze_graph.append(["."]*len(row))
        for coord_x, value in enumerate(row):
            vec = Vec2D(coord_x, coord_y)
            if value == "S":
                start = vec
            elif value == "E":
                stop = vec
            elif value == "#":
                maze_walls.add(vec)
                maze_graph[coord_y][coord_x] = "#"
    
    track = RaceTrack(len(maze_graph), maze_walls)
    min_distance, cheat_nodes = track.shortest_path(start, stop, cheat=True)

    distances_to_end = track.getDistanceToEveryOtherPoint(stop)
    start_to_end_distance = min_distance
    
    # pt 1
    counter = Counter()
    for cheat_s, cheat_e, traveled_to_cheat in cheat_nodes:
        cheat_to_end = distances_to_end[cheat_e]
        start_to_cheat = traveled_to_cheat
        diff = start_to_end_distance - (start_to_cheat + cheat_to_end)
        if diff >= 0 if isTest else 100:
            counter[diff] += 1
        
    items = list(counter.items())
    items.sort(key=lambda item: item[0])
    for dist, c in items:
        print(f"{c} cheats saves: {dist}")        
    print("cheats:", sum(counter.values()))
    

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)