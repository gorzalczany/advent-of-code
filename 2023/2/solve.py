"""AOC 2nd day."""

file = open('./2/1.txt', 'r')
lines = file.readlines()

possibleIds = [0]*len(lines)
powerSum = 0

def only_numerics(seq):
    seq_type= type(seq)
    return int(seq_type().join(filter(seq_type.isdigit, seq)))

for index, line in enumerate(lines):
    game = line.split(':')
    gameId = only_numerics(game[0])
    gameSets = game[1].split(';')

    max_red=0
    max_green=0
    max_blue=0

    for set in gameSets:
        colors = set.split(',')
        for color in colors:
            if 'red' in color:
                max_red  = max(only_numerics(color), max_red)
            if 'green' in color:
                max_green  = max(only_numerics(color), max_green)
            if 'blue' in color:
                max_blue  = max(only_numerics(color), max_blue)
        power = max_red * max_green * max_blue

    powerSum += power

    if max_red > 12 or max_green > 13 or max_blue > 14:
        continue
    else:
        possibleIds[index] = gameId

print(f"sum of possible ids = {sum(possibleIds)}, powerSum = {powerSum}")