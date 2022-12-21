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
    valves=valves,
    location="AA",
    open_valves=[],
    closed_valves=[valve for valve in valves if valves[valve]["flow_rate"] > 0],
    time_remaining=30,
    pressure_release=0,
    memo={},
):
    # print(location, closed_valves, open_valves)
    key = (
        location
        + ","
        + ",".join(open_valves)
        + ","
        + str(time_remaining)
        + ","
        + str(pressure_release)
    )
    if key in memo:
        return memo[key]

    if time_remaining == 0 or not closed_valves:
        return (pressure_release, open_valves)

    # print(
    #     f"location: {location}, time: {time_remaining}, pressure: {pressure_release}, open: {open_valves}, closed: {closed_valves}"
    # )

    actions = [(0, [])]

    # Move to one of the closed valves with a non-zero flow rate and open it
    for dest in closed_valves:
        new_open = open_valves.copy() + [dest]
        new_closed = closed_valves.copy()
        new_closed.remove(dest)
        new_time = time_remaining - (len(shortest_paths[location][dest]) + 1)
        new_pressure_release = pressure_release + valves[dest]["flow_rate"] * new_time
        actions.append(
            perform_action(
                location=dest,
                open_valves=new_open,
                closed_valves=new_closed,
                time_remaining=new_time,
                pressure_release=new_pressure_release,
                memo=memo,
            )
        )

    # print(time_remaining, actions)
    actions.sort(key=lambda x: x[0], reverse=True)
    best_action = actions[0]

    # print(pressure_release)
    memo[key] = (
        best_action[0],
        best_action[1],
    )
    return memo[key]


print(perform_action(valves))
