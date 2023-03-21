from queue import PriorityQueue

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def parse_directions(line: str):
    index = 0
    directions = []
    turns = []
    while index < len(line):
        try:
            lidx = line.index('L', index)
        except ValueError:
            lidx = len(line)
        try:
            ridx = line.index('R', index)
        except ValueError:
            ridx = len(line)
        if lidx < ridx:
            turns.append(-1)
            directions.append(line[index:lidx])
            index = lidx + 1
        else:
            turns.append(1)
            directions.append(line[index:ridx])
            index = ridx + 1
    turns[-1] = 0
    directions = [int(d) for d in directions]
    return directions, turns


def parse_row(line: str, row, face):
    for col, pt in enumerate(line):
        if pt == " ":
            continue
        if pt == ".":
            face[(row + 1, col + 1)] = 0
        else:
            face[(row + 1, col + 1)] = 1
    return


def parse_data1(data: list):
    directions = []
    turns = []
    maze = {}
    for row, line in enumerate(data):
        if 'L' in line or 'R' in line:
            directions, turns = parse_directions(line)
            break
        parse_row(line, row, maze)
    maxrow = 0
    maxcol = 0
    for (row, col) in maze:
        maxrow = max(maxrow, row + 1)
        maxcol = max(maxcol, col + 1)
    return maze, directions, turns, maxrow, maxcol


def step1(row, col, facing, maxrow, maxcol):
    if facing == 0:
        ncol = col + 1
        if ncol >= maxcol:
            ncol = 1
        return row, ncol
    if facing == 1:
        nrow = row + 1
        if nrow >= maxrow:
            nrow = 1
        return nrow, col
    if facing == 2:
        ncol = col - 1
        if ncol <= 0:
            ncol = maxcol - 1
        return row, ncol
    if facing == 3:
        nrow = row - 1
        if nrow <= 0:
            nrow = maxrow - 1
        return nrow, col


def solution1(data):
    maze, directions, turns, maxrow, maxcol = parse_data1(data)

    # Find starting position
    row, col, facing = (1, 1, 0)
    while maze.get((row, col), -1) != 0:
        col += 1
    for d, t in zip(directions, turns):
        for _ in range(d):
            nrow, ncol = step1(row, col, facing, maxrow, maxcol)
            while (nrow, ncol) not in maze:
                nrow, ncol = step1(nrow, ncol, facing, maxrow, maxcol)
            if maze[(nrow, ncol)] == 1:
                break
            row, col = nrow, ncol
        facing = (facing + t) % 4
    return 1000 * row + 4 * col + facing


def parse_data2(data: list, face_size=50):
    directions, turns = parse_directions(data[-1])

    # Find face locations and faces
    faces = {}
    for row in range(0, len(data[:-2]), face_size):
        for col in range(0, len(data[row]), face_size):
            if data[row][col] != " ":
                face = {}
                for r in range(face_size):
                    for c in range(face_size):
                        pt = data[row + r][col + c]
                        if pt == ".":
                            face[(r + 1, c + 1)] = 0
                        else:
                            face[(r + 1, c + 1)] = 1
                frow = row // face_size
                fcol = col // face_size
                faces[(frow, fcol)] = face
    return faces, directions, turns


def inv_dir(d: int):
    return (d + 2) % 4


def find_neighbors(faces: dict):
    def add(sq: tuple, d: int):
        return tuple((sq[0]+DIRECTIONS[d][0], sq[1]+DIRECTIONS[d][1]))

    def is_neighbor(sq1, sq2, neighbor_map):
        for d in range(4):
            sq3, _ = neighbor_map.get((sq1, d), (None, None))
            if sq2 == sq3:
                return True
        return False

    # Set bounds on path
    minx, maxx, miny, maxy = 0, 0, 0, 0
    for (x, y) in faces:
        if x <= minx:
            minx = x - 1
        if x >= maxx:
            maxx = x + 1
        if y <= miny:
            miny = y - 1
        if y >= maxy:
            maxy = y + 1

    pq = PriorityQueue()
    for face in faces.keys():
        for d in range(4):
            next_square = add(face, d)
            # Face, to direction, from direction, next square
            pq.put((0, face, d, d, next_square))

    neighbor_map = {}
    num_neighbors = {}
    while len(neighbor_map) < 24:
        priority, face, toDir, fromDir, pnbr = pq.get()
        # Have all neighbors
        if num_neighbors.get(face, 0) == 4:
            continue

        # Can't be your own neighbor
        if face == pnbr:
            continue

        # Found neighbor, maybe
        if pnbr in faces:
            if ((face, toDir) not in neighbor_map and
                    (pnbr, inv_dir(fromDir)) not in neighbor_map and
                    not is_neighbor(face, pnbr, neighbor_map)):
                neighbor_map[face, toDir] = (pnbr, inv_dir(fromDir))
                neighbor_map[pnbr, inv_dir(fromDir)] = (face, toDir)
                num_neighbors[face] = num_neighbors.get(face, 0) + 1
                num_neighbors[pnbr] = num_neighbors.get(pnbr, 0) + 1
            continue

        # Add more to queue to check
        for d in range(4):
            next_square = add(pnbr, d)
            if minx <= next_square[0] <= maxx and miny <= next_square[1] <= maxy:
                pq.put((priority+1, face, toDir, d, next_square))
    return neighbor_map


def cross_face(to_dir, from_dir, row, col, face_size):
    if from_dir == 0:
        ncol = face_size
    elif from_dir == 1:
        nrow = face_size
    elif from_dir == 2:
        ncol = 1
    else:
        nrow = 1
    if to_dir == 0:
        if from_dir == 0:
            nrow = face_size - (row - 1)
        elif from_dir == 1:
            ncol = row
        elif from_dir == 2:
            nrow = row
        else:
            ncol = face_size - (row - 1)
    elif to_dir == 1:
        if from_dir == 0:
            nrow = col
        elif from_dir == 1:
            ncol = face_size - (col - 1)
        elif from_dir == 2:
            nrow = face_size - (col - 1)
        else:
            ncol = col
    elif to_dir == 2:
        if from_dir == 0:
            nrow = row
        elif from_dir == 1:
            ncol = face_size - (row - 1)
        elif from_dir == 2:
            nrow = face_size - (row - 1)
        else:
            ncol = row
    else:
        if from_dir == 0:
            nrow = face_size - (col - 1)
        elif from_dir == 1:
            ncol = col
        elif from_dir == 2:
            nrow = col
        else:
            ncol = face_size - (col - 1)
    return nrow, ncol


def step2(row, col, facing, face, face_size, neighbor_map):
    nrow = row
    ncol = col
    if facing == 0:
        ncol = col + 1
    elif facing == 1:
        nrow = row + 1
    elif facing == 2:
        ncol = col - 1
    else:
        nrow = row - 1
    if 1 <= ncol <= face_size and 1 <= nrow <= face_size:
        return nrow, ncol, facing, face

    nface, nfacing = neighbor_map[face, facing]
    nrow, ncol = cross_face(facing, nfacing, nrow, ncol, face_size)
    return nrow, ncol, inv_dir(nfacing), nface


def solution2(data: list, face_size=50):
    faces, directions, turns = parse_data2(data, face_size)
    neighbor_map = find_neighbors(faces)

    # Getting starting face
    all_faces = list(faces.keys())
    all_faces.sort()
    face = all_faces[0]
    row, col, facing = (1, 1, 0)

    for d, t in zip(directions, turns):
        for _ in range(d):
            nrow, ncol, nfacing, nface = step2(row, col, facing, face, face_size, neighbor_map)
            if faces[nface][(nrow, ncol)] == 1:
                break
            row, col, facing, face = nrow, ncol, nfacing, nface
        facing = (facing + t) % 4
    final_row = row + face[0]*face_size
    final_col = col + face[1]*face_size
    return final_row * 1000 + final_col * 4 + facing


data = open("data/day22.txt").read().splitlines()
test_data = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''.splitlines()

print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data, 50)}")
