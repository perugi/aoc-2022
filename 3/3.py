from collections import namedtuple

filename = "input.txt"

rucksacks = []
rucksack = namedtuple("rucksack", ["first", "second"])
with open(filename) as f:
    # Generate a list of tuples, the first element being the content of the first
    # compartment and the second of the secoind one.
    for line in f:
        mid = int(len(line) / 2)
        rucksacks.append(rucksack(line[:mid], line[mid:]))


def find_priority(item):
    if item.islower():
        # Lowercase item types a through z have priorities 1 through 26.
        return ord(item) - 96
    else:
        # Uppercase item types A through Z have priorities 27 through 52.
        return ord(item) - 38


""" Part One """
priority = 0
for rucksack in rucksacks:
    for item in rucksack.first:
        if item in rucksack.second:
            priority += find_priority(item)
            break

print(f"Sum of priorities (Part One): {priority}")

""" Part Two """
priority = 0
for i in range(0, len(rucksacks), 3):
    first = rucksacks[i].first + rucksacks[i].second
    second = rucksacks[i + 1].first + rucksacks[i + 1].second
    third = rucksacks[i + 2].first + rucksacks[i + 2].second

    for item in first:
        if item in second and item in third:
            priority += find_priority(item)
            break

print(f"Sum of priorities (Part Two): {priority}")
