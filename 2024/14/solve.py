#!/usr/bin/python3
"""AOC 13th day."""
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import deque, Counter
from math import log

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)
    
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

class Size:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def __iter__(self):
        yield self.w
        yield self.h

class Robot:
    def __init__(self, p: Vec2D, v: Vec2D):
        self.p = p
        self.v = v
    def getNextPos(self):
        return self.p.copy() + self.v
    def move(self):
        self.p += self.v    

def move(robot: Robot, rl, cl):
    oobX = lambda p, rl:  p.x < 0 or p.x >= rl
    oobY = lambda p, cl:  p.y < 0 or p.y >= cl
    
    next_p = robot.getNextPos()
    isOobX = oobX(next_p, rl)
    isOobY = oobY(next_p, cl)
    # all that code below is overcomplicated
    # just use ` nx = (px + vx) % w` next time
    if not (isOobX or isOobY):
        robot.move(); return
    if isOobY: 
        if next_p.y < 0: robot.p.y = cl + next_p.y
        else:  robot.p.y = next_p.y - cl
    else:
        robot.p.y += robot.v.y
    if isOobX: 
        if next_p.x < 0: robot.p.x = rl + next_p.x
        else: robot.p.x = next_p.x - rl
    else:
        robot.p.x += robot.v.x


def flatten(array):
    return [x for xs in array for x in xs]
        
        
def getArrayQuadrants(a):
    h = len(a)
    w = len(a[1])
    def c_div(n, d): return -(n // -d)
    def f_div(n, d): return n // d
    
    top_left =  flatten([a[i][:f_div(w,2)] for i in range(f_div(h,2))])
    top_right = flatten([a[i][c_div(w,2):] for i in range(f_div(h,2))])
    bot_left =  flatten([a[i][:f_div(w,2)] for i in range(c_div(h,2), h)])
    bot_right = flatten([a[i][c_div(w,2):] for i in range(c_div(h,2), h)])
    return [top_left, top_right, bot_left, bot_right]


def getSafetyFactor(robots, rl, cl):
    allPositions = []
    for y in range(cl):
        allPositions.append([])
        for x in range(rl):
            allPositions[y].append(Vec2D(x, y))
    
    quadrants = getArrayQuadrants(allPositions)
    
    factor = 1
    for quadrant in quadrants:
        count = 0
        for robot in robots:
            if robot.p in quadrant:
                count += 1
        factor *= count
            
    return factor


def printRobotsInArray(robots, row_l, col_l):
    positions = [robot.p for robot in robots]
    for y in range(col_l):
        string = ""
        for x in range(row_l):
            if Vec2D(x, y) in positions:
                string += "■"
            else: string += "▢"
        print(string)
        
        
def plotRobots(robots, row_l, col_l, name: str):
    array = np.zeros((col_l, row_l))
    for robot in robots:
        array[robot.p.y][robot.p.x] = 1
    plt.imshow(array, cmap='hot')
    plt.savefig(f'plot/{name}.png')


def main(input_file, a_size):
    lines = input_file.read().splitlines()
    robots = []
    for line in lines:
        p, v = line.split()
        p = Vec2D(*map(int, p.replace(p[:p.index("=")+1], '').split(",")))
        v = Vec2D(*map(int, v.replace(v[:v.index("=")+1], '').split(",")))
        robots.append(Robot(p, v))
    
    entropies = deque([], 10)
    for i in range(1, a_size.w*a_size.h):
        for robot in robots:
            move(robot, *a_size)
        
        if i == 100:
            factor = getSafetyFactor(robots, *a_size)
            print(factor) 
           
        # implementation of https://stats.stackexchange.com/a/17147    
        ocurrences = [0] * a_size.h * a_size.w
        for robot in robots: 
            ocurrences[a_size.w * robot.p.x + robot.p.y] += 1 # 2D array represented as 1D
        distribution = Counter(ocurrences)
        entropy = sum([-1 * item/len(distribution) * log(item/len(distribution), 2) for item in distribution.values()])
        
        # store 10 lowest entropies because why not
        if len(entropies) == 0 or entropy < entropies[0][1]:
            entropies.appendleft((i, entropy))
            # plot board every time we find lower distribution. Just for fun.
            plotRobots(robots, a_size.w, a_size.h, i)
        
        # FUN FACT:
        # image is represented with exacly one robot on one position
        # otherwise there is always at least one position with two robots on it
        #
        # robot_positions = [robot.p for robot in robots]
        # if len(set(robot_positions)) == len(robot_positions):
        #     print("lol", i)
    print(entropies)

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    if env_test_run:
        main(open('00.txt'), Size(11, 7)) 
    else: 
        main(open('01.txt'), Size(101, 103))
