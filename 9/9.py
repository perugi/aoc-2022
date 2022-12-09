from collections import namedtuple
from operator import add

filename = "input.txt"
DIRECTIONS = {"L": [-1, 0], "R": [1, 0], "U": [0, 1], "D": [0, -1]}

instrs = []
instr = namedtuple("instr", ["dir", "steps"])
with open(filename) as f:
    for line in f:
        line = line.strip().split(" ")
        instrs.append(instr(line[0], int(line[1])))


""" Day One """

head_pos = [0, 0]
tail_pos = [0, 0]
visited = {tuple(tail_pos)}


def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    else:
        return -1


for instr in instrs:
    for step in range(instr.steps):
        head_pos = list(map(add, head_pos, DIRECTIONS[instr.dir]))

        distance = int(
            ((head_pos[0] - tail_pos[0]) ** 2 + (head_pos[1] - tail_pos[1]) ** 2) ** 0.5
        )
        if distance > 1:
            if tail_pos[0] == head_pos[0]:
                tail_pos[1] += sign(head_pos[1] - tail_pos[1])
            elif tail_pos[1] == head_pos[1]:
                tail_pos[0] += sign(head_pos[0] - tail_pos[0])
            # diagonal move
            else:
                tail_pos[0] += sign(head_pos[0] - tail_pos[0])
                tail_pos[1] += sign(head_pos[1] - tail_pos[1])

        visited.add(tuple(tail_pos))


print(f"Number of visited positions (Part Two): {len(visited)}")

""" Day Two """

NUMBER_KNOTS = 9
positions = []
for _ in range(NUMBER_KNOTS + 1):
    positions.append([0, 0])
visited = {tuple(positions[-1])}

for instr in instrs:
    for step in range(instr.steps):
        positions[0] = list(map(add, positions[0], DIRECTIONS[instr.dir]))

        for i, knot in enumerate(positions[1:]):
            # There's probably a nicer way of doing this, but I'm committed.
            # This assignment ensures that I don't go completely insane.
            h, t = i, i + 1

            distance = int(
                (
                    (positions[h][0] - positions[t][0]) ** 2
                    + (positions[h][1] - positions[t][1]) ** 2
                )
                ** 0.5
            )
            if distance > 1:
                if positions[t][0] == positions[h][0]:
                    positions[t][1] += sign(positions[h][1] - positions[t][1])
                elif positions[t][1] == positions[h][1]:
                    positions[t][0] += sign(positions[h][0] - positions[t][0])
                # diagonal move
                else:
                    positions[t][0] += sign(positions[h][0] - positions[t][0])
                    positions[t][1] += sign(positions[h][1] - positions[t][1])

        visited.add(tuple(positions[-1]))

    print(instr)
    print(positions[0], positions[-1])

print(f"Number of visited positions (Part One): {len(visited)}")
