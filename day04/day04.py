import re

expected = { "byr": "\d{4}", "iyr": "\d{4}", "eyr": "\d{4}", "hgt":"(\d+)(cm|in)",
             "hcl":"#[0-9a-f]{6}", "ecl":"(amb|blu|brn|gry|grn|hzl|oth)", "pid":"\d{9}"}
def all_present(entry):
    diff = set(expected) - set(entry)
    return len(diff) == 0

def out_of_range(v, min, max):
    n = int(v)
    return (n < min) or (n > max)

def all_valid(entry):
    for key in list(expected):
        if not re.match(expected[key]+"$",entry[key]):
            return False
    if out_of_range(entry["byr"], 1920,2002):
        return False
    if out_of_range(entry["iyr"], 2010,2020):
        return False
    if out_of_range(entry["eyr"], 2020,2030):
        return False
    hv,hunit = re.search(expected["hgt"], entry["hgt"]).groups()
    if hunit == "cm":
        if out_of_range(hv, 150, 193):
            return False
    elif hunit == "in":
        if out_of_range(hv, 59,76):
            return False
    else:
        return False
    return True

def check_entry(entry, qpart):
    ret = False
    if all_present(entry):
        if qpart == 1:
            ret = True
        else:
            if all_valid(entry):
                ret = True
    return ret

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    n = 0
    entry = {}
    for line in lines:
        if line.isspace():
            if check_entry(entry, qpart):
                n += 1
            entry = {}
        else:
            parts = line.split(" ")
            for part in parts:
                key,value = part.split(":")
                entry[key] = value.rstrip("\n")

    # catch final line
    if (len(entry) > 0):
        if check_entry(entry, qpart):
            n += 1

    print("valid: " + str(n))

if __name__ == '__main__':
    solve(1)
    solve(2)