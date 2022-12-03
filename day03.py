data = open('data/day03.txt').read().splitlines()


def score_item(item):
    value = ord(item)
    if ord('a') <= value <= ord('z'):
        return value - ord('a') + 1
    if ord('A') <= value <= ord('Z'):
        return value - ord('A') + 27
    raise RuntimeError("Invalid value")


score1 = 0
score2 = 0
overlap2 = set()
for i, d in enumerate(data):

    # Part 1
    packSize = len(d) // 2
    firstHalf = set(d[:packSize])
    secondHalf = set(d[packSize:])
    overlap1 = firstHalf.intersection(secondHalf)
    assert(len(overlap1) == 1)
    item1 = overlap1.pop()
    score1 += score_item(item1)

    # Part 2
    if i % 3 == 0:
        overlap2 = set(d)
    else:
        overlap2 = overlap2.intersection(set(d))
        if i % 3 == 2:
            assert(len(overlap2) == 1)
            item2 = overlap2.pop()
            score2 += score_item(item2)

print(f"Solution 1: {score1}")
print(f"Solution 2: {score2}")