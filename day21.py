import re


def parse_data(data):
    datamap = {}
    for line in data:
        match = re.match(r"(\S{4}):\s+(\S{4}) (.) (\S{4})", line)
        if match is not None:
            datamap[match.group(1)] = (match.group(3), match.group(2), match.group(4))
        else:
            match = re.match(r"(\S{4}):\s+(\d+)", line)
            datamap[match.group(1)] = int(match.group(2))
    return datamap


def calculate1(k, d):
    v = d[k]
    if type(v) == int:
        return v
    v1 = calculate1(v[1], d)
    v2 = calculate1(v[2], d)
    if v[0] == '+':
        return v1 + v2
    elif v[0] == '*':
        return v1 * v2
    elif v[0] == '-':
        return v1 - v2
    elif v[0] == '/':
        return v1 // v2
    assert False


def solution1(data):
    datamap = parse_data(data)
    return calculate1('root', datamap)


def calculate2(k, d, newd):
    if k not in d:
        return None
    v = d[k]
    if type(v) == int:
        newd[k] = v
        return v
    v1 = calculate2(v[1], d, newd)
    v2 = calculate2(v[2], d, newd)
    if v1 is None or v2 is None:
        return None
    if v[0] == '+' :
        newd[k] = v1 + v2
        return v1 + v2
    elif v[0] == '*':
        newd[k] = v1 * v2
        return v1 * v2
    elif v[0] == '-':
        newd[k] = v1 - v2
        return v1 - v2
    elif v[0] == '/':
        newd[k] = v1 // v2
        return v1 // v2
    return None


def reverse(k, dint, dvar):
    # Existing string operation for k
    op, lk, rk = dvar[k]

    # If k is root, op is '=' and dint[lk] = dint[rk]
    if k == 'root':
        dint[k] = 0
        if lk in dint:
            dint[rk] = dint[lk]
            return rk
        else:
            dint[lk] = dint[rk]
            return lk

    # Otherwise, dint[k] exists and need to calculate either dint[lk] or dint[rk] from it
    vk = dint[k]
    if lk in dint:
        vlk = dint[lk]
        if op == '+':
            # vk = vlk + vrk
            # vrk = vk - vlk
            dint[rk] = vk - vlk
        elif op == '-':
            # vk = vlk - vrk
            # vrk = vlk - vk
            dint[rk] = vlk - vk
        elif op == '*':
            # vk = vlk * vrk
            # vrk = vk // vlk
            dint[rk] = vk // vlk
        else:
            # vk = vlk // vrk
            # vrk = vlk // vlk
            dint[rk] = vlk // vlk
        return rk
    if rk in dint:
        vrk = dint[rk]
        if op == '+':
            # vk = vlk + vrk
            # vlk = vk - vrk
            dint[lk] = vk - vrk
        elif op == '-':
            # vk = vlk - vrk
            # vlk = vk + vrk
            dint[lk] = vk + vrk
        elif op == '*':
            # vk = vlk * vrk
            # vlk = vk // vrk
            dint[lk] = vk // vrk
        else:
            # vk = vlk // vrk
            # vlk = vk * vrk
            dint[lk] = vk * vrk
        return lk
    assert False


def solution2(data):
    datamap = parse_data(data)
    del datamap['humn']

    # Split the map into integer parts (dint) and variable parts (dvar)
    dint = {}
    for k in datamap.keys():
        if k not in dint:
            calculate2(k, datamap, dint)
    dvar = {}
    for k in datamap.keys():
        if k not in dint.keys():
            dvar[k] = datamap[k]

    # Starting with root, reverse dvar until humn is reached
    k = 'root'
    while k != 'humn':
        k = reverse(k, dint, dvar)
    return dint['humn']


data = open("data/day21.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
