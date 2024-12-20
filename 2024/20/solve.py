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
        
    def taxicabDistance(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y)
 
    
class RaceTrack:
    
    vectors = [(0,1), (0,-1), (-1,0), (1,0)]
    
    def __init__(self, size, walls, track):
        self.size = size
        self.walls = walls
        self.track = list(track)
      
    def getShortestAndCheats(self, start, goal, cheat_range):
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
                    ]): 
                    queue.put((next_node, distance+1))
                
                cheat_filter = lambda cheat_end: all([
                            cheat_end != next_node,
                            cheat_end not in self.walls,
                            cheat_end.x >= 0 and cheat_end.y >= 0,
                            cheat_end.x < self.size and cheat_end.y < self.size
                        ])
                potential_cheats = self.getCheets(node, cheat_range)
                cheats_ends = list(filter(cheat_filter, potential_cheats))
                cheats = [(node, cheat_end) for cheat_end in cheats_ends]
                for cheat in cheats:
                    if (cheat[1], cheat[0]) not in cheat_nodes:
                        cheat_nodes.add(cheat)                
                
        return min_distance, cheat_nodes
    
    def getCheets(self, from_point, max_distance):
        return [point for point in self.track if 1 < point.taxicabDistance(from_point) <= max_distance]
        
    
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
                    ]): 
                    queue.put((next_node, distance+1))
                    distances[next_node] = distance+1                
        return distances

def printCheats(counter: Counter, prefix, break_down = False):
    items = list(counter.items())
    if break_down:
        items.sort(key=lambda item: item[0])
        for dist, c in items:
            print(f"{c} cheats saves: {dist}")        
    print(prefix, "cheats:", sum(counter.values()))

def main(input_file, isTest):
    lines =  input_file.read().splitlines()

    track_map = []
    track_walls = set()
    track_coords = set()
    start = Vec2D(0,0)
    stop = Vec2D(0,0)
    for coord_y, row in enumerate(lines):
        track_map.append(["."]*len(row))
        for coord_x, value in enumerate(row):
            vec = Vec2D(coord_x, coord_y)
            if value != "#":
                track_coords.add(vec)
            if value == "S":
                start = vec
            elif value == "E":
                stop = vec
            elif value == "#":
                track_walls.add(vec)
                track_map[coord_y][coord_x] = "#"
    
    track = RaceTrack(len(track_map), track_walls, track_coords)
    
    distances_to_end = track.getDistanceToEveryOtherPoint(stop)
    
    # pt 1
    counter = Counter()
    min_distance, cheat_nodes = track.getShortestAndCheats(start, stop, cheat_range=2)
    for cheat_s, cheat_e in cheat_nodes:
        cheat_start_to_end = distances_to_end[cheat_e]
        cheat_end_to_end = distances_to_end[cheat_s]
        diff = abs(cheat_start_to_end - cheat_end_to_end) - cheat_s.taxicabDistance(cheat_e)
        if diff >= (0 if isTest else 100):
            counter[diff]+=1  
    printCheats(counter, "pt1")
            
    # pt 2
    counter = Counter()
    min_distance, cheat_nodes = track.getShortestAndCheats(start, stop, cheat_range=20)
    for cheat_s, cheat_e in cheat_nodes:
        cheat_start_to_end = distances_to_end[cheat_e]
        cheat_end_to_end = distances_to_end[cheat_s]
        distance = cheat_s.taxicabDistance(cheat_e)
        
        diff = abs(cheat_start_to_end - cheat_end_to_end) - distance
        if diff >= (50 if isTest else 100):
            counter[diff] += 1
    printCheats(counter, "pt2")   

    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)