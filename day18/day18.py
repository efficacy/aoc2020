from enum import Enum

class State(Enum):
    NUM1 = 0
    OP = 1
    NUM2 = 2

def calculate(op, n1, n2, indent):
    print(indent,"calculate(",op,n1,n2,")",end='')
    ret = 0
    if op == '+':
        ret = n1 + n2
    elif op == '*':
        ret = n1 * n2
    else:
        raise (Exception("huh? unexpected operation", op))
    print(" ->",ret)
    return ret

def evaluate(qpart, input, indent):
    total = 0
    state = State.NUM1
    acc = 0
    op = None

    token = ' '
    while token != None:
        token = next(input, None)
        # print(indent,"raw t",token)
        if token == None:
            break
        # print(indent,"state",state,"token",token,"acc",acc,"op",op)
        if state == State.NUM1:
            if token == '(':
                acc = evaluate(qpart, input, indent)
                state = State.OP
            elif token == ')':
                print(indent, "returning", acc)
                return acc
            else:
                acc = token
                state = State.OP
        elif state == State.OP:
            if token == '+' or token == '*':
                op = token
                state = State.NUM2
            elif token == ')':
                print(indent, "returning", acc)
                return acc
        elif state == State.NUM2:
            if token == '(':
                acc = calculate(op, acc,  evaluate(qpart, input,indent+' '), indent)
                op = None
                state = State.OP
            elif token == ')':
                acc = calculate(op, acc, token, indent)
                print(indent, "returning", acc)
                return acc
            else:
                acc = calculate(op, acc, token, indent)
                state = State.OP

    # print(indent,"at end state:",state,"c",token,"acc",acc,"op",op)
    # print(indent,"returning",acc)
    return acc

def next_token(line):
    buf = 0
    for c in line:
        if c.isdigit():
            buf = (buf * 10) + int(c)
        else:
            if buf > 0:
                yield buf
                buf = 0
            if c != ' ':
                yield c
    if buf > 0:
        yield buf

def solve(qpart, filename='input.txt', gens=6):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    result = 0
    for line in lines:
        line = line.strip()
        input = next_token(line)
        print("in",input)
        answer = evaluate(qpart, input, '')
        print("line value:",answer)
        result += answer
    return result

if __name__ == '__main__':
    # answer = solve(1, "test1.txt")
    # answer = solve(1, "test2.txt")
    answer = solve(1, "test3.txt")
    # answer = solve(1, "test4.txt")
    # answer = solve(1)
    # print("answer:", answer)

    # answer = solve(2, "test1.txt")
    # answer = solve(2, "test2.txt")
    # answer = solve(2, "test3.txt")
    # answer = solve(2, "test4.txt")
    # answer = solve(2)
    print("answer:", answer)
