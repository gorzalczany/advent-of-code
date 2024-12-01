#!/usr/bin/python3
"""AOC 1st day."""

file = open('01.txt', 'r')
lines = file.readlines()

left = []
right = []

for line_index, line in enumerate(lines):
    l, r = line.split()
    left.append(int(l))
    right.append(int(r))

left.sort()
right.sort()

total_distance = 0
total_similarity = 0
for i, l in enumerate(left):
    r = right[i]

    # part 1
    distance = abs(l - r)
    total_distance += distance

    # part 2
    similarity = l * right.count(l)
    total_similarity += similarity 

print(total_distance)
print(total_similarity)