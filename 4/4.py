from collections import namedtuple
import re

filename = "input.txt"

regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")

assignments = []
assignment = namedtuple("assignment", ["first", "second"])
section = namedtuple("section", ["start", "stop"])
with open(filename) as f:
    # Generate a list of tuples, the first element being the content of the first
    # compartment and the second of the secoind one.
    for line in f:
        m = regex.search(line)
        assignments.append(
            assignment(
                section(int(m.group(1)), int(m.group(2))),
                section(int(m.group(3)), int(m.group(4))),
            )
        )

""" Part One """
contains = 0
for assignment in assignments:
    if (
        assignment.first.start >= assignment.second.start
        and assignment.first.stop <= assignment.second.stop
    ) or (
        assignment.second.start >= assignment.first.start
        and assignment.second.stop <= assignment.first.stop
    ):
        contains += 1

print(f"Assignment where one range fully contains the other: {contains}")

""" Part Two """
overlaps = 0
for assignment in assignments:
    if (
        # The first section is starts first
        assignment.first.start <= assignment.second.start
        # Check if the second starts before the first stops
        and assignment.second.start <= assignment.first.stop
    ) or (
        # The second section starts first
        assignment.second.start <= assignment.first.start
        # Check if the first starts before the second stops
        and assignment.first.start <= assignment.second.stop
    ):
        overlaps += 1

print(f"Assignment where the two ranges overlap: {overlaps}")
