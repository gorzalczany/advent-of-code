#!/usr/bin/python3
"""AOC 10th day."""
import sys

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

def coordsAround(coord, topographic_map):
    points = [
        Coordinate(coord.x-1, coord.y),
        Coordinate(coord.x+1, coord.y),
        Coordinate(coord.x, coord.y-1),
        Coordinate(coord.x, coord.y+1)
    ]
    return [point for point in points if not oob(point, topographic_map)]

def findNext(coord, topographic_map):
    startValue = topographic_map[coord.y][coord.x]
    lookAround = coordsAround(coord, topographic_map)
    filtered = [point for point in lookAround if topographic_map[point.y][point.x] == startValue + 1]
    return filtered

def getVal(coord, topographic_map):
    return topographic_map[coord.y][coord.x]

def countTrailsForPt2(start, topographic_map):
    count = 0
    nexts = findNext(start, topographic_map)
    for next in nexts:
        if getVal(next, topographic_map) == 9:
            count += 1
            continue
        count += countTrailsForPt2(next, topographic_map)

    return count

def scorePt2(trailhead, topographic_map):
    score = countTrailsForPt2(trailhead, topographic_map)
    return score

def scorePt1(trailhead, topographic_map):
    nine_coords = set()
    toScore = findNext(trailhead, topographic_map)
    while len(toScore)>0:
        next = toScore.pop()
        if getVal(next, topographic_map) == 9:
            nine_coords.add(next)
        toScore += findNext(next, topographic_map)
    return len(nine_coords)


def main(input_file):
    lines =  input_file.read().splitlines()

    topographic_map = []
    trailheads = []
    for coord_y, row in enumerate(lines):
        topographic_map.append([])
        for coord_x, value in enumerate(row): 
            topographic_map[coord_y].append(int(value))
            if value == "0":
                trailheads.append(Coordinate(coord_x, coord_y))

    scores = []
    for trailhead in trailheads:
        scores.append(scorePt1(trailhead, topographic_map))
    print(sum(scores))

    scores = []
    for trailhead in trailheads:
        scores.append(scorePt2(trailhead, topographic_map))
    print(sum(scores))

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))