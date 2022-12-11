import re
from pprint import pprint
import copy
from functools import reduce

filename = "input.txt"

with open(filename) as f:
    content = f.read().split("\n\n")

instructions_re = re.compile(
    r"Monkey (\d+):\n  Starting items: ([\d, ]+)\n  Operation: new = ([\w*\+ ]+)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)"
)


orig_monkeys = []

for instructions in content:
    mo = instructions_re.search(instructions)
    orig_monkeys.append(
        {
            "items": list(
                map(int, mo[2].split(", "))
            ),  # Split into a list and convert items to ints
            "operation": mo[3],
            "divisor": int(mo[4]),
            "true": int(mo[5]),
            "false": int(mo[6]),
            "inspected": 0,
        }
    )

""" Part One """
monkeys = copy.deepcopy(orig_monkeys)

for round in range(1, 21):
    for monkey in monkeys:
        for old in monkey["items"]:
            new = eval(monkey["operation"])
            new = int(new / 3)
            if new % monkey["divisor"] == 0:
                monkeys[monkey["true"]]["items"].append(new)
            else:
                monkeys[monkey["false"]]["items"].append(new)
            monkey["inspected"] += 1
        monkey["items"] = []

monkeys.sort(key=lambda monkey: monkey["inspected"], reverse=True)
monkey_business = monkeys[0]["inspected"] * monkeys[1]["inspected"]
print(
    f"Level of monkey business after 20 rounds of stuff-slinging simian shenanigans: {monkey_business}"
)

""" Part Two """
monkeys = copy.deepcopy(orig_monkeys)
common_divisor = reduce((lambda x, y: x * y), [monkey["divisor"] for monkey in monkeys])

for round in range(1, 10001):
    for monkey in monkeys:
        for old in monkey["items"]:
            new = eval(monkey["operation"])
            new = new % common_divisor
            if new % monkey["divisor"] == 0:
                monkeys[monkey["true"]]["items"].append(new)
            else:
                monkeys[monkey["false"]]["items"].append(new)
            monkey["inspected"] += 1
        monkey["items"] = []

monkeys.sort(key=lambda monkey: monkey["inspected"], reverse=True)
monkey_business = monkeys[0]["inspected"] * monkeys[1]["inspected"]
print(
    f"Level of monkey business after 10000 rounds of stuff-slinging simian shenanigans: {monkey_business}"
)
