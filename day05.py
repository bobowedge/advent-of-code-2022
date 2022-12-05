import re


def parse_input(data):
    instructions = []
    stacks_lines = []
    for d in data:
        match = re.match("move (\d+) from (\d+) to (\d+)", d)
        if match:
            instructions.append((int(match.group(1)), int(match.group(2)) - 1, int(match.group(3)) - 1))
        else:
            stacks_lines.append(d)

    num_stacks = 0
    stacks = []
    stacks_lines.reverse()
    for sl in stacks_lines:
        if len(sl.strip()) == 0:
            continue
        elif '[' not in sl:
            sl = sl.split()
            num_stacks = len(sl)
            stacks = [""] * num_stacks
        else:
            for i in range(num_stacks):
                loc = 1 + i * 4
                if loc >= len(sl):
                    break
                crate = sl[loc].strip()
                if len(crate) > 0:
                    stacks[i] = stacks[i] + crate
    stacks = [list(x) for x in stacks]
    return stacks, instructions


def tops(stacks):
    value = []
    for i, s in enumerate(stacks):
        value.append(s[-1])
    return ''.join(value)


def solution1(stacks, instructions):
    for num, src, dest in instructions:
        for i in range(num):
            if len(stacks[src]) == 0:
                break
            x = stacks[src].pop()
            stacks[dest].append(x)
    return tops(stacks)


def solution2(stacks, instructions):
    for num, src, dest in instructions:
        stacks[dest].extend(stacks[src][-num:])
        stacks[src] = stacks[src][:-num]
    return tops(stacks)


data = open('data/day05.txt').read().splitlines()

stacks, instructions = parse_input(data)
tops1 = solution1(stacks, instructions)
print(f"Solution 1: {tops1}")

stacks, instructions = parse_input(data)
tops2 = solution2(stacks, instructions)
print(f"Solution 2: {tops2}")
