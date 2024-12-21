#!/usr/bin/python3
"""AOC 21th day."""

import sys
from queue import Queue
from collections import Counter, defaultdict
from functools import cache
import re

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)
    
    def scale(self, scalar):
        return Vec2D(self.x * scalar, self.y * scalar)   
    
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

class Keyboard:
    moves = {
        "^": Vec2D(0, -1),
        ">": Vec2D(1, 0),
        "v": Vec2D(0, 1),
        "<": Vec2D(-1, 0)
    }
    
    def __init__(self, key_pad, starting_position_symbol = "A"):
        self.key_pad = {k: Vec2D(*v) for k, v in key_pad.items()}
        self.starting_postion = self.key_pad[starting_position_symbol]
        
    @cache
    def getSequencesForCode(self, code: str) -> str:
        sequences = set()
        queue = Queue()
        queue.put((code, self.starting_postion, ""))
        
        while not queue.empty():
            code, last_known_position, sequence = queue.get()
            code, key = code[1:], code[0]
            key_sequences, moved = self._pressKey(key, last_known_position)
            last_known_position = self.key_pad[key] if moved else last_known_position
            for ks in set(key_sequences):
                s = sequence + ks
                if len(code) != 0:
                    queue.put((code, last_known_position, s))
                else:
                    sequences.add(s)
        shortest = min(sequences, key=len)           
        return [sequence for sequence in sequences if len(sequence)==len(shortest)]
    
    @cache
    def _pressKey(self, key: str, last_known_position) -> str:
        start = last_known_position
        target = self.key_pad[key]
         
        if start == target:
            return "A", False 	
          
        queue = Queue()
        queue.put((start, "", [start]))
        sequences = []
        
        while not queue.empty():
            node, sequence, path = queue.get()
            for move_symbol, vector in self.moves.items():
                next_node = node + vector
                if next_node == target:
                    sequences.append(sequence + move_symbol + "A")
                elif next_node in self.key_pad.values() and next_node not in path:
                    queue.put((next_node, sequence + move_symbol, path + [next_node]))
        
        shortest = min(sequences, key=len)           
        return [sequence for sequence in sequences if len(sequence)==len(shortest)], True
            

def main(input_file, isTest):
    lines =  input_file.read()
    codes = lines.splitlines()

    directional_key_pad = {
                        "^": (1,0),     "A": (2,0),
        "<": (0,1),     "v": (1,1),     ">": (2,1)
    }
    numeric_key_pad = {
        "7": (0,0),     "8": (1,0),     "9": (2,0),
        "4": (0,1),     "5": (1,1),     "6": (2,1),
        "1": (0,2),     "2": (1,2),     "3": (2,2),
                        "0": (1,3),     "A": (2,3),
    }
    
    complexities = {}
    for code in codes:
        print(code) 
        numeric_keyboard = Keyboard(key_pad=numeric_key_pad)
        sequences = set(numeric_keyboard.getSequencesForCode(code))
        # print(sequences)
        
        sequences2 = set()
        directional_keyboard = Keyboard(key_pad=directional_key_pad)
        for sequence in sequences:
            sequences2.update(directional_keyboard.getSequencesForCode(sequence))
            
        # shortest = min(sequences2, key=len)
        # sequences2 = set([sequence for sequence in sequences2 if len(sequence)<=len(shortest)])
        # print()
        # print(sequences2)
            
        sequences3 = set()
        directional_keyboard = Keyboard(key_pad=directional_key_pad)
        for sequence in sequences2:
            sequences3.update(directional_keyboard.getSequencesForCode(sequence))
        # print(sequences3)
        shortest = min(sequences3, key=len)
        sequences3 = set([sequence for sequence in sequences3 if len(sequence)<=len(shortest)])

        complexities[code] = min([len(sequence) * int(code[:-1]) for sequence in sequences3])
    print(complexities)        
    result = (sum(complexities.values()))
    print(result)
    assert result<281594 #p1
    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)