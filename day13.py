from ast import literal_eval
from functools import cmp_to_key


def compare(x, y):
    typex = type(x)
    typey = type(y)
    if typex == int and typey == int:
        if x < y:
            return -1
        elif x > y:
            return 1
        else:
            return 0
    elif typex == int and typey == list:
        return compare([x], y)
    elif typex == list and typey == int:
        return compare(x, [y])
    else:
        for i in range(len(x)):
            if i >= len(y):
                return 1
            comp = compare(x[i], y[i])
            if comp != 0:
                return comp
        if len(x) < len(y):
            return -1
        else:
            return 0


def solution1(data):
    counter = 0
    score = 0
    for i in range(0, len(data), 3):
        x = literal_eval(data[i])
        y = literal_eval(data[i+1])
        counter += 1
        if compare(x, y) == -1:
            score += counter
    return score


def solution2(data):
    packets = [[[2]], [[6]]]
    for i in range(0, len(data), 3):
        x = literal_eval(data[i])
        y = literal_eval(data[i+1])
        packets.append(x)
        packets.append(y)
    packets.sort(key=cmp_to_key(compare))
    index2 = packets.index([[2]]) + 1
    index6 = packets.index([[6]]) + 1
    return index2 * index6


data = open("data/day13.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
