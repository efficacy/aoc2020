
def count_group(group, qpart):
    if qpart == 1:
        matched = set()
        for entry in group:
            matched = matched.union(set(list(entry)))
    else:
        matched = set(list("abcdefghijklmnopqrstuvwxyz"))
        for entry in group:
            matched = matched.intersection(set(list(entry)))

    return len(matched)

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    sum = 0
    group = []
    for line in lines:
        line = line.rstrip()
        if line.isspace() or len(line) == 0:
            sum += count_group(group, qpart)
            group = []
        else:
            group.append(line)

    # catch last group
    if len(group) > 0:
        sum += count_group(group, qpart)
    print("sum=" + str(sum))

if __name__ == '__main__':
    solve(1)
    solve(2)