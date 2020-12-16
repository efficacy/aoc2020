import re

def parse_csv(line):
    # print("csv:",line,end='')
    ret = []
    buf = []
    for c in line:
        if c == ',':
            if len(buf) > 0:
                ret.append(int(''.join(buf)))
                buf = []
        elif c.isdigit():
            buf.append(c)
    if len(buf) > 0:
        ret.append(int(''.join(buf)))
    # print("->",ret)
    return ret

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    categories = {}
    mine = []
    nearby = []
    field_pattern = re.compile(r'([a-z ]+):(.+)')
    range_pattern = re.compile(r"(\d+)-(\d+) or (\d+)-(\d+)")
    valid = set()
    invalid_rt = 0

    state = 0 # fields
    for line in lines:
        line = line.strip()
        if '' == line:
            state += 1
            continue
        if line.endswith(':'):
            continue # skip labels

        if state == 0: # rules block
            m = field_pattern.match(line)
            key = m.group(1)
            rule = m.group(2).strip()
            # print("field:",key,"rule:",rule)
            m = range_pattern.match(rule)
            f1 = int(m.group(1))
            t1 = int(m.group(2))
            f2 = int(m.group(3))
            t2 = int(m.group(4))
            # print(" from",f1,"to",t1," from",f2,"to",t2)
            allowed = set()
            for i in range(f1,t1+1):
                allowed.add(i)
            for i in range(f2,t2+1):
                allowed.add(i)
            valid |= allowed
            categories[key] = allowed

        elif state == 1: # my ticket block
            mine = parse_csv(line)

        elif state == 2: # nearby tickets block
            values = parse_csv(line)
            ok = True
            for v in values:
                if not v in valid:
                    invalid_rt += v
                    ok = False
            if ok:
                nearby.append(values)

        else:
            raise(Exception("huh? unknown state"))
    print("cats:",categories)
    print("vald:",valid)
    print("mine:",mine)
    print("near:",nearby)

    nfields = len(categories)
    can_be = {}
    for i in range(nfields):
        options = set()
        for k in categories:
            options.add(k)
        can_be[i] = options

    for ticket in nearby:
        # print("considering:",ticket)
        for i in range(nfields):
            value = ticket[i]
            # print(" val:", value)
            options = can_be[i]
            # print(" opts:", options)
            nu = set()
            changed = False
            for opt in options:
                numbers = categories[opt]
                # print(" numbers:", numbers)
                if value in numbers:
                    nu.add(opt)
                else:
                    changed = True
            if changed:
                can_be[i] = nu

    print("can_be:",can_be)

    must_be = {}
    while len(must_be) < nfields:
        for i in can_be:
            options = can_be[i]
            # print("considering:",i,'->',options)
            if len(options) == 1:
                selected = options.pop()
                must_be[i] = selected
                for ff in can_be:
                    can_be[ff].discard(selected)

    print("must_be:",must_be)

    mine_annotated = {}
    for ff in must_be:
        mine_annotated[must_be[ff]] = mine[ff]

    print("mine annotated:",mine_annotated)

    departure = 1
    for name in mine_annotated:
        if name.startswith('departure'):
            value = mine_annotated[name]
            print("multiplying field",name,'=',value)
            departure *= value

    print("product of departure fields:", departure)

    if qpart == 1:
        return invalid_rt
    else:
        return departure



if __name__ == '__main__':
    # answer = solve(1, "test1.txt")
    # answer = solve(1)
    # answer = solve(2, "test2.txt")
    answer = solve(2)
    print("answer:",answer)
