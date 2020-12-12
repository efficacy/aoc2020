import math

directions = {
    'N': (0.0, 1.0),
    'E': (1.0, 0.0),
    'S': (0.0,-1.0),
    'W': (-1.0, 0.0)
}

def cartesian(rad):
    ret = (math.sin(rad), math.cos(rad))
    # print("cartesian",rad,'->',p(ret))
    return ret

def manhattan(offset):
    x,y = offset
    return int(abs(x) + abs(y))

def p(v):
    x,y = v
    return "(" + str(round(x,2)) + "," + str(round(y,2)) + ")"

def scale(values, multiplier):
    return tuple(multiplier * x for x in values)

def add(av, bv):
    ret = []
    for i in range(0,len(av)):
        ret.append(av[i] + bv[i])
    return tuple(ret)

def solve(qpart, filename='input.txt', size=25):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    position = (0,0)
    direction = 90
    waypoint = (10, 1)
    for step in lines:
        cmd = step[0]
        arg = int(step[1:])
        if qpart == 1:
            if cmd == 'N' or cmd == 'S' or cmd == 'E' or cmd == 'W':
                vector = directions[cmd]
                vector = scale(vector,arg)
                position = add(position, vector)
                # print("step:",step,"move",p(vector),"to",p(position))
            elif cmd == 'L':
                direction -= arg
                # print("step:",step,"turn to",direction)
            elif cmd == 'R':
                direction += arg
                # print("step:",step,"turn to",direction)
            elif cmd == 'F':
                vector = scale(cartesian(math.radians(direction)),arg)
                position = add(position, vector)
                # print("step:",step,"move",p(vector),"to",p(position))
            else:
                print("huh? unknown command",cmd)
        else:
            if cmd == 'N' or cmd == 'S' or cmd == 'E' or cmd == 'W':
                vector = directions[cmd]
                vector = scale(vector,arg)
                waypoint = add(waypoint, vector)
                # print("step:",step,"move waypoint",p(vector),"to",p(waypoint))
            if cmd == 'L' :
                cmd = 'R'
                arg = 360 - arg
            if cmd == 'R':
                x,y = waypoint
                if arg == 90:
                    waypoint = (y, -x)
                elif arg == 180:
                    waypoint = (-x, -y)
                elif arg == 270:
                    waypoint = (-y, x)
                # print("step:",step,"turn waypoint",arg,"to",waypoint)
            if cmd == 'F':
                vector = scale(waypoint,arg)
                position = add(position, vector)
                # print("step:",step,"move",p(vector),"to",p(position))
    print("final",p(position),"result",manhattan(position))

if __name__ == '__main__':
    # solve(1, "test1.txt")
    solve(1)
    # solve(2, "test1.txt")
    solve(2)