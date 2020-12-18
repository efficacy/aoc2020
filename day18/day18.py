from enum import Enum

class State(Enum):
    NUM1 = 0
    NUM2 = 1

def calculate(op, n1, n2, indent):
    ret = 0
    if op == '+':
        ret = n1 + n2
    elif op == '*':
        ret = n1 * n2
    else:
        raise (Exception("huh? unexpected operation", op))
    print(indent,"calculate(",op,n1,n2,") ->",ret)
    return ret

def evaluate(input, indent):
    total = 0
    state = State.NUM1
    n1 = 0
    op = '+'
    n2 = 0
    buf = 0

    c = ' '
    while c != None:
        c = next(input, None)
        while c != None and c.isspace():
            c = next(input, None)
        # print(indent,"raw c",c)
        if c == None:
            break
        print(indent,"state",state,"c",c,"n1",n1,"op",op,"n2",n2)
        if state == State.NUM1:
            if c == '(':
                buf = evaluate(input, indent)
            elif c == ')':
                ret = n1
                print(indent, "returning", ret)
                return ret
            elif c.isdigit():
                buf *= 10
                buf += int(c)
            elif c == '+' or c == '*':
                op = c
                n1 = buf
                buf = 0
                state = State.NUM2
            else:
                raise(Exception("huh? unexpected character",c,"at state",state))
        elif state == State.NUM2:
            if c == '(':
                buf = evaluate(input,indent+' ')
            elif c == ')':
                ret = calculate(op, n1, buf,indent)
                print(indent, "returning", ret)
                return ret
            elif c.isdigit():
                buf *= 10
                buf += int(c)
            elif c == '+' or c == '*':
                n2 = buf
                n1 = calculate(op, n1, n2, indent)
                op = c
                n2 = 0
                buf = 0
            else:
                raise(Exception("huh? unexpected character",c,"at state",state))

    print(indent,"at end state:",state,"c",c,"n1",n1,"op",op,"n2",n2)
    if state == State.NUM1:
        ret = n1
    elif state == State.NUM2:
        ret = calculate(op, n1, buf,indent)
    print(indent,"returning",ret)
    return ret

def process(line):
    input = (c for c in line)
    return evaluate(input,'')

def solve(qpart, filename='input.txt', gens=6):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    result = 0
    for line in lines:
        line = line.strip()
        answer = process(line)
        print("line value:",answer)
        result += answer
    return result

if __name__ == '__main__':
    # answer = solve(1, "test1.txt")
    # answer = solve(1, "test2.txt")
    # answer = solve(1, "test3.txt")
    # answer = solve(1, "test4.txt")
    answer = solve(1)
    print("answer:", answer)

    # answer = solve(2, "test1.txt")
    # answer = solve(2)
    # print("answer:", answer)
