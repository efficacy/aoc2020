
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

def dump(seats,label, height, width):
    print("----",label)
    map = []
    for r in range(height):
        row = []
        for c in range(width):
            row.append(".")
        map.append(row)

    for seat in seats:
        map[seat.r][seat.c] = seat.status

    for r in range(height):
        print("".join(map[r]))

class Seat:
    def __init__(self, r, c, status):
        # print("creating seat r:",r,"c:",c)
        self.r = r
        self.c = c
        self.status = status
        self.neighbours = []

    def is_occupied(self):
        return self.status == '#' or self.status == '^'

    def count_neighbours(self):
        n = 0
        for other in self.neighbours:
            if other.is_occupied():
                n += 1
        return n

    def has_neighbours(self):
        for other in self.neighbours:
            if other.is_occupied():
                return True
        return False

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

    def occupy(self):
        # print("occupy",self.r,self.c)
        self.status = 'v' # v => sitting down

    def vacate(self):
        # print("vacate",self.r,self.c)
        self.status = '^' # ^ => standing up

    def complete(self):
        if self.status == 'v':
            self.status = '#'
        if self.status == '^':
            self.status = 'L'

    def __str__(self):
        return "(" + str(self.r) + "," + str(self.c) + "," + self.status + ")"

def generation(seats):
    changed = False
    for seat in seats:
        # watch = (seat.r == 0)
        # if watch:
        #     print(seat,end="=")
        #     for n in seat.neighbours:
        #         print(n,end=',')
        #     print()
        old = seat.status
        occupied = seat.is_occupied()
        if not occupied:
            if not seat.has_neighbours():
                seat.occupy()
                changed = True
        else:
            if seat.count_neighbours() >= 5:
                seat.vacate()
                changed = True
        # if watch:
        #     print(" ", old,'->',seat.status)
    if changed:
        for seat in seats:
            seat.complete()
    return changed

def manhattan(seat1, seat2):
    return int(abs(seat2.r-seat1.r) + abs(seat2.c-seat1.c))

def find_directional_neighbours(seat, seats):
    # print("fdn considering",seat)
    ret = { 'n':(None,None),'ne':(None,None),'e':(None,None),'se':(None,None),
            's':(None,None),'sw':(None,None),'w':(None,None),'nw':(None,None), }
    for other in seats:
        direction,distance = seat.find_direction(other)
        if direction != None:
            # print(" found neighbour dir:",direction,"dist:",distance)
            best = ret[direction][0]
            if best == None or distance < best:
                # print("updated best",direction,"to",seat)
                ret[direction] = (distance, other)

    # print("seat",seat,"has neighbours")
    # for d in ret:
    #     dist, seat = ret[d]
    #     if dist != None:
    #         print(' ',d,seat,dist)
    return ret

def init_seats(seat, seats):
    dirs = find_directional_neighbours(seat,seats)
    for d in dirs:
        entry = dirs[d]
        # print("trying to unpack",entry)
        dist,other = entry
        if dist != None:
            seat.neighbours.append(other)

def load(filename):
    height = 0
    width = 0
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    seats = []
    for r in range(0, len(lines)):
        line = lines[r]
        width = max(width,len(line))
        height += 1
        for c in range(0, width):
            v = line[c]
            if v == 'L':
                seats.append(Seat(r, c, 'L'))
    for seat in seats:
        init_seats(seat, seats)
    return (seats,height,width)


def solve(qpart, filename='input.txt', size=25):
    print("Part " + str(qpart))
    seats,height,width = load(filename)

    dump(seats,"0", height, width)
    # generation(seats)
    # dump(seats,"1", height, width)
    # generation(seats)
    # dump(seats,"2", height, width)
    # generation(seats)
    # dump(seats,"3", height, width)
    # return

    step = 0
    while generation(seats):
        step += 1
        print(".",end='')
        # seatmap.dump("step " + str(step))

    occupied = 0
    for seat in seats:
        if seat.is_occupied():
            occupied += 1
    print("\nterminated after",step,"steps with",occupied,"seats occupied")

if __name__ == '__main__':
    # solve(2, "test1.txt")
    solve(2)