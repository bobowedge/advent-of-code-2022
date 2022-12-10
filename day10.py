def solution1(data):
    score_cycles = [20, 60, 100, 140, 180, 220]
    x = 1
    cycle = 1
    scores = [None] * 6
    for line in data:
        line = line.strip()
        for i in range(6):
            if score_cycles[i] - 1 <= cycle <= score_cycles[i] and scores[i] is None:
                scores[i] = score_cycles[i] * x
        if line == "noop":
            cycle += 1
        else:
            x += int(line.split()[1])
            cycle += 2
    return sum(scores)


def draw_crt(position, x):
    if x - 1 <= position <= x + 1:
        print("#", end="")
    else:
        print(".", end="")
    position += 1
    if (position % 40) == 0:
        print("")
        position = 0
    return position


def solution2(data):
    x = 1
    position = 0
    for line in data:
        if line == "noop":
            position = draw_crt(position, x)
        else:
            position = draw_crt(position, x)
            position = draw_crt(position, x)
            x += int(line.split()[1])
    return


data = open("data/day10.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")

print(f"Solution 2:")
solution2(data)

