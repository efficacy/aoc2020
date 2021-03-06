
def next(n, map, turn):
    if n in map:
        value = turn - map[n] - 1
        # print("turn", turn, "=", value, "( found", n, "at index", map[n], ")")
        return value
    else:
        # print("turn",turn,"=",0,"( not found", n, ")")
        return 0

def solve(qpart, filename='input.txt', nsteps=None):
    if nsteps == None:
        if qpart == 1:
            nsteps = 2020
        else:
            nsteps = 30000000
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    starters = [int(x) for x in lines[0].split(',')]
    print("loaded:",starters)

    map = {}
    turn = 1
    prev = None
    for value in starters:
        if prev != None:
            map[prev] = turn-1
        print("turn",turn,"=",value,"(starter)")
        turn += 1
        prev = value

    while turn <= nsteps:
        value = next(prev, map, turn)
        map[prev] = turn-1
        turn += 1
        if 0 == turn % 1000:
            print(".",end='')
        if 0 == turn % 100000:
            print("\n",turn)
        prev = value
    print("final:",prev)

if __name__ == '__main__':
    # solve(1, "test1.txt", 10)
    # solve(1, "test1.txt")
    # solve(1)
    # solve(2, "test1.txt", 10)
    # solve(2, "test1.txt")
    solve(2)
