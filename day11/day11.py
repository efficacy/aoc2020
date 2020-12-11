
class SeatMap:
    def __init__(self, data=[]):
        self.data = data

    def clone(self):
        data = []
        for row in self.data:
            data.append(row.copy())
        return SeatMap(data)

    def append(self, row):
        self.data.append(row)

    def get(self, r, c):
        return self.data[r][c]

    def set(self, r, c, v):
        self.data[r][c] = v

    def complete(self):
        for row in self.data:
            for i in range(0,len(row)):
                v = row[i]
                if v == 'v':
                    row[i] = '#'
                if v == '^':
                    row[i] = 'L'
    def dump(self, label=None):
        if (label):
            print(label)
        for row in self.data:
            print(''.join(row))

class Seat:
    def __init__(self, r, c):
        # print("creating seat r:",r,"c:",c)
        self.r = r
        self.c = c

    def is_occupied(self, seatmap):
        v = seatmap.get(self.r, self.c)
        return v == '#' or v == '^'

    def is_adjacent(self, r, c):
        if self.r == r and self.c == c:
            return False # don't count myself!
        return self.r >= r-1 and self.r <= r+1 and self.c >= c-1 and self.c <= c+1

    def count_neighbours(self, seatmap, seats):
        ret = 0
        for seat in list_neighbours(seats, self.r, self.c):
            if seat.is_occupied(seatmap):
                ret += 1
        return ret

    def occupy(self, seatmap):
        # print("occupy",self.r,self.c)
        seatmap.set(self.r, self.c, 'v') # v => sitting down

    def vacate(self, seatmap):
        # print("vacate",self.r,self.c)
        seatmap.set(self.r, self.c, '^') # ^ => getting up

    def __str__(self):
        return "(" + str(self.r) + "," + str(self.c) + ")"

def list_neighbours(seats, r,c):
    return [seat for seat in seats if seat.is_adjacent(r,c)]

def generation(seatmap, seats):
    changed = False
    for seat in seats:
        occupied = seat.is_occupied(seatmap)
        n = seat.count_neighbours(seatmap, seats)
        # print("considering:",seat.r,seat.c,"occ:",occupied,"n:",n)
        if not occupied and n == 0:
            seat.occupy(seatmap)
            changed = True
        elif occupied and n >= 4:
            seat.vacate(seatmap)
            changed = True
    if changed:
        seatmap.complete()
    return changed

def solve(qpart, filename='input.txt', size=25):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    seatmap = SeatMap()
    seats = []
    nseats = 0
    for r in range(0,len(lines)):
        line = list(lines[r])
        seatmap.append(line)
        for c in range(0,len(line)):
            v = line[c]
            if v == 'L':
                seats.append(Seat(r, c))
                nseats += 1
    # print("found",nseats,"seats, len(self.seats):",len(self.seats))
    # for seat in self.seats:
    #     print(seat)

    seatmap.dump("initial")
    step = 0
    while generation(seatmap, seats):
        step += 1
        print(".",end='')
        # seatmap.dump("step " + str(step))

    occupied = 0
    for seat in seats:
        if seat.is_occupied(seatmap):
            occupied += 1
    print("terminated after",step,"steps with",occupied,"seats occupied")

if __name__ == '__main__':
    # solve(1, "test2.txt")
    # solve(1, "test1.txt")
    solve(1)
    # solve(2, "test1.txt")
    # solve(2)