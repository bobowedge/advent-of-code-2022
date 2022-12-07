import re


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.contents = {}

    def size(self):
        return sum([v.size() for v in self.contents.values()])

    def print(self, tabs=0):
        print("  " * tabs, end="")
        print(f"{self.name}")
        for x in self.contents.values():
            x.print(tabs+1)

    def is_dir(self):
        return True


class File:
    def __init__(self, name, size):
        self.name = name
        self.length = size

    def size(self):
        return self.length

    def print(self, tabs=0):
        print("  "*tabs, end="")
        print(f"{self.name} (size={self.length})")

    def solution1(self):
        return self.size

    def is_dir(self):
        return False


def get_directory_structure(data):
    data.reverse()
    dummy = data.pop()
    root = Dir('/', None)
    cwd = root
    while len(data) > 0:
        line = data.pop()
        match = re.match(r'\$ cd (\S+)', line)
        if match:
            newdir = match.group(1)
            if newdir == '..':
                cwd = cwd.parent
            elif newdir in cwd.contents:
                cwd = cwd.contents[newdir]
            else:
                raise RuntimeError(f"Unknown child: {newdir}")
            continue
        else:
            match = re.match(r'\$ ls', line)
            if match:
                while len(data) > 0 and data[-1][0] != '$':
                    line = data.pop()
                    match = re.match(r'dir (\S+)', line)
                    if match:
                        newdir = match.group(1)
                        cwd.contents[newdir] = Dir(newdir, cwd)
                        continue
                    else:
                        match = re.match(r'(\d+) (\S+)', line)
                        if match:
                            newfile = match.group(2)
                            size = int(match.group(1))
                            cwd.contents[newfile] = File(newfile, size)
                        else:
                            raise RuntimeError(f"Unknown filetype: {line}")
            else:
                raise RuntimeError(f"Unknown command: {line}")
    return root


def solution1(d):
    if not d.is_dir():
        return 0
    total_size = 0
    s = 0
    for x in d.contents.values():
        total_size += solution1(x)
        s += x.size()
    if s > 100000:
        return total_size
    else:
        return total_size + s


def solution2(d):
    total_size = d.size()
    max_size = 40000000
    diff = total_size - max_size
    if diff < 0:
        return 0

    def find_smallest_dir(d):
        if not d.is_dir():
            return total_size
        y = d.size()
        if y < diff:
            return total_size
        for x in d.contents.values():
            z = find_smallest_dir(x)
            y = min(y, z)
        return y

    return find_smallest_dir(d)


data = open('data/day07.txt').read().splitlines()

root = get_directory_structure(data)

print(f"Solution 1: {solution1(root)}")
print(f"Solution 2: {solution2(root)}")



