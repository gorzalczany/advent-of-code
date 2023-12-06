from collections import defaultdict

D = open('./5/1.txt', 'r').read().strip()
lines = D.split('\n')

seeds = []
seedsInput = [int(x) for x in lines.pop(0).split(':')[1].split()]
seeds_ranges = []
while len(seedsInput) >= 2:
  rs = seedsInput.pop(0)
  rl = seedsInput.pop(0)
  seeds_ranges.append(range(rs, rs+rl, 1))

soil_ranges = []
fertilizer_ranges = []
water_ranges = []
temperature_ranges = []
humidity_ranges = []
light_ranges = []
location_ranges = []

maps = defaultdict(str)
mapKey = ""
for line in lines:
  if "map" in line:
    mapKey = line.split()[0]
    print(f"new map key: {mapKey}")
    continue
  
  map = [int(x) for x in line.split()]
  if len(map) <= 0:
    continue

  destination_range_start = map[0]
  source_range_start = map[1]
  range_length = map[2]

  range_diff = source_range_start - destination_range_start
  exec(mapKey.split('-')[-1] +"_ranges" + f".append((range({source_range_start},{source_range_start+range_length},1), {range_diff}))")


min_location = -1
for seeds_range in seeds_ranges:
  for seed in seeds_range:
    soil = -1
    fertilizer =  -1
    water =  -1
    light =  -1
    temperature =  -1
    humidity =  -1
    location =  -1

    for r, d in soil_ranges:
      if seed in r:
        soil = seed - d
        break
    if soil == -1:
      soil = seed

    x = soil
    for r, d in fertilizer_ranges:
      if x in r:
        fertilizer = x - d
        break
    if fertilizer == -1:
      fertilizer = x

    x = fertilizer
    for r, d in water_ranges:
      if x in r:
        water = x - d
        break
    if water == -1:
      water = x

    x = water
    for r, d in light_ranges:
      if x in r:
        light = x - d
        break
    if light == -1:
      light = x

    x = light
    for r, d in temperature_ranges:
      if x in r:
        temperature = x - d
        break
    if temperature == -1:
      temperature = x

    x = temperature
    for r, d in humidity_ranges:
      if x in r:
        humidity = x - d
        break
    if humidity == -1:
      humidity = x

    x = humidity
    for r, d in location_ranges:
      if x in r:
        location = x - d
        break
    if location == -1:
      location = x

    if min_location < 0:
      min_location = location
    else:
      if location < min_location:
        print(min(min_location, location))
      min_location = min(min_location, location)
