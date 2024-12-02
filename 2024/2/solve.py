#!/usr/bin/python3
"""AOC 2nd day."""

file = open('01.txt', 'r')
lines = file.readlines()

def isSafe(report):
    increasing = True
    decreasing = True
    for i, level in enumerate(report[:-1]):
        d_safe = True
        next = report[i+1]
        if next < level:
            increasing = False
        if next > level:
            decreasing = False

        diff = abs(level - next)
        if diff > 3 or diff == 0:
            d_safe = False
        isSafe = d_safe and (increasing or decreasing)
        if not isSafe:
            return False
    return True


safe_count = 0
damped_safe_count = 0
for line_index, line in enumerate(lines):
    report = list(map(int, line.split()))

    if isSafe(report):
        safe_count += 1
        damped_safe_count +=1
        continue

    for i in range(len(report)):
        if isSafe(report[:i] + report[i + 1:]):
            damped_safe_count += 1
            break

print(safe_count)
print(damped_safe_count)
