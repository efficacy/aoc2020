
def works(adapter, input):
    # print("does adapter",adapter,"work with input",input,"?")
    return input < adapter and input >= (adapter-3)

def find(sequence, input, available):
    # print("find seq:",sequence,"in:",input,"ava:",available)
    if len(available) == 0:
        print("found a match!",sequence)
        return sequence

    for adapter in available:
        # print("considering:",adapter)
        if works(adapter, input):
            # print("adapter",adapter,"can work with input",input)
            sofar = sequence.copy()
            sofar.append(adapter)
            ret = find(sofar, adapter, available.difference({adapter}))
            if ret != None:
                return ret
    return None

# the "lazy caterer' sequence a.k.a central polynomial numbers: 1,2,4,7,11,....
def caterer(n):
    return int((n * (n+1)/2) + 1)

def solve(qpart, filename='input.txt', size=25):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.readlines()

    available = set([int(line) for line in lines])
    final = max(available)
    # print(available)

    if qpart == 1:
        input = 0
        sequence = []
        sequence = find(sequence, input, available)
        if sequence == None:
            print("No valid sequence found :(")
            return
        # print("seq:",sequence)
        diffs = {
            1:0,
            2:0,
            3:1 # for the built-in adapter
        }
        for a in sequence:
            diff = a - input
            diffs[diff] += 1
            input = a

        # print("differences:",diffs)
        result = diffs[1] * diffs[3]
        print("result:",result)
    else:
        blocks = []
        block = []
        prev = 0

        # loop through finding contiguous blocks separated by two spaces
        for i in available:
            # print("considering:",i,"prev:",prev)
            if (i - prev) == 3:
                if len(block) > 0:
                    if (len(block)) > 1:
                        blocks.append(block)
                    block = []
            else:
                block.append(i)
            prev = i
        if len(block) > 0:
            blocks.append(block)
        # print(blocks)

        # the result is the product of the possible routes through each block
        ret = 1
        for b in blocks:
            value = caterer(len(b)-1)
            # print("block",b,"worth",value)
            ret *= value
        print("result:",ret)


if __name__ == '__main__':
    # solve(1, "test1.txt")
    # solve(1, "test2.txt")
    solve(1)
    # solve(2, "test1.txt")
    # solve(2, "test2.txt")
    solve(2)