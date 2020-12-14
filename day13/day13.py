
def find(possible):
    for i in range(len(possible)):
        if possible[i] == 0:
            return i
    return None

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    now = int(lines[0])
    timetable = lines[1].split(',')
    print(now,timetable)
    busses = []
    for i in range(len(timetable)):
        bus = timetable[i]
        if bus != 'x':
            busses.append((i, int(bus)))
    print(now, busses)
    if qpart == 1:
        then = now
    else:
        then = 0
        state = 0
        prefix = ''
        nbusses = len(timetable)
        start = None
    while True:
        if qpart == 1:
            possible = [then % x[1] for x in busses]
            print(then,possible)
            id = find(possible)
            if id != None:
                break
            then += 1
        else:
            bus = timetable[state]
            if bus != 'x':
                mins = then % int(bus)
                # print('state',state,'consi dering bus',bus,then,"mins",mins)
                if mins == 0:
                    # print("match at state",state)
                    # print(".",end='')
                    if state > 5:
                        print(prefix+str(then))
                    if state == 0:
                        start = then
                    state += 1
                    prefix += ' '
                else:
                    state = 0
                    prefix = ''
            else:
                state += 1
            if state == nbusses:
                print("got one at",start,"!")
                break
            then += 1
            # steps += 1
            # if steps == 20:
            #     print("break out")
            #     return


if __name__ == '__main__':
    # solve(1, "test1.txt")
    # solve(1)
    # solve(2, "test1.txt")
    solve(2)