def is_visible(index, data, size=99):
    row = index // size
    col = index % size
    if row == 0 or col == 0 or row == (size - 1) or col == (size - 1):
        return 1
    value = data[index]
    if (value > max(data[row * size:index]) or value > max(data[index + 1:(row + 1) * size]) or
            value > max(data[col:index:size]) or value > max(data[index + size::size])):
        return 1
    return 0


def scenic_score(index, data, size=99):
    row = index // size
    col = index % size
    if row == 0 or col == 0 or row == (size - 1) or col == (size - 1):
        return 0

    value = data[index]

    def score(d):
        for i, tree in enumerate(d):
            if tree >= value:
                return i + 1
        return len(d)

    return (score(data[index - 1:row * size - 1:-1]) *
            score(data[index + 1:(row + 1) * size]) *
            score(data[index - size::-size]) *
            score(data[index + size::size]))


data = open("data/day08.txt").read()
data = data.replace('\n', '')
data = [int(x) for x in list(data)]

solution1 = sum([is_visible(index, data) for index in range(len(data))])
print(f"Solution1: {solution1}")

solution2 = max([scenic_score(index, data) for index in range(len(data))])
print(f"Solution2: {solution2}")
