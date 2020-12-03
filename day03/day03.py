def step(pos, slope):
    r,c = pos
    dr,dc = slope
    return (r + dr, c + dc)

def wrap(pos, width):
    r,c = pos
    return (r, c % width)

def is_tree(grid, pos):
    r,c = pos
    row = grid[r]
    return row[c] == '#'

def count_slope(grid, height, width, slope):
    pos = (0, 0)
    n = 0;
    while True:
        pos = wrap(step(pos, slope), width)
        r,c = pos
        if (r >= height):
            break
        t = is_tree(grid, pos)
        if t:
            n = n + 1
    return n

def solve(qpart):
    print("Part " + str(qpart))
    f = open('input.txt', 'r')
    lines = f.readlines()
    f.close()

    width = 0
    grid = []
    for line in lines:
        line = line.rstrip()
        if width == 0:
            width = len(line)
        grid.append(line)

    height = len(grid)
    print ("grid: w=" + str(width) + " h=" + str(height))

    if (qpart == 1):
        n = count_slope(grid, height, width, (1, 3))
        print("counted " + str(n) + " trees")
    else:
        slopes = [
            (1,1),
            (1,3),
            (1,5),
            (1,7),
            (2,1)
        ]
        product = 1
        for slope in slopes:
            n = count_slope(grid, height, width, slope)
            product *= n
            # print(str(slope) + ": counted " + str(n) + " trees, product=" + str(product))
        print("product for all slopes: " + str(product))

if __name__ == '__main__':
    solve(1)
    solve(2)