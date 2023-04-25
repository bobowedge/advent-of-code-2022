def dec2snafu(v: int):
    s = []
    while v > 0:
        x = v % 5
        if x == 4:
            s.append("-")
            v += 1
        elif x == 3:
            s.append("=")
            v += 2
        else:
            s.append(str(x))
            v -= x
        v //= 5
    s.reverse()
    return "".join(s)


def snafu2dec(s: str):
    if len(s) == 1:
        if s == "=":
            return -2
        if s == "-":
            return -1
        return int(s)
    v = 0
    s = list(s)
    s.reverse()
    for i, c in enumerate(s):
        vc = snafu2dec(c) * (5 ** i)
        v += vc
    return v


def solution1(data):
    fuel = 0
    for line in data.splitlines():
        fuel += snafu2dec(line)
    return dec2snafu(fuel)


data = open("data/day25.txt").read()
# data = '''1=-0-2
# 12111
# 2=0=
# 21
# 2=01
# 111
# 20012
# 112
# 1=-1=
# 1-12
# 12
# 1=
# 122'''
print(f"Solution 1: {solution1(data)}")
