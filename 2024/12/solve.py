#!/usr/bin/python3
"""AOC 12th day."""
import sys
        
def floodfillRegion(matrix, start, symbol):
    i = 0
    fillQue = [start]
    queueLength = 1
    checked = set()
    
    maxRow = len(matrix)
    maxCol = len(matrix[0])
    
    while(i < queueLength):
        r = fillQue[i][1]
        c = fillQue[i][0]
        i += 1
        
        if r < 0 or r >= maxRow or c < 0 or c >= maxCol:
            continue
        
        if matrix[r][c] == symbol and (c, r) not in checked:
            checked.add((c, r))           
            fillQue.append((c, r + 1))
            fillQue.append((c + 1, r))
            fillQue.append((c, r -1))
            fillQue.append((c -1, r))
            queueLength += 4
    return checked

        
def getRegionPerimeter(region):
    vectors = [ (0,1), (0,-1), (-1,0), (1,0)]
    count = 0
    for r in region:
        for v in vectors:
            next = (r[0]+v[0], r[1]+v[1])
            if next not in region:
                count += 1
    return count
            
        
def getRegions(farm_map):
    regions = []
    mapped_coords = set()
    for coord_y, row in enumerate(farm_map):
        for coord_x, plant_type in enumerate(row):
            if (coord_x, coord_y) in mapped_coords: 
                continue
            area = floodfillRegion(farm_map, (coord_x, coord_y), plant_type)
            regions.append((plant_type, area))
            mapped_coords.update(area)
    return regions


def countSides(region):
    vectors = [(0,1), (0,-1), (-1,0), (1,0)]
    regionOutsides = set()
    for p in region:
        for v in vectors:
            next = (p[0]+v[0], p[1]+v[1])
            if next not in region:
                regionOutsides.add(next)  
    
    # looking vector, moving vector
    def countWalls(lV, mV, regionOutsides, region):
        walls = 0
        checked = set()
        for current in regionOutsides:
            if current in checked:
                continue
            checked.add(current)
            lookingAt = (current[0]+lV[0], current[1]+(lV[1]))
            if lookingAt not in region:
                continue
            
            walls+=1
            
            next = current
            while True:
                next = (next[0]-(mV[0]), next[1]-(mV[1]))
                if next in region:
                    break
                lookingAt = (next[0]+lV[0], next[1]+(lV[1]))
                checked.add(next)
                if lookingAt not in region:
                    break
            next = current
            while True:
                next = (next[0]+(mV[0]), next[1]+(mV[1]))
                if next in region:
                    break
                lookingAt = (next[0]+lV[0], next[1]+(lV[1]))
                checked.add(next)
                if lookingAt not in region:
                    break
        return walls
                
    walls = 0
    walls += countWalls((0,1), (1,0), regionOutsides, region) #look down, go horizontal
    walls += countWalls((0,-1), (1,0), regionOutsides, region) #look up, go horizontal
    walls += countWalls((-1,0), (0,1), regionOutsides, region) #look left, go vertical
    walls += countWalls((1,0), (0,1), regionOutsides, region) #look right, go vertical
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