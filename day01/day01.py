def solve(qpart):
    print("Part " + str(qpart))
    file1 = open('input.txt', 'r')
    lines = file1.readlines()
    keys = []
    for line in lines:
        n = int(line)
        keys.append(n)
    if qpart == 1:
        for n in keys:
            v = 2020-n
            if v in keys:
                print("found match: " + str(n) + " and " + str(v) + " product=" + str(n * v))
                return
    else:
        for i in keys:
            for j in keys:
                n = i + j
                if n < 2020:
                    v = 2020 - n
                    if v in keys:
                        print("found match: " + str(i) + "," + str(i) + "," + str(v) + " product=" + str(i * j * v))
                        return

if __name__ == '__main__':
    solve(1)
    solve(2)


