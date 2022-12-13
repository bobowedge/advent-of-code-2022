def parse_data(data):
    new_data = []
    start = None
    end = None
    for row, line in enumerate(data):
        line = [ord(x) for x in list(line)]
        if 83 in line:
            col = line.index(83)
            start = (row, col)
            line[col] = 97
        if 69 in line:
            col = line.index(69)
            end = (row, col)
            line[col] = 122
        new_data.append(line)
    return start, end, new_data


def get_nodes1(data):
    nodes = set()
    distances = {}
    for x in range(len(data)):
        for y in range(len(data[x])):
            nodes.add((x, y))
            m = {}
            val = data[x][y] + 1
            if y > 0 and data[x][y-1] <= val:
                m[(x, y-1)] = 1
            if y < len(data[x]) - 1 and data[x][y+1] <= val:
                m[(x, y+1)] = 1
            if x > 0 and data[x-1][y] <= val:
                m[(x-1, y)] = 1
            if x < len(data) - 1 and data[x+1][y] <= val:
                m[(x+1, y)] = 1
            distances[(x, y)] = m
    return nodes, distances


def solution1(data, start, end):
    nodes, distances = get_nodes1(data)
    unvisited = {node: None for node in nodes}
    visited = {}
    current = start
    currentDistance = 0
    unvisited[current] = currentDistance

    while True:
        for neighbor, distance in distances[current].items():
            if neighbor not in unvisited:
                continue
            newDistance = currentDistance + distance
            if unvisited[neighbor] is None or unvisited[neighbor] > newDistance:
                unvisited[neighbor] = newDistance
        visited[current] = currentDistance
        if current == end:
            break
        del unvisited[current]
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key=lambda x: x[1])[0]

    return visited[end]


def get_nodes2(data):
    nodes = set()
    distances = {}
    for x in range(len(data)):
        for y in range(len(data[x])):
            nodes.add((x, y))
            m = {}
            val = data[x][y] - 1
            if y > 0 and data[x][y-1] >= val:
                m[(x, y-1)] = 1
            if y < len(data[x]) - 1 and data[x][y+1] >= val:
                m[(x, y+1)] = 1
            if x > 0 and data[x-1][y] >= val:
                m[(x-1, y)] = 1
            if x < len(data) - 1 and data[x+1][y] >= val:
                m[(x+1, y)] = 1
            distances[(x, y)] = m
    return nodes, distances


def solution2(data, start, end):
    nodes, distances = get_nodes2(data)
    unvisited = {node: None for node in nodes}
    visited = {}
    current = end
    currentDistance = 0
    unvisited[current] = currentDistance

    while True:
        for neighbor, distance in distances[current].items():
            if neighbor not in unvisited:
                continue
            newDistance = currentDistance + distance
            if unvisited[neighbor] is None or unvisited[neighbor] > newDistance:
                unvisited[neighbor] = newDistance
        visited[current] = currentDistance
        del unvisited[current]
        candidates = [node for node in unvisited.items() if node[1]]
        if len(candidates) == 0:
            break
        current, currentDistance = sorted(candidates, key=lambda x: x[1])[0]

    best = visited[start]
    for row, r in enumerate(data):
        for col, c in enumerate(r):
            if c == 97 and (row, col) in visited:
                best = min(visited[(row, col)], best)
    return best


data = open("data/day12.txt").read().splitlines()
start, end, data = parse_data(data)

print(f"Solution1: {solution1(data, start, end)}")
print(f"Solution2: {solution2(data, start, end)}")
