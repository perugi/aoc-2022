filename = "input.txt"

with open(filename) as f:
    content = f.read().splitlines()
    # There is no break on the last line, append it so that the later loop adds the last count.
    content.append("")
