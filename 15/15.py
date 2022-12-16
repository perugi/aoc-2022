import re
from collections import namedtuple
import itertools

# filename = "test.txt"
filename = "input.txt"

with open(filename) as f:
    content = f.read().splitlines()

sensors_re = re.compile(
    r"Sensor at x=([\-\d]+), y=([\-\d]+): closest beacon is at x=([\-\d]+), y=([\-\d]+)"
)

data = namedtuple("data", ["x", "y", "dis"])
sensors = []
beacon = namedtuple("beacon", ["x", "y"])
beacons = set()

for line in content:
    mo = sensors_re.search(line)
    loc_x = int(mo[1])
    loc_y = int(mo[2])
    beacon_x = int(mo[3])
    beacon_y = int(mo[4])
    sensors.append(
        data(
            loc_x,
            loc_y,
            abs(loc_x - beacon_x) + abs(loc_y - beacon_y),
        )
    )
    beacons.add(beacon(beacon_x, beacon_y))

""" Part One """

# target_row = 10
target_row = 2000000

exclusions = []
exclusion = namedtuple("exclusion", ["start", "end"])
# Find the exclusion lines from an individual sensor (create a list of tuples of start and stop x-coordinates
# for the exclusion zones)
for sensor in sensors:

    # Skip sensors which are more than their manhattan distance away on the y-axis.
    sensor_row_y = abs(sensor.y - target_row)
    if sensor_row_y > sensor.dis:
        continue

    # Exclusion radius is the number of coords left/right from the sensor center that it contains.
    exclusion_rad = sensor.dis - sensor_row_y
    exclusions.append(exclusion(sensor.x - exclusion_rad, sensor.x + exclusion_rad))


# Figure out the number of excludes x-coordinates by creating a combined set of all the exclusion zones x-elements
excluded_x = set()
for exclusion in exclusions:
    for i in range(exclusion.start, exclusion.end + 1):
        excluded_x.add(i)

# For the final answer, we need to remove any beacons that are on the tested line, in the excluded radius
beacon_in_radius = 0
for beacon in beacons:
    if beacon.y != target_row:
        continue
    if beacon.x in excluded_x:
        beacon_in_radius += 1

print(
    f"Number of positions that cannot contain the beacon: {len(excluded_x) - beacon_in_radius}"
)

""" Part Two """

# RANGE = 20
RANGE = 4000000

point = namedtuple("point", ("x", "y"))
# The values represent the projection of the borders + 1 pixel to the y-axis.
border = namedtuple("border", ("lb, lt, rb, rt"))
borders = []
for sensor in sensors:

    left_point = point(sensor.x - sensor.dis - 1, sensor.y)
    print(f"l: {left_point}")
    lb = left_point.y + left_point.x
    lt = left_point.y - left_point.x

    right_point = point(sensor.x + sensor.dis + 1, sensor.y)
    print(f"r: {right_point}")
    rb = right_point.y - right_point.x
    rt = right_point.y + right_point.x

    borders.append(border(lb, lt, rb, rt))

# Find four borders that intersect (lb with rt and lt with rb).
for b_1, b_2, b_3, b_4 in itertools.product(borders, repeat=4):
    if (
        b_1.lb == b_2.rt and (b_1.rb <= b_2.rb <= b_1.lt or b_1.rb <= b_2.lt <= b_1.lt)
    ) and (
        b_3.lt == b_4.rb and (b_3.lb <= b_4.lb <= b_3.rt or b_3.lb <= b_4.rt <= b_3.rt)
    ):
        x = (b_1.lb - b_3.lt) / 2
        y = (b_1.lb + b_3.lt) / 2
        if 0 <= x <= RANGE and 0 <= y <= RANGE:
            print(x * RANGE + y)
