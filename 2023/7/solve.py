"""AOC 7th day."""

import sys
import re
from collections import defaultdict
from functools import cmp_to_key
from functools import reduce

file = open('./7/1.txt')
lines = file.read().splitlines()

part1_strength = { "A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2 }
part2_strength = { "A": 14, "K": 13, "Q": 12, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "J": 1 }
def strongerHand(strengths_rank, l, r):
  if l[0] != r[0]:
    return -1 if l[0] < r[0] else 1
  else:
    cards = zip(l[1],r[1])
    for pair in cards:
      l_strength = strengths_rank[pair[0]]
      r_strength = strengths_rank[pair[1]]
      if l_strength == r_strength:
        continue
      return -1 if l_strength < r_strength else 1
    
def strongerHandPart1(l, r):
  return strongerHand(part1_strength, l, r)
def strongerHandPart2(l, r):
  return strongerHand(part2_strength, l, r)

def applyPart2rules(hand):
  type = hand[0]
  cards = hand[1]
  if "J" in cards:
    if type in {6, 5}:
      type = 7
    elif type == 4:
      type = 6
    elif type == 3 and cards.count('J') == 2:
      type = 6
    elif type == 3:
      type = 5
    elif type == 2:
      type = 4
    elif type == 1:
      type = 2
  return (type, cards, hand[2])

rank = []
for idx, line in enumerate(lines, 1):
  cards = line.split()[0]
  bid = int(line.split()[-1])
  labels = defaultdict(str)

  for c in cards:
    if c in labels:
      labels[c] += 1
    else:
      labels[c] = 1

  type = 0
  max_labels = max(labels.values())
  if max_labels == 5:
    type = 7 # five of a kind
  elif max_labels == 4:
    type = 6 # four of a kind
  elif max_labels == 3 and len(labels.keys()) == 2:
    type = 5 # full house
  elif max_labels == 3:
    type = 4 # Three of a kind 
  elif max_labels == 2 and len(list(filter(lambda x: x == 2, labels.values()))) == 2:
    type = 3 # two pairs
  elif max_labels == 2 and len(list(filter(lambda x: x == 2, labels.values()))) == 1:
    type = 2 # one pair
  else:
    type = 1 # High card
  rank.append((type, cards, bid))

rank.sort(key=cmp_to_key(strongerHandPart1))
winnings = reduce(lambda a, e: a + e[0]*e[1][2], enumerate(rank, 1), 0)
print(winnings)

rank2 = list(map(applyPart2rules, rank))
rank2.sort(key=cmp_to_key(strongerHandPart2))
winnings = reduce(lambda a, e: a + e[0]*e[1][2], enumerate(rank2, 1), 0)
print(winnings)

