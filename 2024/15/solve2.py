#!/usr/bin/python3
"""AOC 15th day."""
import sys
import time

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)
    
    def scale(self, scalar):
        return Vec2D(self.x * scalar, self.y * scalar)   
    
    def scaleX(self, scalar):
        return Vec2D(self.x * scalar, self.y)   

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
    def __iter__(self):
        yield self.x
        yield self.y
    
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
    printed = False
    def __init__(self, coordinates, movable):
        self.coords = coordinates
        self.movable = movable
    
class Robot:
    def __init__(self, p: Vec2D):
        self.p = p
        
# CURSOR ANSI ESCAPE PATTERNS
CURSOR_UP = '\033[1A'  # moves cursor up one line
CURSOR_DOWN = '\033[1B'  # moves cursor up one line
CURSOR_RESET = '\033[u'  # resets the cursor
CURSOR_OFF = '\033[?25l'  # makes cursor invisible
CURSOR_ON = '\033[?25h'# makes cursor visible
CURSOR_SAVE_POS = '\033[s'  # saves cursor position
CURSOR_RESTORE_POS = '\033[u'# returns cursor to last saved position

def printWarehouse(objects, robot, size):
    sys.stdout.flush()
    for o in objects:
        o.printed = False
    for y in range(size.h):
        string = ""
        x = 0
        while x < size.w * 2:
            if robot.p ==  Vec2D(x,y):
                string += "🤖"
                x+=1
                continue
            
            searchVector = Vec2D(x,y)
            o = next((x for x in objects if any(coord == searchVector for coord in x.coords) and not x.printed), None)
            if o is None:
                string += "  "
                x+=1
                continue
            elif o.movable:
                string += "⬜⬜"
            else: 
                string += "🟥🟥"
            o.printed = True
            x+=2
        for char in string: sys.stdout.write(char)
        sys.stdout.write('\n')
    sys.stdout.write(CURSOR_UP*size.h)
    time.sleep(1/10)


def getAllNextObjects(object, objects, vector):
    next_objects = []
    for p in object.coords:
        next_p = p + vector
        next_o = next((x for x in objects if any(coord == next_p for coord in x.coords) and x.coords != object.coords), None)
        if next_o is not None:
            next_objects = [*next_objects, *getAllNextObjects(next_o, objects, vector), next_o]
    return next_objects


def moveObject(object, objects, vector):
    if not canMove(object, objects, vector):
        return (object, False)
    
    objects_to_move = [*getAllNextObjects(object, objects, vector), object]
    for object in set(objects_to_move):
        object.coords = [coord + vector for coord in object.coords]
                
    return (object, True)

def canMove(object, objects, vector):
    if not object.movable: 
        return False
       
    next_objects = set()
    for p in object.coords:
        next_p = p + vector
        next_o = next((x for x in objects if any(coord == next_p for coord in x.coords) and x.coords != object.coords), None)
        if next_o is not None:
            next_objects.add(next_o)
    if len(next_objects) == 0:
        return True
    return all(canMove(object, objects, vector) for object in next_objects)
                

def main(input_file):
    warehouse_raw, moves_raw = input_file.read().split("\n\n")
    moves_raw = moves_raw.replace("\n", "")
    warehouse_raw = warehouse_raw.splitlines()
    
    robot_at = Robot(Vec2D(0,0))
    
    objects = []
    size = Size(len(warehouse_raw[0]),len(warehouse_raw))
    for coord_y, row in enumerate(warehouse_raw):
        for coord_x, value in enumerate(row):
            coord = Vec2D(coord_x,coord_y).scaleX(2)
            if value == "@":
                robot_at = Robot(coord.copy())
            if value == "#":
                objects.append(Object([coord.copy(), coord+Vec2D(1,0)], False))
            if value == "O":
                 objects.append(Object([coord.copy(), coord+Vec2D(1,0)], True))

    # print("initial")
    # printWarehouse(objects, robot_at, size)
    sys.stdout.write(CURSOR_OFF)
    for i, move_raw in enumerate(moves_raw):
        move = vectors[move_raw]
        next_p = robot_at.p.copy() + move
        next_o = next((x for x in objects if any(coord == next_p for coord in x.coords)), None)
        if next_o is not None:
            _, moved = moveObject(next_o,objects,move)
            if moved:
                robot_at.p = next_p
        else:
            robot_at.p = next_p
        
        printWarehouse(objects, robot_at, size)
        None # for breakpoint
            
    sys.stdout.write(CURSOR_RESTORE_POS)
    sys.stdout.write(CURSOR_ON)
    result = sum(map(lambda o: o.coords[0].y * 100 + o.coords[0].x , filter(lambda o: o.movable, objects)))
    print(result)
    

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    if env_test_run:
        main(open('00.txt')) 
    else: 
        main(open('01.txt'))
