def mix_round(data, indicer, scale=1):
    for pos in range(len(data)):
        idx = indicer.index(pos)
        val = data.pop(idx)
        indicer.pop(idx)
        new_idx = (idx + val * scale) % len(data)
        data.insert(new_idx, val)
        indicer.insert(new_idx, pos)


def coordinate_sum(data):
    idx0 = data.index(0)
    idx1 = (idx0 + 1000) % len(data)
    idx2 = (idx0 + 2000) % len(data)
    idx3 = (idx0 + 3000) % len(data)
    return data[idx1] + data[idx2] + data[idx3]


def solution1(data: list):
    indicer = [i for i in range(len(data))]
    mix_round(data, indicer)
    return coordinate_sum(data)


def solution2(data: list, scale=811589153):
    indicer = [i for i in range(len(data))]
    for _ in range(10):
        mix_round(data, indicer, scale)
    return scale * coordinate_sum(data)


data = open('data/day20.txt').read().splitlines()
data = [int(x) for x in data]
data2 = list(data)
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data2)}")

