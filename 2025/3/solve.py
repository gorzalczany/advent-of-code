"""AOC 3rd day."""

file = open('1.txt', 'r')
lines = file.readlines()

max_joltages_1 = []
max_joltages_2 = []

def find_largest_joltage(bank: list[int],  number_of_bateries_to_turn_on: int) -> int:
    selected_batteries = []
    start_index = 0
    while len(selected_batteries) < number_of_bateries_to_turn_on:
        missing_batteries_count = number_of_bateries_to_turn_on - len(selected_batteries)
        stop_index = len(bank)-missing_batteries_count+1
        search_space = bank[start_index:stop_index]
        battery = max(search_space)
        selected_batteries.append(battery)
        start_index = bank.index(battery, start_index) + 1
    max_joltage = int("".join(map(str, selected_batteries)))
    return max_joltage

for line_index, bank_string in enumerate(lines):

    bank = list(map(int, bank_string.strip()))

    #p1 - first solution
    # battery_1 = max(bank[:-1])
    # battery_2 = max(bank[bank.index(battery_1)+1:])
    # max_joltage = int(str(battery_1)+str(battery_2))
    # max_joltages_1.append(max_joltage)

    #p1
    max_joltages_1.append(find_largest_joltage(bank, 2))

    #p2 
    max_joltages_2.append(find_largest_joltage(bank, 12))

print(sum(max_joltages_1))
print(sum(max_joltages_2))