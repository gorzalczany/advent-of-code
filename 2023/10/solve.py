"""AOC 10th day."""
import numpy as np
from matplotlib import path

steps = {
  "↑": (0, -1),
  "←": (-1, 0),
  "→": (1, 0), 
  "↓": (0, 1)
}

tiles = {
  "|": "║",
  "-": "═",
  "L": "╚",
  "J": "╝",
  "7": "╗",
  "F": "╔",
  ".": " ",#"░",
  "S": "S"
}

connections = {
  "|": {"↑": ["7", "F", "|"], "↓": ["J", "L", "|"]},
  "-": {"←": ["-", "L", "F"], "→": ["-", "J", "7"]},
  "L": {"↑": ["7", "F", "|"], "→": ["-", "J", "7"]},
  "J": {"↑": ["7", "F", "|"], "←": ["-", "L", "F"]},
  "7": {"↓": ["J", "L", "|"], "←": ["-", "L", "F"]},
  "F": {"↓": ["J", "L", "|"], "→": ["-", "J", "7"]},
}

array2D = []
f = open('./10/1.txt', 'r')
for idx, row in enumerate(f.read().splitlines()):
   array2D.append([])
   for value in row:
      array2D[idx].append(value)
f.close()

def isConnected(x, y):
    if array2D[y][x] == "S":
       return True
    elif array2D[y][x] == ".":
       return False
    else:
      connections_count = 0
      tile = array2D[y][x]
      for step_direction, step_coords in steps.items():
        try:
          cX = x+step_coords[0]
          cY = y+step_coords[1]
          toCheck = array2D[cY][cX]
          if cX < 0 or cY < 0 or cY > len(array2D) or cX > len(array2D[y]):
              continue
          pipe_directions = connections[tile]
          available_connection = pipe_directions.get(step_direction, [])
          if toCheck in available_connection or toCheck == "S":
              connections_count += 1
        except IndexError:
            continue
      return True if connections_count >= 2 else False
    
def findSReplacement(x, y):
   for tile in tiles.keys():
      connections_count = 0
      for step_direction, step_coords in steps.items():
        try:
          cX = x+step_coords[0]
          cY = y+step_coords[1]
          toCheck = array2D[cY][cX]
          if cX < 0 or cY < 0 or cY > len(array2D) or cX > len(array2D[y]):
              continue
          pipe_directions = connections[tile]
          available_connection = pipe_directions.get(step_direction, [])
          if toCheck in available_connection or toCheck == "S":
              connections_count += 1
        except IndexError:
            continue
      if connections_count == 2:
         return tile

s_coords = (-1, -1)
for iy, row in enumerate(array2D):
   for ix, tile in enumerate(row):
      if tile == "S":
        s_coords = (ix, iy)
      if not isConnected(ix,iy):
         array2D[iy][ix] = "."

s_replacement = findSReplacement(s_coords[0], s_coords[1])

def pathPrint():
   for row in array2D:
    row_string = ''.join(str(tile) for tile in row)
    for key, value in tiles.items():
      row_string = row_string.replace(key, value)
    print(row_string)

def findNextPointsCoords(origin_coord, origin_tile):
  """ pass (x, y) tuple as startingCoords
  """
  availableDirections = connections[origin_tile]
  nextPoints = []
  for direction in availableDirections.keys():
      step = steps[direction]
      nextPoint = (origin_coord[0] + step[0],  origin_coord[1] + step[1])
      nextPoints.append(nextPoint)
  return nextPoints

def buildPaths(startingCoords , startingTile):
    """ pass (x, y) tuple as startingCoords
    """
    startingPoints = findNextPointsCoords(startingCoords, startingTile)
    paths = []
    for point in startingPoints:
      path = [point]
      previous_point = (startingCoords, startingTile)
      current_point = (point, array2D[point[1]][point[0]])
      returned_to_S = False
      while not returned_to_S:
        potential_next_points = findNextPointsCoords(current_point[0], current_point[1])
        next_coords = next(filter(lambda np: np != previous_point[0],  potential_next_points ))
        next_tile = array2D[next_coords[1]][next_coords[0]]
        previous_point = current_point
        current_point = (next_coords, next_tile)
        if next_tile == "S":
           returned_to_S = True
           continue
        else:
           path.append(next_coords)
      paths.append(path)
    return paths
       
path1, path2 = buildPaths(s_coords, s_replacement)
furthermost = (-1, -1)

for index, (a, b) in enumerate(zip(path1, path2)):
   if a == b:
      furthermost = a

pathPrint()
print(f"replace S with: {tiles[s_replacement]}")
print(f"furthermost point: {furthermost}")
print(f"Steps: {path1.index(furthermost)+1}")

# part2
my_path = [s_coords, *path1]
npArray = np.array([[point[0], point[1]] for point in my_path ])
npPath = path.Path(npArray)

points_within = 0
for iy, row in enumerate(array2D):
   for ix, tile in enumerate(row):
      if (ix, iy) in my_path:
         continue
      if npPath.contains_point([ix, iy]):
         points_within += 1

print(f"points within: {points_within}")