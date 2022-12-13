from collections import namedtuple
from itertools import zip_longest
from functools import cmp_to_key
import ast
import json

filename = "input.txt"

""" Part One """

packets = []
packet = namedtuple("packet", ["left", "right"])
with open(filename) as f:
    lines = f.read().split("\n\n")
    for line in lines:
        line = line.split("\n")
        left = json.loads(line[0])
        right = json.loads(line[1])
        packets.append(packet(left, right))


def find_order(left, right):
    if left == None:
        return 1
    elif right == None:
        return -1

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        if left > right:
            return -1
        else:
            return 0

    if isinstance(left, int):
        left = [left]

    if isinstance(right, int):
        right = [right]

    for left_el, right_el in zip_longest(left, right, fillvalue=None):
        compare = find_order(left_el, right_el)
        if compare == 0:
            continue
        return compare

    return 0


sum = 0
for i, packet in enumerate(packets):
    if find_order(packet.left, packet.right) == 1:
        sum += i + 1

print(f"Sum of the indices of pairs in the right order: {sum}")

""" Part Two """
DIVIDER_1 = [[2]]
DIVIDER_2 = [[6]]
packets = [DIVIDER_1, DIVIDER_2]
packet = namedtuple("packet", ["left", "right"])
with open(filename) as f:
    for line in f:
        if line != "\n":
            packets.append(json.loads(line.strip()))

packets = sorted(packets, key=cmp_to_key(find_order), reverse=True)

decoder_key = (packets.index(DIVIDER_1) + 1) * (packets.index(DIVIDER_2) + 1)
print(f"Decoder key for the distress signal: {decoder_key}")
