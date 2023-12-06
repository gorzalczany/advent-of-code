"""AOC 6th day."""

import sys
import re

def chances(races):
  answer = 0
  for race in races:
    chances = 0
    time = race[0]
    record = race[1]
    for v in range(1,time,1):
      t = time - v # remaining time
      D=v*t
      if D > record:
        chances += 1
    answer = chances if answer == 0 else answer * chances
  return answer

file = open('./6/1.txt')
lines = file.read().splitlines()

def part1():
  times =  [int(x) for x in lines[0].split(':')[-1].split()]
  distances = [int(x) for x in lines[1].split(':')[-1].split()]
  races = zip(times,distances)
  print(chances(races))

def part2():
  times =  list(map(int,re.findall(r'(\d+)', lines[0].replace(" ", ""))))
  distances = list(map(int,re.findall(r'(\d+)', lines[1].replace(" ", ""))))
  races = zip(times,distances)
  print(chances(races))

part1()
part2()