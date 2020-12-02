import re

def parse(s):
    match = re.search('(\d+)-(\d+) ([a-z]): ([a-z]+)', s, re.IGNORECASE)
    min = match.group(1)
    max = match.group(2)
    letter = match.group(3)
    string = match.group(4)
    return (min,max,letter,string)

def count(letter, string):
    ret = 0
    for c in string:
        if c == letter:
            ret = ret + 1
    return ret

def solve(qpart):
    print("Part " + str(qpart))
    file1 = open('input.txt', 'r')
    lines = file1.readlines()
    valid = 0;
    for line in lines:
        min,max,letter,string = parse(line)
        if qpart == 1:
            n = count(letter, string)
            # print("split: (" + min + "," + max + "," + letter + "," + string + ") n=" + str(n))
            if n >= int(min) and n <= int(max):
                valid = valid + 1
        else:
            i1 = int(min)-1
            i2 = int(max)-1
            p1 = i1 < len(string) and string[i1] == letter
            p2 = i2 < len(string) and string[i2] == letter
            if (p1 or p2) and not (p1 and p2):
                valid = valid + 1

    print("  valid=" + str(valid))

if __name__ == '__main__':
    solve(1)
    solve(2)