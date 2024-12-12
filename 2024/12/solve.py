#!/usr/bin/python3
"""AOC 12th day."""
import sys

adjacency_list = [ (0,1), (0,-1), (-1,0), (1,0)]
        
def floodfillRegion(matrix, start):
    floodingValue = matrix[start[1]][start[0]]
    fillQue = [start]
    flooded = set()
    
    oob = lambda x, y:  x < 0 or x >= len(matrix[0]) or y < 0 or y >= len(matrix)
    
    while(len(fillQue)>0):
        x, y = fillQue.pop(0)
        if oob(x, y):
            continue
        if matrix[y][x] == floodingValue and (x, y) not in flooded:
            flooded.add((x, y))
            for dx, dy in adjacency_list:
                fillQue.append((x + dx, y + dy))           
    return flooded

        
def getRegionPerimeter(region):
    count = 0
    for rx, ry in region:
        for dx, dy in adjacency_list:
            next = (rx + dx, ry + dy)
            if next not in region:
                count += 1
    return count
            
        
def getRegions(farm_map):
    regions = []
    checked_coords = set()
    for y, row in enumerate(farm_map):
        for x, plant_type in enumerate(row):
            if (x, y) in checked_coords: 
                continue
            area = floodfillRegion(farm_map, (x, y))
            regions.append((plant_type, area))
            checked_coords.update(area)
    return regions


def countSides(region):    
    # looking vector, moving vector
    def countWalls(lV, mV, region_adjacents, region):
        walls = 0
        checked = set()
        for current in region_adjacents:
            if current in checked:
                continue
            checked.add(current)
            lookingAt = (current[0]+lV[0], current[1]+(lV[1]))
            
            # check if there is a wall in direction we are "looking at"
            if lookingAt not in region: continue
            
            walls+=1
            # mark all adjacents to same wall as checked 
            # by "walking" next to the wall in both directions and "looking at" it
            for move_dx, move_dy in [(mV[0]*i, mV[1]*i) for i in [-1, 1] ]:
                next = current
                while True:
                    next = (next[0]-move_dx, next[1]-move_dy)
                    if next in region:
                        # if walked into another wall it means that current one ended
                        break
                    lookingAt = (next[0]+lV[0], next[1]+(lV[1]))
                    checked.add(next)
                    if lookingAt not in region:
                        # if wall "disapeared" that means it ended
                        break
                next = current
        return walls
    
    region_adjacents = set()
    for rx, ry in region:
        for dx, dy in adjacency_list:
            next = (rx+dx, ry+dy)
            if next not in region:
                region_adjacents.add(next)  
                
    walls = 0
    walls += countWalls((0,1), (1,0), region_adjacents, region) #look down, go horizontal
    walls += countWalls((0,-1), (1,0), region_adjacents, region) #look up, go horizontal
    walls += countWalls((-1,0), (0,1), region_adjacents, region) #look left, go vertical
    walls += countWalls((1,0), (0,1), region_adjacents, region) #look right, go vertical
    return walls


def main(input_file):
    lines =  input_file.read().splitlines()

    farm_map = []
    for coord_y, row in enumerate(lines):
        farm_map.append([])
        for coord_x, value in enumerate(row): 
            farm_map[coord_y].append(value)
            
    regions = getRegions(farm_map)
        
    price1 = 0        
    price2 = 0        
    for region in regions:
        (plant_type, region) = region
        area = len(region)
        
        # p1
        price1 += getRegionPerimeter(region) * area
        
        # pt 2
        price2 += countSides(region) * area
    
    print("pt1:", price1)
    print("pt2:", price2)
           
                
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))