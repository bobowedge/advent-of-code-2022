import re
import math


def parse_line(line):
    rocks = set()
    line = line.split(" -> ")
    for i in range(len(line)-1):
        x1, y1 = [int(z) for z in line[i].split(",")]
        x2, y2 = [int(z) for z in line[i+1].split(",")]
        if x1 == x2:
            sgn = int(math.copysign(1, y2-y1))
            for y in range(y1, y2+sgn, sgn):
                rocks.add((x1, y))
        else:
            sgn = int(math.copysign(1, x2-x1))
            for x in range(x1, x2+sgn, sgn):
                rocks.add((x, y1))
    return rocks


def solution1(data):
    rocks = set()
    for line in data:
        new_rocks = parse_line(line)
        rocks = rocks.union(new_rocks)

    maxy = 0
    for rx, ry in rocks:
        if ry > maxy:
            maxy = ry

    sand_count = 0
    while True:
        sand = (500, 0)
        while sand[1] < maxy:
            if (sand[0], sand[1] + 1) not in rocks:
                sand = (sand[0], sand[1] + 1)
                continue
            if (sand[0] - 1, sand[1] + 1) not in rocks:
                sand = (sand[0] - 1, sand[1] + 1)
                continue
            if (sand[0] + 1, sand[1] + 1) not in rocks:
                sand = (sand[0] + 1, sand[1] + 1)
                continue
            break
        if sand[1] >= maxy:
            break
        else:
            rocks.add(sand)
            sand_count += 1
    return sand_count


def solution2(data):
    rocks = set()
    for line in data:
        new_rocks = parse_line(line)
        rocks = rocks.union(new_rocks)

    floor = 0
    for rx, ry in rocks:
        if ry + 2 > floor:
            floor = ry + 2

    sand_count = 0
    while True:
        sand = (500, 0)
        while sand[1] + 1 < floor:
            if (sand[0], sand[1] + 1) not in rocks:
                sand = (sand[0], sand[1] + 1)
                continue
            if (sand[0] - 1, sand[1] + 1) not in rocks:
                sand = (sand[0] - 1, sand[1] + 1)
                continue
            if (sand[0] + 1, sand[1] + 1) not in rocks:
                sand = (sand[0] + 1, sand[1] + 1)
                continue
            break
        if sand == (500, 0):
            sand_count += 1
            break
        rocks.add(sand)
        sand_count += 1
    return sand_count


data = open("data/day14.txt").read().splitlines()
# data = '''498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9'''.splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
