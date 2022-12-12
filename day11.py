import re


def op(val, op1, op2):
    if op2 == "old":
        val2 = val
    else:
        val2 = int(op2)
    if op1 == "*":
        return val * val2
    else:
        return val + val2


class Monkey:
    def __init__(self, number, items, op1, op2, divby, mtrue, mfalse):
        self.number = number
        self.items = items
        self.op1 = op1
        self.op2 = op2
        self.divby = divby
        self.mtrue = mtrue
        self.mfalse = mfalse
        self.counter = 0

    def inspect_items(self, lcm=None):
        new_items = []
        for item in self.items:
            new_item = op(item, self.op1, self.op2)
            if lcm is None:
                new_item = new_item // 3
            else:
                new_item %= lcm
            if new_item % self.divby == 0:
                new_items.append((self.mtrue, new_item))
            else:
                new_items.append((self.mfalse, new_item))
        self.counter += len(self.items)
        self.items = []
        return new_items


def monkey_parser(data, soln1):
    match = re.search(r"Monkey (\d+):", data[0])
    mnum = int(match.group(1))
    match = re.search(r"Starting items: (.*)", data[1])
    items = [int(x) for x in match.group(1).split(",")]
    match = re.search(r"Operation: new = old (\S+) (\S+)", data[2])
    op1 = match.group(1)
    op2 = match.group(2)
    match = re.search(r"Test: divisible by (\d+)", data[3])
    divby = int(match.group(1))
    match = re.search(r"If true: throw to monkey (\d+)", data[4])
    mtrue = int(match.group(1))
    match = re.search(r"If false: throw to monkey (\d+)", data[5])
    mfalse = int(match.group(1))
    return Monkey(mnum, items, op1, op2, divby, mtrue, mfalse)


def solution1(data):
    monkeys = []
    for i in range(0, len(data), 7):
        monkey = monkey_parser(data[i:i + 7], True)
        monkeys.append(monkey)

    for _ in range(20):
        for m in range(len(monkeys)):
            new_items = monkeys[m].inspect_items()
            for newm, new_item in new_items:
                monkeys[newm].items.append(new_item)

    counters = [m.counter for m in monkeys]
    counters.sort(reverse=True)
    return counters[0] * counters[1]


def solution2(data):
    monkeys = []
    lcm = 1
    for i in range(0, len(data), 7):
        monkey = monkey_parser(data[i:i + 7], False)
        monkeys.append(monkey)
        lcm *= monkey.divby

    for _ in range(10000):
        for m in range(len(monkeys)):
            new_items = monkeys[m].inspect_items(lcm)
            for newm, new_item in new_items:
                monkeys[newm].items.append(new_item)

    counters = [m.counter for m in monkeys]
    counters.sort(reverse=True)
    return counters[0] * counters[1]


data = open("data/day11.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
