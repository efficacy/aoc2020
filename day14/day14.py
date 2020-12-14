import re
import math

BITS = 36
MAX = 0b111111111111111111111111111111111111

def invert(x):
    return MAX - x

def double(values, bit):
    # print("double:",values,bit)
    ret = []
    for value in values:
        # print("considering:",value)
        zero = value & invert(bit)
        one = zero | bit
        ret.append(zero)
        ret.append(one)
        # print("appended:",ret)
    return ret

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
        b = (invert(self.enable)) & value
        ret = a | b
        # print("apply mask e:",self.enable,"v:",self.value,"a:",a,"b:",b,"->",ret)
        return ret

    def apply_mask2(self, value):
        floaters = invert(self.enable)
        # print("apply mask 2 e:",format(self.enable,'b'),"f:",format(floaters,'b'),"v:",self.value,"i",value)
        base = self.value | value
        ret = [base]
        for i in range(BITS):
            bit = int(math.pow(2,i))
            if (floaters & bit):
                ret = double(ret, bit)
                # print("after double:", ret)
                # raise(Exception("huh"))
        # print("apply mask 2 e:",self.enable,"v:",self.value,"->",ret)
        return ret

    def put(self, addr, value):
        # print("put:",addr,':=',value)
        if value > 0:
            self.mem[addr] = value
        else:
            self.mem.pop(addr, None)

    def set_value(self, addr, value, qpart):
        if (qpart == 1):
            masked = self.apply_mask(value)
            self.put(addr, masked)
        else:
            masked = self.apply_mask2(addr)
            for a in masked:
                self.put(a, value)
        return masked

    def count_memory(self):
        ret = 0
        for loc in self.mem:
            ret += self.mem[loc]
        return ret

# return all possible combinations of bits where mask is 0
def splurge(mask,value, input):
    pass

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
            masked = cpu.set_value(int(addr),int(value), qpart)
            print("set addr:",addr,"value:",value,"->",masked)
            continue
        print("unknown line: " + line)

    # print(cpu)
    print("result:",cpu.count_memory())

if __name__ == '__main__':
    # solve(1, "test1.txt")
    # solve(1)

    # cpu = Cpu()
    # cpu.set_mask('000000000000000000000000000000000X0X')
    # v = 0xF
    # print('app1',cpu.apply_mask(v))
    # print('app2',cpu.apply_mask2(v))
    # solve(2, "test2.txt")
    # solve(2, "test3.txt")
    # solve(2, "test1.txt")
    solve(2)