"""AOC 1st day."""

file = open('./1/1.txt', 'r')
lines = file.readlines()

digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
count = 0

for line_index, line in enumerate(lines):
    first_coord = ""
    last_coord = ""

    lowest_index = len(line)
    hights_index = 0

    for digit_index, digit_string in enumerate(digits):
        found = line.find(digit_string)
        if found >= 0:
            if found < lowest_index:
                lowest_index = found
                first_coord = f"{digit_index + 1}"
        found_from_end = line.rfind(digit_string)
        if found_from_end >= 0:
            if found_from_end > hights_index:
                hights_index = found_from_end
                last_coord = f"{digit_index + 1}"
    for index, char in enumerate(line):
        if char.isdigit() and index <= lowest_index:
            first_coord = char
            break
    for index, char in enumerate(line[::-1]):
        true_index = len(line) - index
        if char.isdigit() and true_index > hights_index:
            last_coord = char
            break
    coord_string = first_coord + last_coord
    coord_value = int(coord_string)
    print(f"line {line_index+1} value is {coord_value}")

    count += coord_value

print(count)