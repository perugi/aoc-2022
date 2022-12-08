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

""" Part Two"""

forest = transpose(forest)
# Create an array of the same dimensions as the forest, to track the scenic scores
scores = [[1 for _ in forest[0]] for _ in forest]


def evaluate(forest, scores):
    for row, treeline in enumerate(forest):
        for col, tree in enumerate(treeline):
            # Look left.
            visible_trees = treeline[:col]
            if visible_trees:
                for index, other_tree in enumerate(reversed(visible_trees)):
                    if other_tree >= tree:
                        visible_trees = visible_trees[-index - 1 :]
                        break
            scores[row][col] *= len(visible_trees)

            # Look right
            visible_trees = treeline[col + 1 :]
            if visible_trees:
                for index, other_tree in enumerate(visible_trees):
                    if other_tree >= tree:
                        visible_trees = visible_trees[: index + 1]
                        break
            scores[row][col] *= len(visible_trees)

    return scores


scores = evaluate(forest, scores)
forest = transpose(forest)
scores = transpose(scores)
scores = evaluate(forest, scores)

print(f"Highest scenic score: {max([max(treeline) for treeline in scores])}")
