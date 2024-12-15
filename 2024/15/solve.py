#!/usr/bin/python3
"""AOC 15th day."""
import sys

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
        return False
    
vectors = {
    "^": Vec2D(0, -1),
    ">": Vec2D(1, 0),
    "v": Vec2D(0, 1),
    "<": Vec2D(-1, 0)
}

class Size:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def __iter__(self):
        yield self.w
        yield self.h
        
class Object:
    def __init__(self, p: Vec2D, movable):
        self.p = p
        self.movable = movable
    
class Robot:
    def __init__(self, p: Vec2D, v: Vec2D):
        self.p = p
        self.v = v
    def getNextPos(self):
        return self.p.copy() + self.v
    def move(self):
        self.p += self.v    

def printWarehouse(objects, robot, size):
    toPrint = objects
    for y in range(size.h):
        string = ""
        for x in range(size.w):
            if robot.p ==  Vec2D(x,y):
                string += "@"
                continue
            
            o = next((o for o in toPrint if o.p == Vec2D(x,y)), None)
            if o is None:
                string += "."
            elif o.movable:
                string += "O"
            else: 
                string += "#"
        print(string)

def moveObject(object, objects, vector):
    started_at = object.p.copy()
    if object.movable:
        next_p = object.p + vector
        next_o = next((x for x in objects if x.p == next_p), None)
        if next_o is None:
            object.p = next_p
        else:
            _, moved  = moveObject(next_o, objects, vector)
            if moved:
                object.p = next_p
    moved = started_at != object.p
    return (object, moved)

def main(input_file):
    warehouse_raw, moves_raw = input_file.read().split("\n\n")
    moves_raw = moves_raw.replace("\n", "")
    
    robot_at = Robot(Vec2D(0,0),Vec2D(0,0))
    
    warehouse = []
    objects = []
    for coord_y, row in enumerate(warehouse_raw.splitlines()):
        warehouse.append([])
        for coord_x, value in enumerate(row):
            if value == "@":
                robot_at = Robot(Vec2D(coord_x,coord_y),Vec2D(0,0))
                warehouse[coord_y].append(".")
            else: 
                warehouse[coord_y].append(value)
            if value == "#":
                objects.append(Object(Vec2D(coord_x, coord_y), False))
            if value == "O":
                objects.append(Object(Vec2D(coord_x, coord_y), True))

    for move_raw in moves_raw:
        move = vectors[move_raw]
        next_p = robot_at.p.copy() + move
        next_o = next((x for x in objects if x.p == next_p), None)
        if next_o is not None:
            _, moved = moveObject(next_o,objects,move)
            if moved:
                robot_at.p = next_p
        else:
            robot_at.p = next_p
            
    # warehouse_size = Size(len(warehouse[0]), len(warehouse))        
    # printWarehouse(objects, robot_at, warehouse_size)

    pt1 = sum(map(lambda o: o.p.y * 100 + o.p.x , filter(lambda o: o.movable, objects)))
    print(pt1)
    

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    if env_test_run:
        main(open('00.txt')) 
    else: 
        main(open('01.txt'))
