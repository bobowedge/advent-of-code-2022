import math


def lcd(x, y):
    return x * y // math.gcd(x, y)


def parse_data(data: str):
    data = data.splitlines()

    directions = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}

    blizzards = dict()
    row_max = len(data)
    col_max = len(data[0])
    for row, line in enumerate(data):
        for col, ch in enumerate(line):
            if ch in ['.', '#']:
                continue
            if ch not in directions.keys():
                assert False
            curr_list = blizzards.get((row, col), [])
            curr_list.append(directions[ch])
            blizzards[(row, col)] = curr_list
    return blizzards, row_max, col_max


def all_blizzards(blizzards, row_max, col_max):
    num_states = lcd(row_max-2, col_max-2)
    all_blizzards = {}
    for step in range(num_states):
        blocked = set()
        new_blizzards = {}
        for (row, col), directions in blizzards.items():
            blocked.add((row, col))
            for direction in directions:
                new_row = row + direction[0]
                if new_row == row_max-1:
                    new_row = 1
                elif new_row == 0:
                    new_row = row_max-2
                new_col = col + direction[1]
                if new_col == col_max-1:
                    new_col = 1
                elif new_col == 0:
                    new_col = col_max-2
                curr_list = new_blizzards.get((new_row, new_col), [])
                curr_list.append(direction)
                new_blizzards[(new_row, new_col)] = curr_list
        blizzards = dict(new_blizzards)
        all_blizzards[step] = blocked
    return all_blizzards


def solution1(data: str):
    blizzards, row_max, col_max = parse_data(data)
    blizzards = all_blizzards(blizzards, row_max, col_max)
    lenblizz = len(blizzards)

    walls = set()
    for x in range(row_max):
        walls.add((x, 0))
        walls.add((x, col_max-1))
    for y in range(col_max):
        if y != 1:
            walls.add((0, y))
        if y != col_max - 2:
            walls.add((row_max-1, y))
    walls.add((-1, 1))

    start = (0, 1)
    end = (row_max-1, col_max-2)
    paths = set()
    paths.add(start)
    steps = 0
    while end not in paths:
        steps += 1
        blocked = blizzards[steps % lenblizz].union(walls)
        new_paths = set()
        for (posx, posy) in paths:
            for (x, y) in [(posx, posy), (posx+1, posy), (posx-1, posy), (posx, posy+1), (posx, posy-1)]:
                if (x, y) == end:
                    new_paths.add((x, y))
                    break
                if (x, y) in blocked:
                    continue
                new_paths.add((x, y))
        paths = new_paths
    return steps


def solution2(data: str):
    blizzards, row_max, col_max = parse_data(data)
    blizzards = all_blizzards(blizzards, row_max, col_max)
    lenblizz = len(blizzards)

    walls = set()
    for x in range(row_max):
        walls.add((x, 0))
        walls.add((x, col_max - 1))
    for y in range(col_max):
        if y != 1:
            walls.add((0, y))
        if y != col_max - 2:
            walls.add((row_max - 1, y))
    walls.add((-1, 1))
    walls.add((row_max, col_max - 2))

    start = (0, 1)
    end = (row_max - 1, col_max - 2)
    goals = [end, start, end]
    paths = set()
    paths.add(start)
    steps = 0
    while goals:
        steps += 1
        blocked = blizzards[steps % lenblizz].union(walls)
        new_paths = set()
        for (posx, posy) in paths:
            for (x, y) in [(posx, posy), (posx + 1, posy), (posx - 1, posy), (posx, posy + 1), (posx, posy - 1)]:
                if (x, y) == goals[0]:
                    new_paths.add((x, y))
                    break
                if (x, y) in blocked:
                    continue
                new_paths.add((x, y))
        if goals[0] in new_paths:
            # print(f"Reached {goals[0]} in {steps} steps")
            paths = set()
            paths.add(goals.pop(0))
        else:
            paths = new_paths
    return steps


data = open("data/day24.txt").read()
# data = '''#.######
# #>>.<^<#
# #.<..<<#
# #>v.><>#
# #<^v^^>#
# ######.#'''
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
