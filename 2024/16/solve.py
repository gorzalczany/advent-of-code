#!/usr/bin/python3
"""AOC 16th day."""
import sys
from queue import Queue

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
 
    
class Maze:
    """
            N
        W       E
            S
   
        Maze is 2D array represented by `#` (walls) and `.`
        We are starting facing E        
    """
    def __init__(self, map, walls):
        self.map = map
        self.walls = set(walls)
        
    vectors = {
        "N": Vec2D(0, -1),
        "E": Vec2D(1, 0),
        "S": Vec2D(0, 1),
        "W": Vec2D(-1, 0)
    }
        
    rotations = {
        "none": 0,
        "clockwise": 1,
        "counterclockwise": -1
    }
        
    def rotateVector(self, vector, rotation):
        values = [self.vectors["N"], self.vectors["E"], self.vectors["S"], self.vectors["W"]]
        next_index = (values.index(vector) + rotation) % 4
        return values[next_index]
        
    def getVectorOrientation(self, vector):
        return  next(key for key, value in self.vectors.items() if value == vector)
    
    def score(self, distance, rotations):
        return distance + 1000*rotations  
    
    def possiblePaths(self, start: Vec2D, goal: Vec2D):
        queue = Queue()
        queue.put((start, []))
        
        successfullPaths = []
        
        while not queue.empty():
            node, path = queue.get()
            for v in self.vectors.values():
                next_node = node + v
                if next_node == goal:
                    successfullPaths.append(path + [next_node])
                if next_node not in self.walls and next_node not in path:
                    queue.put((next_node, path + [next_node]))
        return successfullPaths
    
    def solve(self, start: Vec2D, goal: Vec2D):
        successfullPaths = []        
        queue = Queue()
        queue.put((
            start, # first node
            [],    # path 
            "E",   # direction
            0      # rotations
        ))
        
        visited = {}
                
        while not queue.empty():
            node, path, direction, rotations = queue.get()
            vector = self.vectors[direction]
            score = self.score(len(path),rotations)
            # xD how to store it better?
            if visited.get(f"{node}-{direction}") is not None and visited.get(f"{node}-{direction}") < score:
                continue
                
            visited[f"{node}-{direction}"] = score
             
            for rotation_value in self.rotations.values():
                adjusted_v = self.rotateVector(vector, rotation_value)
                next_node = node + adjusted_v
                adjusted_d = self.getVectorOrientation(adjusted_v)                
                if next_node == goal:
                    s_path = path + [next_node]
                    score = self.score(len(s_path),rotations)
                    successfullPaths.append((s_path, score, len(s_path), rotations + abs(rotation_value)))
                if next_node not in self.walls and next_node not in path:
                    queue.put((next_node, path + [next_node], adjusted_d, rotations + abs(rotation_value)))
        return successfullPaths


def main(input_file):
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
    
    maze = Maze(maze_graph, maze_walls)
    solution = maze.solve(start, stop)
    best_score = min([score for _,score,_,_ in solution])
    
    #pt 1
    print(best_score)
    
    tiles = set()
    tiles.add(start)
    paths = [path for path,score,_,_ in solution if score == best_score]
    for path in paths:
        for tile in path:
            tiles.add(tile)
    
    #pt 2
    print(len(tiles))


if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))