filename = "input.txt"

forest = []

with open(filename) as f:
    for line in f:
        forest.append([int(char) for char in line.strip()])

# Create an array of the same dimensions as the forest, to track whether a tree is visible.
visible = [[False for _ in forest[0]] for _ in forest]


def transpose(array):
    return [[row[i] for row in array] for i in range(len(array[0]))]


""" Part One """


def observe(forest, visible):
    """Observe the forest left-right, set True in visible for any trees that can be seen"""
    for row, treeline in enumerate(forest):
        for col, tree in enumerate(treeline):
            # Look from left to right. (Adding -1 so that we have a default value at the
            # left edge, where there are no trees in front of the tested tree).
            if max([-1] + treeline[:col]) < tree:
                visible[row][col] = True

            # Look from right to left.
            if max([-1] + treeline[col + 1 :]) < tree:
                visible[row][col] = True

    return visible


visible = observe(forest, visible)
forest = transpose(forest)
visible = transpose(visible)
visible = observe(forest, visible)

print(
    f"Number of trees that are visible: {sum([sum(treeline) for treeline in visible])}"
)
