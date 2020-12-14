import re

BITS = 36
MAX = 0b111111111111111111111111111111111111

class Cpu:
    def __init__(self):
        self.enable = 0
        self.value =  0
        self.mem = {}

    def __str__(self):
        return "mask:"+str(self.enable)+","+str(self.value)+"\n mem:"+str(self.mem)

    def set_mask(self, mask):
        nbits = len(mask)
        if not nbits == BITS:
            raise(Exception("mask must be 36 bits, was",nbits))
        # print("set_mask:", mask)
        e = ''
        v = ''
        for i in range(BITS):
            c = mask[i]
            if c == 'X':
                e += '0'
                v += '0'
            else:
                e += '1'
                v += c
        self.enable = int(e,2)
        self.value = int(v,2)

    def apply_mask(self, value):
        a = self.enable & self.value
        b = (MAX - self.enable) & value
        ret = a | b
        # print("apply mask e:",self.enable,"v:",self.value,"a:",a,"b:",b,"->",ret)
        return ret

    def set_value(self, addr, value):
        masked = self.apply_mask(value)
        # print("set:",value,'->',masked)
        if masked > 0:
            self.mem[addr] = masked
        else:
            self.mem.pop(addr,None)
        return masked

    def count_memory(self):
        ret = 0
        for loc in self.mem:
            ret += self.mem[loc]
        return ret


def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    cpu = Cpu()
    for line in lines:
        possible = re.match("mask = ([01X]{36})", line)
        if possible:
            mask = possible.group(1)
            cpu.set_mask(mask)
            print("set mask: ",mask)
            continue
        possible = re.match("mem\[(\d+)\] = (\d+)", line)
        if possible:
            addr,value = possible.groups()
            masked = cpu.set_value(addr,int(value))
            print("set addr:",addr,"value:",value,"->",masked)
            continue
        print("unknown line: " + line)

    # print(cpu)
    print("result:",cpu.count_memory())

if __name__ == '__main__':
    # solve(1, "test1.txt")
    solve(1)
    # solve(2, "test1.txt")
    # solve(2)