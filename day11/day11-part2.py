class Seat:
    def __init__(self, r, c, status):
        # print("creating seat r:",r,"c:",c)
        self.r = r
        self.c = c
        self.status = status
        self.nb = {
            'n': [],
            'ne': [],
            'e': [],
            'se': [],
            's': [],
            'sw': [],
            'w': [],
            'nw':[]
        }
        self.neighbours = []

    def is_occupied(self):
        return self.status == '#' or self.status == '^'

    def is_adjacent(self, other):
        if self.r == other.r and self.c == other.c:
            return None # don't count myself!
        diff_r = other.r - self.r
        diff_c = other.c - self.c
        if diff_r == 0:
            if diff_c > 0:
                return 'e'
            elif diff_c < 0:
                return 'w'
        elif diff_c == 0:
            if diff_r < 0:
                return 'n'
            elif diff_r > 0:
                return 's'
        elif abs(diff_c) == abs(diff_r):
            if diff_c > 0:
                if diff_r > 0:
                    return 'ne'
                else:
                    return 'se'
            elif diff_c < 0:
                if diff_r > 0:
                    return 'nw'
                else:
                    return 'sw'
        return None

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

    def occupy(self):
        # print("occupy",self.r,self.c)
        self.status = 'v' # v => sitting down

    def vacate(self):
        # print("vacate",self.r,self.c)
        self.status = '^' # v => standing up

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
        occupied = seat.is_occupied()
        n = seat.count_neighbours()
        # print("considering:",seat.r,seat.c,"occ:",occupied,"n:",n)
        if not occupied:
            if not seat.has_neighbours():
                seat.occupy()
                changed = True
        else:
            if seat.count_neighbours() == 5:
                seat.vacate()
                changed = True
    if changed:
        for seat in seats:
            seat.complete()
    return changed

def manhattan(seat1, seat2):
    return int(abs(seat2.r-seat1.r) + abs(seat2.c-seat1.c))

width = 0
height = 0

def dump(seats):

def solve(qpart, filename='input.txt', size=25):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    seats = []
    nseats = 0
    for r in range(0,len(lines)):
        line = lines[r]
        width = len(line)
        ++height
        for c in range(0,width):
            v = line[c]
            if v == 'L':
                seats.append(Seat(r, c, 'L'))
                nseats += 1
    for seat in seats:
        for other in seats:
            dir = seat.is_adjacent(other)
            if dir:
                distance = manhattan(seat, other)
                seat.nb[dir].append((distance, other))
        for dir in seat.nb:
            if len(seat.nb[dir]) > 0:
                list = sorted(seat.nb[dir], key=lambda tup: tup[0])
                list.sort(key=lambda tup: tup[0])
                seat.neighbours.append(list[0][1])

    dump(seats,"0")
    generation(seats)
    dump(seats,"1")
    generation(seats)
    dump(seats,"2")
    return

    step = 0
    while generation(seats):
        step += 1
        print(".",end='')
        # seatmap.dump("step " + str(step))

    occupied = 0
    for seat in seats:
        if seat.is_occupied():
            occupied += 1
    print("terminated after",step,"steps with",occupied,"seats occupied")

if __name__ == '__main__':
    solve(2, "test1.txt")
    # solve(2)