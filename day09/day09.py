
def valid(n, window):
    for a in window:
        for b in window:
            if (n == (a+b) and a != b):
                return True
    return False

def find_sublist(n, numbers):
    rets = []
    for i in range(0,len(numbers)):
        a = numbers[i]
        for ret in rets:
            ret.append(a)
            if (sum(ret) == n):
                return ret
        rets.append([a])
    print("None found :(")

def solve(qpart, filename='input.txt', size=25):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.readlines()
    numbers = list(map(int, lines))

    window = []
    for i in range(0,size):
        n = numbers[i]
        window.append(n)
    for i in range(size,len(lines)):
        n = numbers[i]
        if not valid(n, window):
            if (qpart == 1):
                print("!",n,"is not a sum from",window)
                return n
            else:
                break
        window.append(n)
        window = window[1:]

    ret = find_sublist(n, numbers)
    low = min(ret)
    high = max(ret)
    print("!", n, "is a sum of ", ret)
    print(" min:", low, "max:", high, "sum of ends:", (low + high))

if __name__ == '__main__':
    # solve(1, "test1.txt", 5)
    solve(1)
    # solve(2, "test1.txt", 5)
    solve(2)