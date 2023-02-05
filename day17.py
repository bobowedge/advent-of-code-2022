ROCK_TYPES = [[(0, 30), (1,  0), (2,  0), (3,  0)],  # minus shape
          [(0,  8), (1, 28), (2,  8), (3,  0)],  # cross
          [(0, 28), (1,  4), (2,  4), (3,  0)],  # backwards L
          [(0, 16), (1, 16), (2, 16), (3, 16)],  # vertical line
          [(0, 24), (1, 24), (2,  0), (3,  0)]]  # square


def blow_rock_step(rock, direction, filled_spots: list):
    if direction == '<':
        direction = -1
    else:
        direction = 1
    new_rock = []
    for (y, value) in rock:
        if (value >= 64 and direction == -1) or (value & 1 and direction == 1):
            return rock
        if y < len(filled_spots):
            filled = filled_spots[y]
        else:
            filled = 0
        if direction == -1:
            new_value = value << 1
        else:
            new_value = value >> 1
        if new_value & filled:
            return rock
        new_rock.append((y, new_value))
    return new_rock


def down_rock_step(rock, filled_spots: list):
    new_rock = []
    for (y, value) in rock:
        new_y = y - 1
        if new_y < len(filled_spots):
            filled = filled_spots[new_y]
            if filled & value:
                return rock, True
        new_rock.append((new_y, value))
    return new_rock, False


def draw_cavern(rock, filled_spots: list, top, bottom=0):
    for y in range(top, bottom-1, -1):
        if y < len(filled_spots):
            filled = filled_spots[y]
        else:
            filled = 0
        if y == 0:
            print('+-------+')
            continue
        else:
            print('|', end='')
            for x in range(7):
                if filled & 2**(6-x):
                    print('#', end='')
                else:
                    rock_flag = False
                    for (py, value) in rock:
                        if py == y and value & 2**(6-x):
                            rock_flag = True
                    if rock_flag:
                        print("@", end='')
                    else:
                        print(".", end='')
            print('|')
    print()


def drop_rock(rock_type, filled_spots, data, time):
    top = len(filled_spots)
    rock = [(y+top+3, value) for (y, value) in rock_type]
    stop_flag = False
    while not stop_flag:
        direction = data[time % len(data)]
        time += 1
        rock = blow_rock_step(rock, direction, filled_spots)
        rock, stop_flag = down_rock_step(rock, filled_spots)
    return rock, time


def drop_rocks(filled_spots, time, start_rock, num_rocks):
    end_rock = start_rock + num_rocks
    lentypes = len(ROCK_TYPES)
    for r in range(start_rock, end_rock):
        rock_type = ROCK_TYPES[r % lentypes]
        rock, time = drop_rock(rock_type, filled_spots, data, time)
        for (y, value) in rock:
            if value == 0:
                continue
            if y < len(filled_spots):
                filled_spots[y] = filled_spots[y] | value
            elif y == len(filled_spots):
                filled_spots.append(value)
            else:
                assert False
    return filled_spots, time


def solution1(data):
    filled_spots = [127]
    time = 0
    filled_spots, _ = drop_rocks(filled_spots, time, 0, 2022)
    return len(filled_spots) - 1


def solution2(data):
    floors = [0, 0, 0, 0, 0, 0, 0]
    filled_spots = [127]
    time = 0
    rock_num = 0
    hashMap = dict()
    heights = dict()
    lendata = len(data)
    lentypes = len(ROCK_TYPES)

    cycle_found = False
    while not cycle_found and rock_num < 1000000:
        rock_type = ROCK_TYPES[rock_num % lentypes]
        rock, time = drop_rock(rock_type, filled_spots, data, time)
        for (y, value) in rock:
            if value == 0:
                continue
            if y < len(filled_spots):
                filled_spots[y] = filled_spots[y] | value
            elif y == len(filled_spots):
                filled_spots.append(value)
            else:
                assert False
            for i in range(7):
                if value & 2**i:
                    floors[i] = max(floors[i], y)

        hash_rock = [f - min(floors) for f in floors]
        hash_rock.append(rock_num % 5)
        hash_rock.append(time % lendata)
        hash_rock = tuple(hash_rock)
        if hash_rock in hashMap.values():
            cycle_found = True
        hashMap[rock_num] = hash_rock
        heights[rock_num] = len(filled_spots) - 1
        rock_num += 1

    if rock_num == 1000000:
        print("FAIL")
        return 0

    end_cycle_pn = rock_num - 1
    end_ht = heights[end_cycle_pn]
    end_hp = hashMap[end_cycle_pn]

    for rock_num, hp in hashMap.items():
        if hp == end_hp and rock_num != end_cycle_pn:
            start_cycle_pn = rock_num
            start_ht = heights[start_cycle_pn]
            break

    cycle_length = end_cycle_pn - start_cycle_pn
    cycle_ht = end_ht - start_ht

    FINAL_PIECE = 1000000000000

    num_cycles = (FINAL_PIECE - start_cycle_pn) // cycle_length
    remaining_rocks = FINAL_PIECE - start_cycle_pn - num_cycles * cycle_length

    drop_rocks(filled_spots, time, end_cycle_pn + 1, remaining_rocks)
    new_ht = len(filled_spots) - 1
    total_height = start_ht + num_cycles * cycle_ht + (new_ht - end_ht)
    return total_height


data = open('data/day17.txt').read()
data = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
data = list(data)

print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")



