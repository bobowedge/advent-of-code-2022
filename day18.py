DELTAS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


def solution1(data):
    cubes = dict()
    for line in data:
        pt = tuple([int(w) for w in line.split(",")])
        sides = 6
        for delta in DELTAS:
            new_pt = tuple([pt[i] + delta[i] for i in range(3)])
            if new_pt in cubes:
                sides -= 1
                cubes[new_pt] -= 1
        cubes[pt] = sides
    return sum(cubes.values())


def DFS(v, visited, component, neighbors):
    '''Depth-First Search'''
    # Add to the visited set
    visited.add(v)
    # Add to the set for this component
    component.add(v)

    # Find all of the valid edges
    for delta in DELTAS:
        new_pt = tuple([v[i] + delta[i] for i in range(3)])
        if new_pt in visited:
            continue
        if new_pt in neighbors:
            DFS(new_pt, visited, component, neighbors)
        else:
            for delta2 in DELTAS:
                new_pt2 = tuple([new_pt[i] + delta2[i] for i in range(3)])
                if new_pt2 not in visited and new_pt2 in neighbors:
                    DFS(new_pt2, visited, component, neighbors)


def solution2(data):
    cubes = set()
    neighbors = set()

    # Find all the cubes and their neighbors
    for line in data:
        pt = tuple([int(w) for w in line.split(",")])
        cubes.add(pt)
        for delta in DELTAS:
            neighbor = tuple([pt[i] + delta[i] for i in range(3)])
            neighbors.add(neighbor)

    # Split the neighbors into components
    neighbors = neighbors - cubes
    visited = set(cubes)
    components = []
    component = set()
    for n in neighbors:
        if n in visited:
            continue
        DFS(n, visited, component, neighbors)
        components.append(set(component))
        component = set()

    # Largest component is the outside
    component_sizes = [len(c) for c in components]
    largest_size = max(component_sizes)
    oidx = component_sizes.index(largest_size)
    outside = components[oidx]

    result = 0
    for pt in cubes:
        for delta in DELTAS:
            new_pt = tuple([pt[i] + delta[i] for i in range(3)])
            if new_pt in outside:
                result += 1
    return result


data = open("data/day18.txt").read().splitlines()
print(f"Solution 1:{solution1(data)}")
print(f"Solution 2:{solution2(data)}")
