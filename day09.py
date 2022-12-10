import re


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, d):
        if d == 'R':
            self.x += 1
        elif d == 'L':
            self.x -= 1
        elif d == 'U':
            self.y += 1
        elif d == 'D':
            self.y -= 1
        else:
            raise RuntimeError("Invalid direction")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return str((self.x, self.y))


def new_tail(head, tail):
    if abs(tail.x - head.x) <= 1 and abs(tail.y - head.y) <= 1:
        return Point(tail.x, tail.y)
    if abs(tail.y - head.y) == 2:
        y = (head.y + tail.y) // 2
    else:
        y = head.y
    if abs(tail.x - head.x) == 2:
        x = (head.x + tail.x) // 2
    else:
        x = head.x
    return Point(x, y)


def solution1(data):
    head = Point(0, 0)
    tail = Point(0, 0)
    pts1 = set()
    pts1.add(tail)
    for line in data:
        match = re.match(r"(\S) (\d+)", line)
        d = match.group(1)
        v = int(match.group(2))
        for _ in range(v):
            head.move(d)
            tail = new_tail(head, tail)
            pts1.add(tail)
    return len(pts1)


def solution2(data):
    rope = [Point(0, 0) for _ in range(10)]
    pts9 = set()
    pts9.add(rope[-1])

    for line in data:
        match = re.match(r"(\S) (\d+)", line)
        d = match.group(1)
        v = int(match.group(2))
        for _ in range(v):
            rope[0].move(d)
            for t in range(1, 10):
                rope[t] = new_tail(rope[t-1], rope[t])
            pts9.add(rope[-1])
    return len(pts9)


data = open("data/day09.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
