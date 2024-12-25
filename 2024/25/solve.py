#!/usr/bin/python3
"""AOC 23th day."""
import sys
from collections import Counter


def isLock(schematics):
    isTopRowFilled = schematics[0] ==  ["#"] * len(schematics[0])
    isBottomEmpty =  schematics[len(schematics)-1] ==  ["."] * len(schematics[0])
    return isTopRowFilled and isBottomEmpty

def isKey(schematics):
    isTopRowEmpty = schematics[0] ==  ["."] * len(schematics[0])
    isBottomFilled =  schematics[len(schematics)-1] ==  ["#"] * len(schematics[0])
    return isTopRowEmpty and isBottomFilled
    

def main(input_file, isTest):    
    schematics_collection =  input_file.read().split("\n\n")

    locks_prints = []
    keys_prints = []
    
    for schematics in schematics_collection:
        schema = []
        col_heights = Counter()
        for vec_y, row in enumerate(schematics.splitlines()):
            schema.append(["."]*len(row))
            for vec_x, value in enumerate(row):
                if value == "#":
                    col_heights[vec_x] += 1
                    schema[vec_y][vec_x] = "#"
        if isLock(schema):
            locks_prints.append((schema, col_heights))
        elif isKey(schema): 
            keys_prints.append((schema, col_heights))
            
    pairs_count = 0        
    for lock_print, l_heights in locks_prints:
        lock_size = len(lock_print)
        for key_print, k_heights in keys_prints:
            overlaps = []
            for i, kh in k_heights.items():
                overlaps.append(l_heights[i] +  kh > lock_size)
            if not any(overlaps):
                pairs_count += 1
                print(f"Lock {l_heights.values()} and key {k_heights.values()}: all columns fit")
            else:
                print(f"Lock {l_heights.values()} and key {k_heights.values()}: overlaps")
                
                
    print(pairs_count)
                    


    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)