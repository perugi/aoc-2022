import re
from pprint import pprint

filename = "test.txt"

regex = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)"
)

valves = dict()
with open(filename) as f:
    for line in f:
        mo = regex.search(line)
        id, flow_rate = mo[1], int(mo[2])
        dests = mo[3].split(", ")
        valves[id] = {"flow_rate": flow_rate, "dests": dests, "parent": None}


def shortest_path(valves, start, end):
    """Return the shortest path between the start and end nodes as a list of nodes"""
    visited, queue = [], [start]
    for valve in valves:
        valves[valve]["parent"] = None

    while True:
        active_node = queue.pop(0)
        if active_node == end:
            break
        for destination in valves[active_node]["dests"]:
            if destination not in visited and destination not in queue:
                valves[destination]["parent"] = active_node
                queue.append(destination)
        visited.append(active_node)

        if not queue:
            return None

    path = []
    while valves[active_node]["parent"] != None:
        path = [active_node] + path
        active_node = valves[active_node]["parent"]

    return path


# Pre-calculate the shortest paths from all the nodes to all the other nodes.
shortest_paths = {
    start: {end: shortest_path(valves, start, end) for end in valves}
    for start in valves
}


def perform_action(
    location="AA",
    open_valves=[],
    pressure_release=0,
    time_remaining=30,
):
    # Perform one of the possible actions, either by opening the valve or taking the tunnel
    # to one of the neighbouring valves. The action is performed by recursively calling the
    # function until the time goes to zero (base case).
    print(location, open_valves)

    if time_remaining == 0:
        return 0

    action_rewards = []

    # Open the valve.
    if location not in open_valves:
        action_rewards.append(
            perform_action(location, open_valves + [location], time_remaining - 1)
        )

    # Move to one of the unopened valves. TODO: only move to the closed valves with a non-zero flow rate/
    for dest in valves[location]["dests"]:
        if dest not in open_valves:
            action_rewards.append(
                perform_action(
                    dest,
                    open_valves,
                    time_remaining - len(shortest_paths[location][dest]),
                )
            )

    return max(action_rewards)


print(perform_action())
