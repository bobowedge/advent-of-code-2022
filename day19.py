import re

bpt_pattern = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. "
                         r"Each clay robot costs (\d+) ore. "
                         r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
                         r"Each geode robot costs (\d+) ore and (\d+) obsidian.")


def parse_blueprint(blueprint: str):
    '''Parse blueprint string into list'''
    match = bpt_pattern.match(blueprint)
    return [int(match.group(i)) for i in range(1, 8)]


def init_state():
    '''Initial factory state'''
    return tuple([0, 1, 0, 0, 0, 0, 0, 0, 0])


def advance(s, m: int):
    '''Advance state s by m minutes'''
    return [s[0] + m*s[1], s[1], s[2] + m*s[3], s[3], s[4] + m*s[5], s[5], s[6] + m*s[7], s[7], s[8] + m]


def next_robot(state, ore_cost, clay_cost, obsidian_cost, robot_index, max_minutes, max_geodes):
    '''Get the state after completing the next robot'''
    # First, optimize out some states that aren't worth continuing to score
    # If there are no robots building the right resources for the given robot, stop with this state
    if (ore_cost > 0 and state[1] == 0) or (clay_cost > 0 and state[3] == 0) or (obsidian_cost > 0 and state[5] == 0):
        return None
    # If there are enough robots building each resource needed per turn, don't bother building another one
    if ore_cost < state[1] and clay_cost < state[3] and obsidian_cost < state[5]:
        return None
    # Find the time needed to gather enough resources for this robot
    minutes = [0, 0, 0]
    if state[0] < ore_cost:
        minutes[0] = (ore_cost - state[0] + state[1] - 1) // state[1]
    if state[2] < clay_cost:
        minutes[1] = (clay_cost - state[2] + state[3] - 1) // state[3]
    if state[4] < obsidian_cost:
        minutes[2] = (obsidian_cost - state[4] + state[5] - 1) // state[5]
    minutes = max(minutes)
    # If passed the end of given time, no need to score
    if state[8] + minutes + 1 >= max_minutes:
        return None

    # new_state is after building this robot
    new_state = advance(state, minutes + 1)
    new_state[0] -= ore_cost
    new_state[2] -= clay_cost
    new_state[4] -= obsidian_cost
    new_state[robot_index] += 1

    # If building geode robots every turn still isn't enough to reach current max, don't keep this state
    time_left = max_minutes - new_state[8]
    ideal_geodes_left = (time_left - 1) * time_left // 2
    max_possible_geodes = new_state[6] + (time_left + 1) * new_state[7] + ideal_geodes_left
    if max_possible_geodes <= max_geodes:
        return None

    return tuple(new_state)


def score_blueprint(bpt: list, max_minutes: int):
    max_geodes = 0
    states = set()
    states.add(init_state())
    counter = 0
    while len(states) > 0:
        state = states.pop()

        # Fast-forward in time until the next robot of each type can be built
        # Next robot is ore robot
        new_state = next_robot(state, bpt[1], 0, 0, 1, max_minutes, max_geodes)
        if new_state is not None:
            states.add(new_state)

        # Next robot is clay robot
        new_state = next_robot(state, bpt[2], 0, 0, 3, max_minutes, max_geodes)
        if new_state is not None:
            states.add(new_state)

        # Next robot is obsidian robot
        new_state = next_robot(state, bpt[3], bpt[4], 0, 5, max_minutes, max_geodes)
        if new_state is not None:
            states.add(new_state)

        # Next robot is geode robot
        new_state = next_robot(state, bpt[5], 0, bpt[6], 7, max_minutes, max_geodes)
        if new_state is not None:
            geodes = new_state[6] + new_state[7] * (max_minutes - new_state[8])
            max_geodes = max(max_geodes, geodes)
            states.add(new_state)
        counter += 1
    return max_geodes


def solution1(data):
    total_score = 0
    for blueprint in data:
        bpt = parse_blueprint(blueprint)
        total_score += bpt[0] * score_blueprint(bpt, 24)
    return total_score


def solution2(data):
    total_score = 1
    for blueprint in data[:3]:
        bpt = parse_blueprint(blueprint)
        total_score *= score_blueprint(bpt, 32)
    return total_score


data = open("data/day19.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
