#!/usr/bin/python3
"""AOC 21th day."""

import sys
from functools import cache

class Keyboard:
    Vector = tuple[int, int]
    KeyPad = dict[str: Vector]

    moves = {
        "^": (0, -1),"v": (0, 1),
        "<": (-1, 0),">": (1, 0),
    }

    d_pad: KeyPad = {
                        "^": (1,0),     "A": (2,0),
        "<": (0,1),     "v": (1,1),     ">": (2,1)
    }

    num_pad: KeyPad = {
        "7": (0,0),     "8": (1,0),     "9": (2,0),
        "4": (0,1),     "5": (1,1),     "6": (2,1),
        "1": (0,2),     "2": (1,2),     "3": (2,2),
                        "0": (1,3),     "A": (2,3),
    }


def getSequencesToPressKey(prevKey: str, nextKey: str, key_pad:Keyboard.KeyPad) -> list[str]:
    if prevKey == nextKey:
        return ["A"]

    start, target = key_pad[prevKey], key_pad[nextKey]
    queue = [(start, "", [start])]
    sequences = []

    while len(queue) > 0:
        node, sequence, path = queue.pop(0)
        for move_symbol, (dx, dy) in Keyboard.moves.items():
            next_node = (node[0] + dx, node[1] + dy)
            seq_with_move = sequence + move_symbol
            if next_node == target:
                if not sequences or len(sequences[0]) == len(seq_with_move):
                    sequences.append(seq_with_move)
            elif next_node in key_pad.values() and next_node not in path:
                queue.append((next_node, seq_with_move, path + [next_node]))
    return [sequence + "A" for sequence in sequences]


@cache
def getLengthOfCodePressingSequences(code: str, depth: int) -> int:
    if depth == 1:
        return len(code)

    key_pad = Keyboard.num_pad if any(map(str.isdigit, code)) else Keyboard.d_pad

    length = 0
    for prev_key, next_key in zip("A" + code, code):
        shortest_paths = getSequencesToPressKey(prev_key, next_key, key_pad)
        length += min( getLengthOfCodePressingSequences(sp, depth - 1) for sp in shortest_paths)
    return length


def get_code_complexity(code, middle_robbots):
    length_of_pressing = getLengthOfCodePressingSequences(code, 1 + middle_robbots + 1)
    return length_of_pressing * int(code[:-1])


def main(input_file, isTest):
    lines = input_file.read()
    codes = lines.splitlines()
    
    print("pt1:", sum(get_code_complexity(code, middle_robbots=2) for code in codes))
    print("pt2:", sum(get_code_complexity(code, middle_robbots=25) for code in codes))


if __name__ == "__main__":
    env_test_run = sys.argv[-1] == "-t"
    main(open("01.txt" if not env_test_run else "00.txt", "r"), env_test_run)
