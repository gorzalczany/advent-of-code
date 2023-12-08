"""AOC 8th day."""

import math
from collections import defaultdict

def parseInput(file):
  file = open(file)
  lines = file.read().splitlines()
  instructions = lines[0]
  nodes = defaultdict(str)
  for line in lines[2:]:
    node = line.split(' = ')[0]
    coords = line.split(' = ')[1][1:-1:].split(', ')
    nodes[node] = {'L': coords[0], 'R': coords[-1]}
  file.close()
  return nodes, instructions

def part1(nodes, instructions):
  found_zzz = False
  current_node = 'AAA'
  steps = 0
  while not found_zzz:
    for instruction in instructions:
      steps +=1
      next_node = nodes[current_node][instruction]
      current_node = next_node
      if current_node == "ZZZ":
        found_zzz = True
        break
  print(steps)

def part2(nodes, instructions):
  current_nodes = list(filter(lambda x: x[-1] == 'A', nodes.keys()))
  steps_arr  = [0]*len(current_nodes)
  step = 0
  all_on_z = False
  while not all_on_z:
    for instruction in instructions:
      step +=1
      for idx, current_node in enumerate(current_nodes):
        next_node = nodes[current_node][instruction]
        current_nodes[idx] = next_node
        if next_node[-1] == 'Z' and steps_arr[idx] == 0:
          steps_arr[idx] = step
      if all(x > 0 for x in steps_arr):
        all_on_z = True
        break
  print(math.lcm(*steps_arr))

input = parseInput('./8/1.txt')
part1(*input)
part2(*input)
