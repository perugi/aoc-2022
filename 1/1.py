filename = "input.txt"

with open(filename) as f:
    content = f.read().splitlines()
    # There is no break on the last line, append it so that the later loop adds the last count.
    content.append("")

""" Part One """
# Sum the calories, held by each elf, delimited by '' lines that are.
cal_counts = []
cal_count = 0
for line in content:
    if line == "":
        # We found an empty line between two elves.
        cal_counts.append(cal_count)
        cal_count = 0
    else:
        cal_count += int(line)

# Find the max. Sorting is used instead of max, because having a sorted list will be useful later on.
# (max() could be used here and also later on, as the algorithm complexity is lower than sort,
# but the dataset is small enough)
cal_counts.sort(reverse=True)
print(f"The elf with the most Calories is carrying {cal_counts[0]} Calories.")

""" Part Two """
# Find the largest three calory counts
print(
    f"The top three elves carrying the most Calories are carrying {sum(cal_counts[0:3])} Calories."
)
