#!/usr/bin/python3
"""AOC 11th day."""
import sys
from collections import Counter

def splitStone(stone):
    half = len(stone)//2
    return stone[:half], str(int(stone[half:]))

def blinkAt(stone):
    newStones = []
    if len(stone) == 1 and int(stone) == 0: 
        newStones.append("1")
    elif len(stone) % 2 == 0:
        newStones = splitStone(stone)
    else:
         newStones.append(str(int(stone) * 2024))
    return newStones

def main(input_file):
    line =  input_file.read()
    stones = line.split()

    stones_counter = Counter(stones)
        
    for _ in range(0, 75):
        new_counter = Counter()
        for stone, count in stones_counter.items():
            newStones = blinkAt(stone)
            for newStone in newStones:
                new_counter[newStone] += count
        stones_counter = new_counter
        
    print(sum(stones_counter.values()))

if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'))