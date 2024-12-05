#!/usr/bin/python3
"""AOC 5th day."""

def check_page(instruction, page, rules):
   is_page_ok = True
   page_rules = filter(lambda rule: rule[0] == page, rules)
   where_page = instruction.index(page)
   for (page, other) in page_rules:
      if other in instruction and instruction.index(other) < where_page:
        is_page_ok = False
   return is_page_ok

def correct_instruction(instruction, rules):
    every_page_correct = True
    for page in instruction:
        every_page_correct &= check_page(instruction, page, rules)
    if every_page_correct:
       return

    for page in instruction:
        page_rules = filter(lambda rule: rule[0] == page, rules)
        where_page = instruction.index(page)
        for (page, other) in page_rules:
            if other in instruction and instruction.index(other) < where_page:
                where_other = instruction.index(other)
                instruction.pop(where_page)
                instruction.insert(where_other, page)
                break
    correct_instruction(instruction, rules)

def main():
    file = open('01.txt', 'r')
    lines = file.read().splitlines()

    rules = []
    instructions = []
    for idx, line in enumerate(lines):
        if "|" in line:
            line.split("|")
            key, value = map(int, line.split("|"))
            rules.append((key, value))
            continue
        if not line:
            continue
        instructions.append( [int(i) for i in line.split(',')])

    correct_middle_points = []
    corrected_middle_points = []
    for instruction in instructions:
        every_page_correct = True
        for page in instruction:
            every_page_correct &= check_page(instruction, page, rules)
        if every_page_correct:
           mid = int((len(instruction) - 1)/2)
           correct_middle_points.append(instruction[mid])
        else:
           correct_instruction(instruction, rules)
           mid = int((len(instruction) - 1)/2)
           corrected_middle_points.append(instruction[mid])

    print("part 1:", sum(correct_middle_points))
    print("part 2:", sum(corrected_middle_points))

main()