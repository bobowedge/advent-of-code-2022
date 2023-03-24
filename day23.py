def parse_data(data):
    elf_locations = set()
    for row, string in enumerate(data):
        for col, char in enumerate(list(string)):
            if char == '#':
                elf_locations.add((row, col))
    return elf_locations


def print_elves(elf_locations):
    x, y = elf_locations.pop()
    minx, maxx, miny, maxy = [x, x, y, y]
    elf_locations.add((x, y))
    for x, y in elf_locations:
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)

    print("---------------")
    for x in range(minx, maxx+1):
        line = []
        for y in range(miny, maxy+1):
            if (x, y) in elf_locations:
                line.append('#')
            else:
                line.append('.')
        line = "".join(line)
        print('-', line)
    print("---------------")


def count_neighbors(elf, elf_locations):
    neighbors = set()
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x != 0 or y != 0:
                neighbors.add((elf[0] + x, elf[1] + y))
    neighbors = elf_locations.intersection(neighbors)
    return len(neighbors)


def solution1(data):
    elf_locations = parse_data(data)
    direction_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    direction_map = {}
    for d in direction_list:
        if d[0] == 0:
            direction_map[d] = [(x, d[1]) for x in [-1, 0, 1]]
        else:
            direction_map[d] = [(d[0], x) for x in [-1, 0, 1]]
    # print_elves(elf_locations)
    for _ in range(10):
        new_elf_locations = set()
        loc_map = {}
        for elf in elf_locations:
            if count_neighbors(elf, elf_locations) == 0:
                new_elf_locations.add(elf)
                continue
            moved_flag = False
            for d in direction_list:
                if d[0] == 0:
                    locs = set([(elf[0] + x, elf[1] + d[1]) for x in [-1, 0, 1]])
                else:
                    locs = set([(elf[0] + d[0], elf[1] + x) for x in [-1, 0, 1]])
                overlap = locs.intersection(elf_locations)
                if len(overlap) == 0:
                    moved_elf = (elf[0] + d[0], elf[1] + d[1])
                    if moved_elf in loc_map:
                        new_elf_locations.add(elf)
                        new_elf_locations.remove(moved_elf)
                        new_elf_locations.add(loc_map[moved_elf])
                    else:
                        new_elf_locations.add(moved_elf)
                    loc_map[moved_elf] = elf
                    moved_flag = True
                    break
            if not moved_flag:
                new_elf_locations.add(elf)
        elf_locations = new_elf_locations
        # print_elves(elf_locations)
        direction_list = direction_list[1:] + direction_list[0:1]

    x, y = elf_locations.pop()
    minx, maxx, miny, maxy = [x, x, y, y]
    for x, y in elf_locations:
        minx = min(minx, x)
        maxx = max(maxx, x+1)
        miny = min(miny, y)
        maxy = max(maxy, y+1)
    return (maxx-minx) * (maxy-miny) - (len(elf_locations) + 1)


def solution2(data):
    elf_locations = parse_data(data)
    direction_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    direction_map = {}
    for d in direction_list:
        if d[0] == 0:
            direction_map[d] = [(x, d[1]) for x in [-1, 0, 1]]
        else:
            direction_map[d] = [(d[0], x) for x in [-1, 0, 1]]
    move_round = 0
    global_move_flag = True
    while global_move_flag:
        global_move_flag = False
        move_round += 1
        new_elf_locations = set()
        loc_map = {}
        for elf in elf_locations:
            if count_neighbors(elf, elf_locations) == 0:
                new_elf_locations.add(elf)
                continue
            moved_flag = False
            for d in direction_list:
                if d[0] == 0:
                    locs = set([(elf[0] + x, elf[1] + d[1]) for x in [-1, 0, 1]])
                else:
                    locs = set([(elf[0] + d[0], elf[1] + x) for x in [-1, 0, 1]])
                overlap = locs.intersection(elf_locations)
                if len(overlap) == 0:
                    moved_elf = (elf[0] + d[0], elf[1] + d[1])
                    if moved_elf in loc_map:
                        new_elf_locations.add(elf)
                        new_elf_locations.remove(moved_elf)
                        new_elf_locations.add(loc_map[moved_elf])
                    else:
                        new_elf_locations.add(moved_elf)
                    loc_map[moved_elf] = elf
                    moved_flag = True
                    global_move_flag = True
                    break
            if not moved_flag:
                new_elf_locations.add(elf)
        elf_locations = new_elf_locations
        # print_elves(elf_locations)
        direction_list = direction_list[1:] + direction_list[0:1]
    return move_round


data = open("data/day23.txt").read().splitlines()
# data = '''....#..
# ..###.#
# #...#.#
# .#...##
# #.###..
# ##.#.##
# .#..#..'''.splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
