
def find(possible):
    for i in range(len(possible)):
        if possible[i] == 0:
            return i
    return None

def solve(qpart, filename='input.txt'):
    print("Part",qpart)
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    now = int(lines[0])
    timetable = lines[1].split(',')
    # print(now,timetable)
    busses = []
    for i in range(len(timetable)):
        bus = timetable[i]
        if bus != 'x':
            busses.append((i, int(bus)))
    # print(now, busses)
    if qpart == 1:
        then = now
        while True:
            possible = [then % x[1] for x in busses]
            # print(then,possible)
            id = find(possible)
            if id != None:
                break
            then += 1
        wait = then - now
        return wait * busses[id][1]
    else:
        then = 0
        step = 1
        # print("busses", busses)
        for mins, id in busses:
            while (then + mins) % id != 0:
                then += step
            step *= id
        return then

if __name__ == '__main__':
    # answer = solve(1,"test1.txt")
    # answer = solve(1)
    # answer = solve(2,"test1.txt")
    answer = solve(2)
    print("answer",answer)
