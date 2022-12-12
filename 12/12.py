from collections import namedtuple
from pprint import pprint
import math

filename = "input.txt"

nodes = {}
with open(filename) as f:
    for row, line in enumerate(f):
        for col, char in enumerate(line.strip()):
            if char == "S":
                char = "a"
                start = (col, row)
            elif char == "E":
                char = "z"
                end = (col, row)
            nodes[(col, row)] = {"height": char, "paths": [], "distance": math.inf}

dimension_x = col
dimension_y = row

# Build the lists of paths between the nodes. Ignore the paths with elevation change of more than one.
try_paths = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for node in nodes:
    for try_path in try_paths:
        # Generate a candidate destination node (element-wise list addition)
        dest_node = tuple([sum(i) for i in zip(node, try_path)])
        # Do not judge the nodes that would fall out of the list dimensions
        if (
            dest_node[0] < 0
            or dest_node[0] > dimension_x
            or dest_node[1] < 0
            or dest_node[1] > dimension_y
        ):
            continue
        elevation_diff = ord(nodes[dest_node]["height"]) - ord(nodes[node]["height"])
        # The elevation difference between the destination and the current node needs to be less or equal to one.
        if elevation_diff <= 1:
            nodes[node]["paths"].append(dest_node)

# Let's get some Dijkstra action up in here
def get_min_path(nodes, start, end):
    nodes[start]["distance"] = 0
    distances = {}
    while nodes:
        active_node = min(nodes, key=lambda x: nodes[x]["distance"])
        current_dis = nodes[active_node]["distance"]
        for dest_node in nodes[active_node]["paths"]:
            if dest_node in distances:
                continue
            elif current_dis + 1 < nodes[dest_node]["distance"]:
                nodes[dest_node]["distance"] = current_dis + 1
        distances[active_node] = nodes.pop(active_node)

    return distances[end]["distance"]


""" Part One """
print(f"Distance to E: {get_min_path(nodes, start, end)}")
