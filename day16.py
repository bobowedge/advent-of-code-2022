import re
import itertools


def parse_data(data):
    pressures = {}
    tunnels = {}
    valves = []
    for line in data:
        match = re.match(r"Valve (\S+) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
        valve = match.group(1)
        pressure = int(match.group(2))
        output_valves = match.group(3).split(", ")
        if pressure > 0:
            pressures[valve] = pressure
        tunnels[valve] = output_valves
        if valve not in valves:
            valves.append(valve)
    return pressures, tunnels, valves


def keep_state(new_state, states, equal=False):
    if equal and new_state in states:
        return True
    for state in states:
        if state[0] >= new_state[0] and state[1] <= new_state[1] and state[3].issubset(new_state[3]):
            return False
    return True


def solution1_old(data):
    pressures, tunnels, _ = parse_data(data)
    # total pressure, minutes elapsed, location, open valves
    init_state = (0, 0, 'AA', set())
    states = [init_state]
    best_states = {'AA': [init_state]}
    best_pressure = 0
    while len(states) > 0:
        total_pressure, elapsed_time, location, open_valves = states.pop()
        elapsed_time += 1
        if elapsed_time == 30 or len(open_valves) == len(pressures):
            continue
        for new_valve in tunnels[location]:
            new_state = (total_pressure, elapsed_time, new_valve, set(open_valves))
            bs = best_states.get(new_valve, [])
            if keep_state(new_state, bs):
                states.append(new_state)
                bs.append(new_state)
                best_states[new_valve] = bs
        if location in pressures and location not in open_valves:
            total_pressure += pressures[location] * (30 - elapsed_time)
            open_valves = set(open_valves)
            open_valves.add(location)
            new_state = (total_pressure, elapsed_time, location, open_valves)
            bs = best_states.get(location, [])
            if keep_state(new_state, bs):
                states.append(new_state)
                bs.append(new_state)
                best_states[location] = bs
            if total_pressure > best_pressure:
                best_pressure = total_pressure
        states.sort()
    return best_pressure


def floyd_warshall(valves, tunnels):
    len_valves = len(valves)
    dmatrix = [[40 for _ in range(len_valves)] for _ in range(len_valves)]
    for vertex, edges in tunnels.items():
        idx1 = valves.index(vertex)
        dmatrix[idx1][idx1] = 0
        for edge in edges:
            idx2 = valves.index(edge)
            dmatrix[idx1][idx2] = 1
    for k in range(len_valves):
        for i in range(len_valves):
            for j in range(len_valves):
                if dmatrix[i][j] > dmatrix[i][k] + dmatrix[k][j]:
                    dmatrix[i][j] = dmatrix[i][k] + dmatrix[k][j]
    return dmatrix


def find_best_pressure(pressures, valves, dmatrix, init_state, unbroken_valves):
    states = [init_state]
    best_pressure = 0
    while len(states) > 0:
        total_pressure, elapsed_time, current_valve, open_valves = states.pop()
        unvisited_valves = unbroken_valves.symmetric_difference(open_valves)
        for new_valve in unvisited_valves:
            dist = dmatrix[current_valve][new_valve]
            new_elapsed_time = elapsed_time + dist + 1
            if new_elapsed_time < 30:
                new_total_pressure = total_pressure + (30 - new_elapsed_time) * pressures[valves[new_valve]]
                new_open_valves = set(open_valves)
                new_open_valves.add(new_valve)
                new_state = new_total_pressure, new_elapsed_time, new_valve, new_open_valves
                states.append(new_state)
                if new_total_pressure > best_pressure:
                    best_pressure = new_total_pressure
    return best_pressure


def solution1(data):
    pressures, tunnels, valves = parse_data(data)
    valves = list(tunnels.keys())
    valves.sort()

    # Floyd-Warshall on valves (find shortest path between pair of valves)
    dmatrix = floyd_warshall(valves, tunnels)

    # total pressure, minutes elapsed, location, open valves
    init_state = (0, 0, 0, set())
    unbroken_valves = set([valves.index(v) for v in pressures.keys()])
    return find_best_pressure(pressures, valves, dmatrix, init_state, unbroken_valves)


def calc_pressure_map(pressures, valves, dmatrix, init_state, unbroken_valves):
    states = [init_state]
    best_pressure_map = {}
    while len(states) > 0:
        total_pressure, elapsed_time, current_valve, open_valves = states.pop()
        unvisited_valves = unbroken_valves.symmetric_difference(open_valves)
        for new_valve in unvisited_valves:
            dist = dmatrix[current_valve][new_valve]
            new_elapsed_time = elapsed_time + dist + 1
            if new_elapsed_time < 30:
                new_total_pressure = total_pressure + (30 - new_elapsed_time) * pressures[valves[new_valve]]
                new_open_valves = set(open_valves)
                new_open_valves.add(new_valve)
                new_state = new_total_pressure, new_elapsed_time, new_valve, new_open_valves
                states.append(new_state)
                key = frozenset(new_open_valves)
                bp = best_pressure_map.get(key, 0)
                if new_total_pressure > bp:
                    best_pressure_map[key] = new_total_pressure
    return best_pressure_map


def solution2(data):
    pressures, tunnels, valves = parse_data(data)
    valves = list(tunnels.keys())
    valves.sort()

    # Floyd-Warshall on valves (find shortest path between pair of valves)
    dmatrix = floyd_warshall(valves, tunnels)

    init_state = (0, 4, 0, set())
    unbroken_valves = set([valves.index(v) for v in pressures.keys()])
    bp_map = calc_pressure_map(pressures, valves, dmatrix, init_state, unbroken_valves)

    best_pressure = 0
    for my_valves, myp in bp_map.items():
        for el_valves, elp in bp_map.items():
            if my_valves.isdisjoint(el_valves):
                best_pressure = max(best_pressure, myp + elp)
    return best_pressure


data = open("data/day16.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
