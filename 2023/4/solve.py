"""AOC 4th day."""
import re

file = open('./4/1.txt', 'r')
lines = file.readlines()

class Scratchcard:
    id = 0
    winingNumbers = []
    myNumbers = []

scratchcards = []

for line in lines:
    game = line.split(':')
    cardSets = game[1].split('|')
    scratchcard = Scratchcard()
    scratchcard.id = int(re.findall(r"\d+", game[0])[0])
    scratchcard.winingNumbers = list(map(lambda x: int(x), re.findall(r"\d+", cardSets[0])))
    scratchcard.myNumbers = list(map(lambda x: int(x), re.findall(r"\d+", cardSets[1])))
    scratchcards.append(scratchcard)

# part one
allPoints = 0
for card in scratchcards:
    matchingNumbers = list(filter(lambda x: x in card.winingNumbers, card.myNumbers))
    points = 0
    if len(matchingNumbers) == 1:
        points = 1
    if len(matchingNumbers) >= 2:
        points = 2**(len(matchingNumbers)-1)
    allPoints += points
print(f"sum of points: {allPoints}")

# part two
copies = []
for card in scratchcards:
    matchingNumbers = list(filter(lambda x: x in card.winingNumbers, card.myNumbers))
    copiesOfCurrent = list(filter(lambda x: x.id == card.id, copies))

    # original won
    newCopiesFromOriginal = scratchcards[card.id : card.id + len(matchingNumbers) : 1]
    copies += newCopiesFromOriginal

    #copies won
    for copy in copiesOfCurrent:
        matchingNumbers = list(filter(lambda x: x in copy.winingNumbers, copy.myNumbers))
        newCopiesFromCopies = scratchcards[copy.id : copy.id + len(matchingNumbers) : 1]
        copies += newCopiesFromCopies

print(f"all copies count: {len(copies) + len(scratchcards)}")
