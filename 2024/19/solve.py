#!/usr/bin/python3
"""AOC 19th day."""
import sys

def main(input_file, isTest):
    input = input_file.read()
    
    patterns, designs = input.split('\n\n')
    patterns = patterns.split(", ")
    designs = designs.splitlines()    
    
    checkedDesign = {}
    
    def check(design):
        if design in checkedDesign:
            return checkedDesign[design]
        
        if len(design) == 0:
            return 1
        
        total = 0
        for key in patterns:
            if design.startswith(key): 
                total += check(design[len(key):])
        checkedDesign[design] = total
        return total
    
    pt1 = 0
    pt2 = 0
    for design in designs:
            options = check(design)
            pt1 += 1 if options > 0 else 0
            pt2 += check(design)
            
    print(pt1)
    print(pt2)

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)