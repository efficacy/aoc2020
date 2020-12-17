import math

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

direction_lookup = {
    (-1, 0): 'n',
    (-1, 1): 'ne',
    (0, 1): 'e',
    (1, 1): 'se',
    (1, 0): 's',
    (1, -1): 'sw',
    (0, -1): 'w',
    (-1, -1): 'nw'
}

class Seat:
    def __init__(self, r, c, status='L'):
        # print("creating seat r:",r,"c:",c)
        self.r = r
        self.c = c
        self.status = status
        self.nb = []

    def is_occupied(self):
        return self.status == '#' or self.status == '^'

    def is_adjacent(self, r, c):
        if self.r == r and self.c == c:
            return False # don't count myself!
        return self.r >= r-1 and self.r <= r+1 and self.c >= c-1 and self.c <= c+1

    def find_direction(self, other):
        if self.r == other.r and self.c == other.c:
            return (None,None) # don't count myself!
        # now work out if the supplied co-ords lie on a cardinal axis from this point
        offset_r = other.r - self.r
        abs_r = abs(offset_r)
        offset_c = other.c - self.c
        abs_c = abs(offset_c)

        if  offset_r == 0 or offset_c == 0 or abs_c == abs_r:
            if offset_r == 0:
                offset = (0, sign(offset_c))
                distance = abs_c
            elif offset_c == 0:
                offset = (sign(offset_r), 0)
                distance = abs_r
            else:
                offset = ( sign(offset_r), sign(offset_c))
                distance = abs_r

            return (direction_lookup[offset], distance)

        return (None,None)

    def count_neighbours(self):
        ret = 0
        for other in self.nb:
            if other.is_occupied():
                ret += 1
        return ret

    def occupy(self):
        # print("occupy",self.r,self.c)
        self.status = 'v' # v => sitting down

    def vacate(self):
        # print("vacate",self.r,self.c)
        self.status ='^' # ^ => getting up

    def complete(self):
        if self.status == 'v':
            # print("sitting at",self.r,self.c)
            self.status = '#'
        if self.status == '^':
            # print("standing at",self.r,self.c)
            self.status = 'L'

    def __str__(self):
        return "Seat(" + str(self.r) + "," + str(self.c) + "," + str(self.status) + ")"


def count_immediate_neighbours(seat, neighbours):
    ret = 0
    for seat in neighbours[seat]:
        if seat.is_occupied():
            ret += 1
    return ret


def dump(seats):
    for seat in seats:
        print("(",seat.r,",",seat.c,",",seat.status,")")

def find_immediate_neighbours(seats, r, c):
    return [seat for seat in seats if seat.is_adjacent(r,c)]

def find_directional_neighbours(seat, seats):
    print("fdn considering",seat)
    ret = { 'n':(None,None),'ne':(None,None),'e':(None,None),'se':(None,None),
            's':(None,None),'sw':(None,None),'w':(None,None),'nw':(None,None), }
    for other in seats:
        direction,distance = seat.find_direction(other)
        if direction != None:
            print(" found neighbour dir:",direction,"dist:",distance)
            best = ret[direction][0]
            if best == None or distance < best:
                print("updated best",direction,"to",seat)
                ret[direction] = (distance, seat)

    for d in ret:
        entry = ret[d]
        print("trying to unpack",entry)
        dist,seat = entry
        if dist != None:
            seat.nb3d.append(seat)
    return ret

global height
global width

def load(filename, qpart):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    seats = []
    nseats = 0
    for r in range(0,len(lines)):
        line = list(lines[r])
        width = len(line)
        height += 1
        for c in range(0,len(line)):
            v = line[c]
            if v == 'L' or v == '#':
                seats.append(Seat(r, c, v))
                nseats += 1
    # print("found",nseats,"seats, len(self.seats):",len(self.seats))
    # for seat in self.seats:
    #     print(seat)

    neighbours = {}
    for seat in seats:
        if qpart == 1:
            seat.nb = find_immediate_neighbours(seat, seats)
        else:
           seat.nb = find_directional_neighbours(seat, seats)

    return seats, neighbours

def generation(seats, nlimit):
    changed = False
    for seat in seats:
        occupied = seat.is_occupied()
        n = seat.count_neighbours()
        # print("considering:",seat.r,seat.c,seat.status,"occ:",occupied,"n:",n)
        if not occupied and n == 0:
            seat.occupy()
            changed = True
        elif occupied and n >= nlimit:
            seat.vacate()
            changed = True
    # dump(seats)
    if changed:
        for seat in seats:
            seat.complete()
    return changed

def dump(seats,label):
    print("----",label)
    map = []
    for r in range(0,height):
        row = []
        for c in range(0,width):
            row.append(".")
        map.append(row)
    for seat in seats:
        map[seat.r][seat.c] = seat.status
    for r in range(0,height):
        print("".join(map[r]))


def solve(qpart, filename='input.txt', size=25):
    print("Part " + str(qpart))
    seats, neighbours = load(filename, qpart)

    step = 0
    if qpart == 1:
        nlimit = 4
    else:
        nlimit = 5
    while generation(seats, nlimit):
        step += 1
        print(".",end='')
        # dump(seats)

    occupied = 0
    for seat in seats:
        if seat.is_occupied():
            occupied += 1
    print("\nterminated after",step,"steps with",occupied,"seats occupied")

def check(seat, r, c, exp):
    print(seat.r, seat.c,'->',r,c,"=",seat.find_direction(r,c),'sould be',exp)

if __name__ == '__main__':
    # solve(1, "test2.txt")
    # solve(1, "test1.txt")
    # solve(1)
    # solve(2, "test1.txt")
    # solve(2)

    seat = Seat(3,4,'L')
    # check(seat, 3, 4, (None, None))
    #
    # check(seat, 2, 4, ('n', 1))
    # check(seat, 4, 4, ('s', 1))
    # check(seat, 3, 5, ('e', 1))
    # check(seat, 3, 3, ('w', 1))
    #
    # check(seat, 4, 5, ('se', 1))
    # check(seat, 5, 6, ('se', 2))
    # check(seat, 2, 5, ('ne', 1))
    # check(seat, 4, 3, ('sw', 1))
    # check(seat, 2, 3, ('nw', 1))
    #
    # check(seat, 2, 6, (None, None))
    # check(seat, 1, 4, ('w', 2))
    # check(seat, 1, 5, (None, None))
    # check(seat, 3, 1, ('n', 3))

    seats = [
        Seat(2,4, '#'),
        Seat(2,6),
        Seat(4,4),
        Seat(1,4, '#'),
        Seat(3,5, '#'),
        Seat(3,3)
    ]
    seat.nb = find_directional_neighbours(seat, seats)
    print(seat.count_neighbours())