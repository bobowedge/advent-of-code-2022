import re


def manhattan(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def parse_data(data):
    sensors = {}
    beacons = set()
    for line in data:
        match = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        sensor = (int(match.group(1)), int(match.group(2)))
        beacon = (int(match.group(3)), int(match.group(4)))
        sensors[sensor] = manhattan(sensor, beacon)
        beacons.add(beacon)
    return sensors, beacons


def solution1(data, y = 2000000):
    sensors, beacons = parse_data(data)
    xmin = None
    xmax = None
    for sensor in sensors:
        if xmin is None or xmin > sensor[0]:
            xmin = sensor[0]
        if xmax is None or xmax < sensor[0]:
            xmax = sensor[0]

    bad_positions = 0
    for x in range(xmin, xmax + 1):
        test_beacon = (x, y)
        if test_beacon in sensors or test_beacon in beacons:
            continue
        for sensor, d in sensors.items():
            test_d = manhattan(sensor, test_beacon)
            if test_d <= d:
                bad_positions += 1
                break
    x = xmin
    flag = True
    while flag:
        x -= 1
        test_beacon = (x, y)
        flag = False
        for sensor, d in sensors.items():
            test_d = manhattan(sensor, test_beacon)
            if test_d <= d:
                bad_positions += 1
                flag = True
                break
    x = xmax
    flag = True
    while flag:
        x += 1
        test_beacon = (x, y)
        flag = False
        for sensor, d in sensors.items():
            test_d = manhattan(sensor, test_beacon)
            if test_d <= d:
                bad_positions += 1
                flag = True
                break
    return bad_positions


def solution2(data):
    sensors, beacons = parse_data(data)

    for y in range(0, 4000000):
        x = 0
        while x < 4000001:
            prevx = x
            for sensor, distance in sensors.items():
                testb0 = (x, y)
                xd0 = manhattan(sensor, testb0)
                if xd0 > distance:
                    continue
                x1 = x + 1
                testb1 = (x1, y)
                xd1 = manhattan(sensor, testb1)
                if xd1 > xd0:
                    x += distance - xd0 + 1
                else:
                    x = sensor[0] + (distance - abs(sensor[1]-y)) + 1
                if x >= 4000001:
                    break
            if x == prevx:
                return 4000000 * x + y
    return 0


def solution2_test(data):
    sensors, beacons = parse_data(data)

    for y in range(0, 20):
        x = 0
        while x < 21:
            prevx = x
            for sensor, distance in sensors.items():
                testb0 = (x, y)
                xd0 = manhattan(sensor, testb0)
                if y == 11:
                    print(x, sensor, xd0, distance)
                if xd0 > distance:
                    continue
                x1 = x + 1
                testb1 = (x1, y)
                xd1 = manhattan(sensor, testb1)
                if xd1 > xd0:
                    x += distance - xd0 + 1
                else:
                    x = sensor[0] + (distance - abs(sensor[1]-y)) + 1
                if x >= 21:
                    break
            if x == prevx:
                return 4000000 * x + y
    return 0


data = open("data/day15.txt").read().splitlines()
# data = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3'''.splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
