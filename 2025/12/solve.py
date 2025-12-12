#!/usr/bin/python3
"""AOC 12th day."""
import sys

def fit_check(region, shapes, quantities):
    total_cells_needed = 0
    max_w = 0
    max_h = 0
    for shape_index, quantity in enumerate(quantities):
        if quantity == 0:
            continue
        shape = shapes[shape_index]
        cells = sum(row.count(1) for row in shape)
        total_cells_needed += cells * quantity
        shape_w = max(sum(1 for v in row if v == 1) for row in shape)
        shape_h = max(sum(1 for row in shape if row[c] == 1) for c in range(3))
        max_w = max(max_w, shape_w)
        max_h = max(max_h, shape_h)

    W, H = region
    if total_cells_needed > W * H:
        return False
    if max_w > W or max_h > H:
        return False
    return True


def main(input_file):
    lines =  input_file.read().splitlines()
    
    sections = [[]]
    for index, line in enumerate(lines):
        if line == '':
            sections.append([])
        else:
            sections[-1].append(line)
    shapes_strings = sections[:6]
    regions_strings = sections[6:][0]

    shapes = []
    for shape_index, shape in enumerate(shapes_strings):
        shapes.append([])
        for row in shape[1:]:
            shapes[shape_index].append(list(map(lambda x: 0 if x == '.' else 1, row)))

    count = 0
    for region in regions_strings:
        size, rest = region.split(': ')
        size = size.split('x')
        w, h = (int(size[0]), int(size[1]))
        region = (w, h)
        quantities = list(map(int, rest.split(' ')))
        can_fit = fit_check(region, shapes, quantities)
        if can_fit:
            count+=1
    print(count)
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('1.txt' if not env_test_run else '0.txt', 'r'))