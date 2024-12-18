#!/usr/bin/python3
"""AOC 18th day."""
import sys
from queue import Queue 
import collections

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

class Memory:
    
    vectors = [(0,1), (0,-1), (-1,0), (1,0)]
    
    def __init__(self, size, corrupted_bytes):
        self.size = size
        self.corrupted_bytes = corrupted_bytes
        
    def shortest_path(self, start, goal):
        queue = Queue()
        queue.put((start,0))
        
        visited = set()
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
                        next_node not in self.corrupted_bytes,
                        next_node not in visited,
                        next_node.x >= 0 and next_node.y >= 0,
                        next_node.x < self.size and next_node.y < self.size
                    ]): 
                    queue.put((next_node, distance+1))
        return min_distance
        

def main(input_file, isTest):
    lines = input_file.read().splitlines()
    
    mem_size = 7 if isTest else 71
    bytes_arr = []
    
    fallen_count = 12 if isTest else 1024
    
    for line in lines:
        byte = Vec2D(*map(int, line.split(",")))
        bytes_arr.append(byte)
     
    # pt1
    mem = Memory(mem_size, bytes_arr[:fallen_count])
    solution = mem.shortest_path(Vec2D(0,0), Vec2D(mem_size-1, mem_size-1))
    print(solution)
    
    # pt2
    for i in range(fallen_count, len(bytes_arr)):
        mem = Memory(mem_size, bytes_arr[:i])
        solution = mem.shortest_path(Vec2D(0,0), Vec2D(mem_size-1, mem_size-1))
        if solution is None:
            print(bytes_arr[i-1])
            break
    


if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)