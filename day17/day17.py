
def nb3d(key):
    x ,y ,z = key
    # print("nb:", x, y, z)
    ret = []
    for ix in range( x -1 , x +2):
        for iy in range( y -1 , y +2):
            for iz in range( z -1 , z +2):
                # print("considering:", ix, iy, iz)
                if ix == x and iy == y and iz == z:
                    continue
                ret.append((ix ,iy ,iz))
    return ret

def nb4d(key):
    x ,y ,z, w = key
    # print("nb:", x, y, z, w)
    ret = []
    for ix in range( x -1 , x +2):
        for iy in range( y -1 , y +2):
            for iz in range( z -1 , z +2):
                for iw in range(w - 1, w + 2):
                    # print("considering:", ix, iy, iz, iw)
                    if ix == x and iy == y and iz == z and iw == w:
                        continue
                    ret.append((ix ,iy ,iz, iw))
    return ret

def is_active(key, grid):
    cell = grid.get(key)
    if cell == None:
        return False
    return cell.status == '#' or cell.status == 'v' # active or deactivating

def count_nb(key, grid):
    ret = 0
    for key in nb3d(key):
        if is_active(key, grid):
            ret += 1
    return ret

def split(cell, grid):
    active = set()
    inactive = set()
    for key in cell.nb:
        if is_active(key, grid):
            active.add(key)
        else:
            inactive.add(key)
    return (active, inactive)

def clean(grid):
    remove = []
    for key in grid:
        cell = grid[key]
        if cell.status == 'v': # deactivating
            remove.append(key)
        if cell.status == '^': # activating
            cell.status = '#'

    for key in remove:
        grid.pop(key, None)

class Cell:
    def __init__(self, key, status, nb):
        self.key = key
        self.status = status
        self.nb = nb

def load3d(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    grid = {}
    for y in range(0, len(lines)):
        line = lines[y].strip()
        for x in range(len(line)):
            v = line[x]
            if v == '#':
                key = (x,y,0)
                cell =  Cell(key, '#', nb3d(key))
                grid[key] = cell
                # print("loaded active cell at",key)
    return grid

def load4d(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    grid = {}
    for y in range(0, len(lines)):
        line = lines[y].strip()
        for x in range(len(line)):
            v = line[x]
            if v == '#':
                key = (x,y,0,0)
                cell =  Cell(key, '#', nb4d(key))
                grid[key] = cell
                # print("loaded active cell at",key)
    return grid

def generation(grid, qpart):
    changed = False
    candidates = set()
    changed = False
    if qpart == 1:
        nbfn = nb3d
    else:
        nbfn = nb4d

    for key in grid:
        cell = grid[key]
        (active,inactive) = split(cell, grid)
        # print("coonsidering",key,"active:",active,"inactive:",inactive)
        n = len(active)
        if n < 2 or n > 3:
            cell.status = 'v' # deactivate
            # print("deactivating old cell at", key)
        candidates.update(inactive)

    for key in candidates:
        neighbours = nbfn(key)
        n = 0
        for nk in neighbours:
            if is_active(nk, grid):
                n += 1
            if n > 3:
                break
        if n == 3:
            grid[key] = Cell(key, '^', nbfn(key))
            # print("activating new cell at",key)
            changed = True

    if changed:
        clean(grid)
    return changed

def dump3d(grid, gen):
    print("-- generation",gen)
    bounds = [ [None, None], [None, None], [None, None] ]
    X = 0
    Y = 1
    Z = 2
    MIN = 0
    MAX = 1
    for key in grid:
        x,y,z = key
        if bounds[X][MIN] == None or x < bounds[X][MIN]:
            bounds[X][MIN] = x
        if bounds[X][MAX] == None or x > bounds[X][MAX]:
            bounds[X][MAX] = x
        if bounds[Y][MIN] == None or y < bounds[Y][MIN]:
            bounds[Y][MIN] = y
        if bounds[Y][MAX] == None or y > bounds[Y][MAX]:
            bounds[Y][MAX] = y
        if bounds[Z][MIN] == None or z < bounds[Z][MIN]:
            bounds[Z][MIN] = z
        if bounds[Z][MAX] == None or z > bounds[Z][MAX]:
            bounds[Z][MAX] = z

    print("dump, bounds:",bounds)
    for z in range(bounds[Z][MIN], bounds[Z][MAX]+1):
        print("z="+str(z))
        for y in range(bounds[Y][MIN], bounds[Y][MAX] + 1):
            for x in range(bounds[X][MIN], bounds[X][MAX] + 1):
                c = '.'
                if is_active((x,y,z), grid):
                    c = '#'
                print(c, end='')
            print()

def dump4d(grid, gen):
    print("-- generation",gen)
    bounds = [ [None, None], [None, None], [None, None], [None, None] ]
    X = 0
    Y = 1
    Z = 2
    W = 3
    MIN = 0
    MAX = 1
    for key in grid:
        x,y,z,w = key
        if bounds[X][MIN] == None or x < bounds[X][MIN]:
            bounds[X][MIN] = x
        if bounds[X][MAX] == None or x > bounds[X][MAX]:
            bounds[X][MAX] = x
        if bounds[Y][MIN] == None or y < bounds[Y][MIN]:
            bounds[Y][MIN] = y
        if bounds[Y][MAX] == None or y > bounds[Y][MAX]:
            bounds[Y][MAX] = y
        if bounds[Z][MIN] == None or z < bounds[Z][MIN]:
            bounds[Z][MIN] = z
        if bounds[Z][MAX] == None or z > bounds[Z][MAX]:
            bounds[Z][MAX] = z
        if bounds[W][MIN] == None or w < bounds[W][MIN]:
            bounds[W][MIN] = w
        if bounds[W][MAX] == None or w > bounds[W][MAX]:
            bounds[W][MAX] = w

    print("dump, bounds:",bounds)
    for w in range(bounds[W][MIN], bounds[W][MAX]+1):
        for z in range(bounds[Z][MIN], bounds[Z][MAX]+1):
            print("z="+str(z)+", w="+str(w))
            for y in range(bounds[Y][MIN], bounds[Y][MAX] + 1):
                for x in range(bounds[X][MIN], bounds[X][MAX] + 1):
                    c = '.'
                    if is_active((x,y,z,w), grid):
                        c = '#'
                    print(c, end='')
                print()

def solve(qpart, filename='input.txt', gens=6):
    print("Part " + str(qpart))
    if qpart == 1:
        grid = load3d(filename)
        # dump3d(grid, 0)
    else:
        grid = load4d(filename)
        # dump4d(grid, 0)
    for i in range(1,gens+1):
        generation(grid, qpart)
        # dump(grid, i)
    return len(grid)

if __name__ == '__main__':
    # answer = solve(1, "test1.txt")
    answer = solve(1)
    print("answer:", answer)

    # answer = solve(2, "test1.txt")
    answer = solve(2)
    print("answer:", answer)
