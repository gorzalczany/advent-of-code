#!/usr/bin/python3
"""AOC 21th day."""

import sys
from queue import Queue
from collections import Counter
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
    vectors = {
        "^": Vec2D(0, -1),
        ">": Vec2D(1, 0),
        "v": Vec2D(0, 1),
        "<": Vec2D(-1, 0)
    }
    
    def __init__(self, key_pad, current_position_symbol = "A"):
        self.key_pad = {k: Vec2D(*v) for k, v in key_pad.items()}
        self.current_position = self.key_pad[current_position_symbol]
        
    def pressCode(self, code: str) -> str:
        sequence = ""
        
        for key in code:
            key_sequence, moved = self._pressKey(key)
            self.current_position = self.key_pad[key] if moved else self.current_position
            sequence += key_sequence
            
        return sequence
    
    def _pressKey(self, key: str) -> str:
        start = self.current_position
        target = self.key_pad[key]
         
        if start == target:
            return "A", False 	
          
        queue = Queue()
        queue.put((start, ""))
        visited = set()

        sequences = []
        
        while not queue.empty():
            node, sequence = queue.get()
            if node in visited: continue
            visited.add(node)
            for move_symbol, vector in self.vectors.items():
                next_node = node + vector
                if next_node == target:
                    sequences.append(sequence + move_symbol + "A")
                if next_node in self.key_pad.values() and next_node not in visited:
                    queue.put((next_node, sequence + move_symbol))
                    
        score = lambda x: len(x) - len(re.findall(r"(.)\1", x)) - len(re.findall(r"(.)\1+", x))
        return min(sequences, key=score), True
            

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
    
    complexities = []
    for code in codes:
        # print(code) 
        last_numeric_keyboard = Keyboard(key_pad=numeric_key_pad)
        sequence = last_numeric_keyboard.pressCode(code)
        # print(sequence)

        remote_in_radiation = Keyboard(key_pad=directional_key_pad)
        sequence = remote_in_radiation.pressCode(sequence)
        # print(sequence)

        remote_in_freezing = Keyboard(key_pad=directional_key_pad)
        sequence = remote_in_freezing.pressCode(sequence)
        # print(sequence)

        complexity = len(sequence) * int(code[:-1])
        complexities.append(complexity)
        print(f"{len(sequence)} * {int(code[:-1])}")
        
    print(sum(complexities))
        
    # // 295616 - to high
    
if __name__ == '__main__':
    env_test_run = sys.argv[-1] == '-t'
    main(open('01.txt' if not env_test_run else '00.txt', 'r'), env_test_run)