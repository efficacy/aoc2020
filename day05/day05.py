
def bisect(key, start, len):
    # print("bisect key=" + key + " start=" + str(start) + " len=" + str(len))
    if (len == 1):
        return start
    head = key[0]
    tail = key[1:]
    len = int(len/2)
    if (head == 'B' or head == 'R'):
        start = int(start + len)
    return bisect(tail, start, len)

def find(line):
    rowkey = line[0:7]
    row = bisect(rowkey, 0, 128)
    colkey = line[7:10]
    col = bisect(colkey, 0, 8)
    return (row,col)

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    highest = 0
    taken = []
    for line in lines:
        line = line.rstrip()
        row, col = find(line)
        result = row * 8 + col
        if (result > highest):
            highest = result
        taken.append(result)

    if (qpart == 1):
        print("highest: " + str(highest))
    else:
        taken = sorted(taken)
        prev = taken[0]-1
        for n in taken:
            if n > prev + 1:
                print("found a free seat at: " + str(n-1))
                break
            prev = n

if __name__ == '__main__':
    solve(1)
    solve(2)