#!/usr/bin/python3
"""AOC 9th day."""
import sys
import itertools


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def get_area(p1: Point, p2: Point):
    min_x = min(p1.x, p2.x)
    max_x = max(p1.x, p2.x)
    min_y = min(p1.y, p2.y)
    max_y = max(p1.y, p2.y)
    return (max_x - min_x + 1) * (max_y - min_y + 1)


def solve1(corners):
    combinations = itertools.combinations(corners, 2)
    tiles = []
    for combo in combinations:
        c1, c2 = combo
        area = get_area(c1, c2)
        tiles.append((c1, c2, area))
    tiles.sort(key=lambda x: x[2])
    largest_tile = tiles[-1]
    print("p1: ", largest_tile[2])


def solve2(corners, loop_lines):
    combinations = itertools.combinations(corners, 2)
    tiles = []
    for combo in combinations:
        c1, c2 = combo
        area = get_area(c1, c2)
        tiles.append((c1, c2, area))
    
    good_tiles = []
    for rect in tiles:
        if is_rectangle_any_good(rect, loop_lines):
            good_tiles.append(rect)
    good_tiles.sort(key=lambda x: x[2])
    largest_good_tile = good_tiles[-1]
    print("p2: ", largest_good_tile[2])


def is_rectangle_any_good(tile, loop_lines):
    c1, c2, area = tile
    min_x = min(c1.x+1, c2.x+1)
    max_x = max(c1.x-1, c2.x-1)
    min_y = min(c1.y+1, c2.y+1)
    max_y = max(c1.y-1, c2.y-1)
    rect_lines = connect_points(
        [ Point(min_x, min_y), Point(min_x, max_y), Point(max_x, max_y), Point(max_x, min_y) ]
    )

    for line in rect_lines:
        for loop_line in loop_lines:
            if intersect(line, loop_line):
                return False
    return True


def ccw(A: Point, B: Point, C: Point):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


def intersect(line1: Line, line2: Line):
    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    A, B, C, D = line1.p1, line1.p2, line2.p1, line2.p2
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def connect_points(points: list[Point]):
    lines = []
    for i, p1 in enumerate(points):
        p2 = points[(i + 1) % len(points)]
        lines.append(line_between_points(p1, p2))
    return (lines)


def line_between_points(p1: Point, p2: Point):
    if p1.x == p2.x:
        x = p1.x
        return Line(Point(x, min(p1.y, p2.y)), Point(x, max(p1.y, p2.y)))
    elif p1.y == p2.y:
        y = p1.y
        return Line(Point(min(p1.x, p2.x), y), Point(max(p1.x, p2.x), y))


def main(input_file, limit):
    lines =  input_file.read().splitlines()

    corners = []
    for index, line in enumerate(lines):
        x, y = map(int, line.split(','))
        corners.append(Point(x, y))

    loop_lines = connect_points(corners)
    solve1(corners)
    solve2(corners, loop_lines)
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'), 1000 if not env_test_run else 10)