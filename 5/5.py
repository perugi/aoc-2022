from collections import namedtuple
import copy

filename = "input.txt"

starting_stacks = {i: [] for i in range(1, 10)}
with open(filename) as f:
    # Build up the initial state of the stacks
    line = ""
    while line != "\n":
        line = f.readline()

        for stack_no, index in zip(range(1, 10), range(1, len(line), 4)):
            if line[index].isupper():
                # Build list so that the crate on the top of the stack is the last in the list.
                starting_stacks[stack_no].insert(0, line[index])

    instructions = []
    instruction = namedtuple("instruction", ["quantity", "origin", "dest"])
    while True:

        line = f.readline().strip()
        if not line:
            break
        contents = line.split(" ")
        instructions.append(
            instruction(int(contents[1]), int(contents[3]), int(contents[5]))
        )

""" Part One """
stacks = copy.deepcopy(starting_stacks)

# Go through the instructions and simulate the moves
for instr in instructions:
    for _ in range(instr.quantity):
        stacks[instr.dest].append(stacks[instr.origin].pop())

print("Crates on top of each stack (Part One):")
for stack in stacks.values():
    print(stack[-1], end="")

""" Part Two """
stacks = copy.deepcopy(starting_stacks)

# Go through the instructions and simulate the moves
for instr in instructions:
    stacks[instr.dest] = stacks[instr.dest] + stacks[instr.origin][-instr.quantity :]
    del stacks[instr.origin][-instr.quantity :]

print("")
print("Crates on top of each stack (Part Two):")
for stack in stacks.values():
    print(stack[-1], end="")
