from collections import namedtuple

filename = "input.txt"

matches = []
match = namedtuple("match", ["opponent", "me"])
with open(filename) as f:
    # Generate a list of tuples, the first element being the opponent move and second my move.
    for line in f:
        matches.append(match(line[0], line[2]))

""" Part One """
SCORES_SHAPE = {"X": 1, "Y": 2, "Z": 3}
SCORES_OUTCOME = {"lose": 0, "tie": 3, "win": 6}
SHAPE_WINS = {"X": "C", "Y": "A", "Z": "B"}
SHAPE_LOSSES = {"X": "B", "Y": "C", "Z": "A"}

score = 0
for match in matches:
    # Get the score for the outcome of the match.
    if SHAPE_WINS[match.me] == match.opponent:
        score += SCORES_OUTCOME["win"]
    elif SHAPE_LOSSES[match.me] == match.opponent:
        score += SCORES_OUTCOME["lose"]
    else:
        score += SCORES_OUTCOME["tie"]

    # Get the score for the shape I have selected.
    score += SCORES_SHAPE[match.me]

print(f"My score (Part One): {score}")

""" Part Two """
SCORES_SHAPE = {"A": 1, "B": 2, "C": 3}
SCORES_OUTCOME = {"X": 0, "Y": 3, "Z": 6}
SHAPE_WINS = {"A": "B", "B": "C", "C": "A"}
SHAPE_LOSSES = {"A": "C", "B": "A", "C": "B"}

score = 0
for match in matches:
    # Get the score for the outcome of the match.
    score += SCORES_OUTCOME[match.me]

    # Get the score for the shape I have selected.
    if match.me == "X":
        my_shape = SHAPE_LOSSES[match.opponent]
    elif match.me == "Y":
        my_shape = match.opponent
    else:
        my_shape = SHAPE_WINS[match.opponent]
    score += SCORES_SHAPE[my_shape]

print(f"My score (Part Two): {score}")
