from collections import namedtuple
import time

filename = "input.txt"

with open(filename) as f:
    content = f.read().splitlines()

# Generate a set of tuples, representing the rock locations
obstacles_orig = set()
for line in content:
    coords = line.split(" -> ")
    for i in range(len(coords) - 1):
        start = [int(coord) for coord in coords[i].split(",")]
        end = [int(coord) for coord in coords[i + 1].split(",")]
        if start[0] == end[0]:
            obstacles_orig.update(
                [
                    (start[0], min([start[1], end[1]]) + i)
                    for i in range(abs(start[1] - end[1]) + 1)
                ]
            )
        elif start[1] == end[1]:
            obstacles_orig.update(
                [
                    (min([start[0], end[0]]) + i, start[1])
                    for i in range(abs(start[0] - end[0]) + 1)
                ]
            )


""" Part One """
obstacles = obstacles_orig.copy()
void_y = max([coord[1] for coord in obstacles]) + 1
rocks_no = len(obstacles)


def move_sand(coord):
    """Returns a tuple: Boolean if the sand moved and the sand location"""
    new = list(coord)
    # Move down
    new[1] += 1
    if tuple(new) in obstacles:
        # Try to move down and to the left
        new[0] -= 1
    if tuple(new) in obstacles:
        # Try to move down and to the right
        new[0] += 2
    if tuple(new) in obstacles:
        # If nothing works, return the original location
        return False, coord

    return True, tuple(new)


while True:
    # Generate a new sand unit
    sand = (500, 0)

    while sand[1] < void_y:
        # Try to move. If no movement possible, add to list of resting sands.
        moved, sand = move_sand(sand)
        if not moved:
            obstacles.add(sand)
            break

    if sand[1] >= void_y:
        break

sand_no = len(obstacles) - rocks_no
print(f"Units of sand (Part One): {sand_no}")


""" Part Two """

# Add a floor, two down from the highest y.
# Being lazy, so adding a floor of length 1000. There's probably a more generic solution.
obstacles = obstacles_orig.copy()
floor_y = max([coord[1] for coord in obstacles]) + 2
min_x = min([coord[0] for coord in obstacles])
max_x = max([coord[0] for coord in obstacles])

for x in range(0, 1001):
    obstacles.add((x, floor_y))

rocks_no = len(obstacles)

while True:
    # Generate a new sand unit
    sand = (500, 0)

    while True:
        # Try to move. If no movement possible, add to list of resting sands.
        moved, sand = move_sand(sand)
        if not moved:
            obstacles.add(sand)
            break

    if sand == (500, 0):
        break

sand_no = len(obstacles) - rocks_no
print(f"Units of sand (Part Two): {sand_no}")
