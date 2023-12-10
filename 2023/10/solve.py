"""AOC 10th day."""
from matplotlib import path

steps = {
  "↑": (0, -1),
  "←": (-1, 0),
  "→": (1, 0), 
  "↓": (0, 1)
}

tiles = { # alternative symbol just for visualization 
  "|": "║",
  "-": "═",
  "L": "╚",
  "J": "╝",
  "7": "╗",
  "F": "╔",
  ".": " ",
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

def isTileInClosedLoop(x, y, array2D):
    """ function became useless after finishing part 2
        it helped to clean visualization in part 1 tho
    """
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
          pipe_directions = connections[tile]
          available_connection = pipe_directions.get(step_direction, [])
          if toCheck in available_connection or toCheck == "S":
              connections_count += 1
        except IndexError:
            continue
      return True if connections_count >= 2 else False
    
def findSReplacement(s_coords, array2D):
   for tile in tiles.keys():
      connections_count = 0
      for step_direction, step_coords in steps.items():
        try:
          cX = s_coords[0]+step_coords[0]
          cY = s_coords[1]+step_coords[1]
          toCheck = array2D[cY][cX]
          if cX < 0 or cY < 0 or cY > len(array2D) or cX > len(array2D[cY]):
              continue
          pipe_directions = connections[tile]
          available_connection = pipe_directions.get(step_direction, [])
          if toCheck in available_connection or toCheck == "S":
              connections_count += 1
        except IndexError:
            continue
      if connections_count == 2:
         return tile

def pathPrint(array2D):
   for row in array2D:
    row_string = ''.join(str(tile) for tile in row)
    for key, value in tiles.items():
      row_string = row_string.replace(key, value)
    print(row_string)

def findNextPointsCoords(origin_coord, origin_tile):
  """ function returns coordinates of possible moves from provided tile
      pass (x, y) tuple and tile symbol
  """
  availableDirections = connections[origin_tile]
  nextPoints = []
  for direction in availableDirections.keys():
      step = steps[direction]
      nextPoint = (origin_coord[0] + step[0],  origin_coord[1] + step[1])
      nextPoints.append(nextPoint)
  return nextPoints

def buildPaths(startingCoords , startingTile, array2D):
    """ function returns path of closed loop starting with provided tile
        pass (x, y) tuple and tile symbol
    """
    startingPoints = findNextPointsCoords(startingCoords, startingTile)
    paths = []
    for point in startingPoints:
      path = [startingCoords, point]
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
       
def getFurthermostPoint(path1, path2):
  """ returns first point where closed loop path meets together
      provide paths that starts from the same point but goes in opposite directions
  """
  for (a, b) in zip(path1[1::1], path2[1::1]):
    if a == b:
      return a
  return None

def main():
  array2D = []
  f = open('./10/1.txt', 'r')
  for idx, row in enumerate(f.read().splitlines()):
    array2D.append([])
    for value in row:
        array2D[idx].append(value)
  f.close()

  #part 1
  s_coords = (-1, -1)
  for iy, row in enumerate(array2D):
    for ix, tile in enumerate(row):
        if tile == "S":
          s_coords = (ix, iy)
        if not isTileInClosedLoop(ix,iy, array2D):
          array2D[iy][ix] = "."

  s_replacement = findSReplacement(s_coords, array2D)
  path1, path2 = buildPaths(s_coords, s_replacement, array2D)
  furthermost = getFurthermostPoint(path1, path2)
  print(f"replace S with: {tiles[s_replacement]}")
  print(f"furthermost point: {furthermost}")
  # do not count first tile (S) as step and then we add 1 cause first step index is 0
  print(f"Steps: {path1[1::].index(furthermost)+1}")

  # part2
  my_path = [s_coords, *path1]
  npPath = path.Path(my_path)

  points_within = 0
  for iy, row in enumerate(array2D):
    for ix, tile in enumerate(row):
        if (ix, iy) in my_path:
          continue
        else: 
          array2D[iy][ix] = "."
        if npPath.contains_point([ix, iy]):
          points_within += 1

  print(f"points within: {points_within}")

  print_visualization = False
  if print_visualization:
    pathPrint(array2D)

if __name__ == '__main__':
    main()