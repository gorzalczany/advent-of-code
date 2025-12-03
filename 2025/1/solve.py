"""AOC 1st day."""

file = open('1.txt', 'r')
lines = file.readlines()

start = 50
sum_1 = 0
sum_2 = 0
for line_index, line in enumerate(lines):
    direction, value = line[0], int(line[1:])

    if direction == 'L':
        start -= value
    else:
        start += value

    full_rotations = abs(start // 100)
    sum_2 += full_rotations
    
    start = start % 100
    if start == 0:
        sum_1 += 1

print(sum_1)
print(sum_2)