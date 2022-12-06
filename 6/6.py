filename = "input.txt"

with open(filename) as f:
    content = f.read()


def find_marker(stream, length):
    marker = []
    for i, char in enumerate(stream):
        if char in marker:
            marker = marker[marker.index(char) + 1 :]
        marker.append(char)
        if len(marker) >= length:
            break

    return i + 1


""" Part One """
LEN_MARKER = 4
print(f"First marker after character {find_marker(content, LEN_MARKER)}")


""" Part Two """
LEN_MESSAGE = 14
print(
    f"First start-of-message marker after character {find_marker(content, LEN_MESSAGE)}"
)
