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
