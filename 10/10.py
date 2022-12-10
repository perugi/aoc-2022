from collections import namedtuple

filename = "input.txt"

instrs = []
instr = namedtuple("instr", ["cmd", "val"])
with open(filename) as f:
    # Generate a list of tuples, the first element being the opponent move and second my move.
    for line in f:
        line = line.strip().split(" ")
        if len(line) == 1:
            instrs.append(instr(line[0], None))
        else:
            instrs.append(instr(line[0], int(line[1])))

""" PART ONE """

INSTR_CYCLES = {"noop": 1, "addx": 2}

reg, cycle, strength = 1, 0, 0
for instr in instrs:

    for _ in range(INSTR_CYCLES[instr.cmd]):
        cycle += 1
        if (cycle - 20) % 40 == 0:
            strength += cycle * reg

    if instr.cmd == "addx":
        reg += instr.val

    if cycle > 220:
        break

print(f"Sum of the signal strengths: {strength}")


""" PART TWO """

INSTR_CYCLES = {"noop": 1, "addx": 2}

reg, cycle, h_counter = 1, 0, 0
for instr in instrs:

    for _ in range(INSTR_CYCLES[instr.cmd]):
        cycle += 1

        if abs(reg - h_counter) <= 1:
            print("#", end="")
        else:
            print(".", end="")

        h_counter += 1

        if not (cycle % 40):
            print("")
            h_counter = 0

    if instr.cmd == "addx":
        reg += instr.val
