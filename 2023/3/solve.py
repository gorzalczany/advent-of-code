"""AOC 3rd day."""

xyoffsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

f = open('./3/1.txt', 'r')
array2D = f.read().splitlines()
f.close()

def isAdjacent(a, b):
    isAnyAdjacent=False
    for offset in xyoffsets:
        try:
            cX = a+offset[0]
            cY = b+offset[1]
            toCheck = array2D[cX][cY]
            if cX < 0 or cY < 0 or cX > len(array2D) or cY > len(array2D[a]):
                continue
            if not toCheck.isnumeric() and toCheck != '.':
                isAnyAdjacent = True
                break
        except IndexError:
            continue
    return isAnyAdjacent

def isAdjacentToGear(a, b):
    gearPosition=(-1, -1)
    for offset in xyoffsets:
        try:
            cX = a+offset[0]
            cY = b+offset[1]
            toCheck = array2D[cX][cY]
            if cX < 0 or cY < 0 or cX > len(array2D) or cY > len(array2D[a]):
                continue
            if toCheck == "*":
                gearPosition = (cX, cY)
                break
        except IndexError:
            continue
    return gearPosition
        
def main():
    temp=""
    adjacent=False
    gearAdjacents = []

    adjacentToGear=False
    gearPosition=(-1, -1)
    answer = 0
    for ix, x in enumerate(array2D):
        for iy, y in enumerate(x):
            if y.isnumeric():
                temp+=y
                adjacent = adjacent or isAdjacent(ix,iy)
                checkedGearPosition = isAdjacentToGear(ix,iy)
                adjacentToGear = adjacentToGear or checkedGearPosition != (-1, -1)
                if checkedGearPosition != (-1, -1):
                    gearPosition = checkedGearPosition
            if not y.isnumeric() and adjacent:
                adjacent = False
                if len(temp) > 0:
                    answer += int(temp)
            if not y.isnumeric() and adjacentToGear:
                adjacentToGear = False
                if len(temp) > 0:
                    gearAdjacents.append((int(temp), gearPosition))
            if not y.isnumeric():
                temp = ""

    print(f"sum = {answer}")

    gearRatio = 0
    checkedGears=[]
    for gearAdjacent in gearAdjacents:
        if gearAdjacent[1] in checkedGears:
            continue
        checkedGears.append(gearAdjacent[1])
        sameGears = list(filter(lambda x: x[1] == gearAdjacent[1], gearAdjacents))
        if len(sameGears) == 2:
            gearRatio += sameGears[0][0]*sameGears[1][0]

    print(f"gear ratio = {gearRatio}")

if __name__ == '__main__':
    main()
