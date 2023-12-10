"""AOC 9th day."""
from itertools import pairwise
from math import ceil

def parseInput(file):
  file = open(file)
  lines = file.read().splitlines()
  dataset = []
  for line in lines:
    dataset.append([int(x) for x in line.split(' ')])
  file.close()
  return dataset

def all_zeroes(lst):
  return not lst or lst.count(0) == len(lst)

def predictFrom(seq):
  prediction = 0
  while not all_zeroes(seq):
      prediction += seq[-1]
      seq = [b - a for a, b in pairwise(seq)]
  return prediction

def printDifferenceTable(seq):
  step = 0
  str_len = len(str(max(seq)))
  while not all_zeroes(seq):
    print(" "*(ceil(step*str_len/2)+step), *[str(x).center(ceil(str_len/2)*2) for x in seq])
    step +=1
    seq = [b - a for a, b in pairwise(seq)]

def part1(dataset):
  predictions = []
  for history in dataset:
    predictions.append(predictFrom(history))
  return sum(predictions)

def part2(dataset):
  predictions = []
  for history in dataset:
    predictions.append(predictFrom(history[::-1]))
  return sum(predictions)

dataset = parseInput('./9/0.txt')
# print(part1(dataset))
# print(part2(dataset))
history = dataset[2]
printDifferenceTable(history)
history.append(predictFrom(history))
printDifferenceTable(history)
