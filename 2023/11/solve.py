"""AOC 10th day."""
import itertools
  
def getGalaxies(image):
  galaxies = []
  for iy, row in enumerate(image):
    for ix, e in enumerate(row):
        if e == "#":
          galaxies.append((ix, iy))
  return galaxies

def get_column(matrix, i):
    return [row[i] for row in matrix]

def getEmpties(image):
  empty_columns_x = []
  empty_rows_y = []
  for iy, row in enumerate(image):
    if all(e == "." for e in row):
        empty_rows_y.append(iy)

  for ix in range(0, len(image[0]),1 ):
    column = get_column(image, ix)
    if all(e == "." for e in column):
      empty_columns_x.append(ix)

  return(empty_columns_x, empty_rows_y)

def steps_between(p1, p2, empties, t):
  empty_y_count = 0
  empty_x_count = 0
  if p1[1] > p2[1]:
     for y in range(p2[1], p1[1], 1):
        if y in empties[1]:
           empty_y_count += 1
  elif p1[1] < p2[1]:
      for y in range(p1[1], p2[1], 1):
        if y in empties[1]:
           empty_y_count += 1

  if p1[0] > p2[0]:
     for y in range(p2[0], p1[0], 1):
        if y in empties[0]:
           empty_x_count += 1
  elif p1[0] < p2[0]:
      for y in range(p1[0], p2[0], 1):
        if y in empties[0]:
           empty_x_count += 1

  return abs(p1[0] - p2[0])+(t*empty_x_count)-empty_x_count + abs(p1[1] - p2[1])+(t*empty_y_count)-empty_y_count

def main():
  image = []
  f = open('./11/input.txt', 'r')
  for idx, row in enumerate(f.read().splitlines()):
    image.append([])
    for value in row:
        image[idx].append(value)
  f.close()

  galaxies = getGalaxies(image)  
  pairs = list(itertools.combinations(galaxies, 2))
  empties = getEmpties(image)

  #part 1
  distances = []
  for p1, p2 in pairs:
    distances.append(steps_between(p1, p2, empties, 2))
  print(f"part1: {sum(distances)}")

  #part 2
  distances = []
  for p1, p2 in pairs:
    distances.append(steps_between(p1, p2, empties, 1_000_000))
  print(f"part2: {sum(distances)}")

if __name__ == '__main__':
    main()