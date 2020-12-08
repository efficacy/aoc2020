
class Cpu:
    def __init__(self):
        self.microcode = {
            "nop": self.nop,
            "acc": self.acc,
            "jmp": self.jmp,
            "hlt": self.hlt
        }

    def status(self):
        return "[ac=" + str(self.accumulator)+" pc=" + str(self.programcounter)+"]"

    def nop(self, offset):
        # print(" nop "+str(offset)+self.status())
        self.programcounter += 1

    def acc(self, offset):
        # print(" acc "+str(offset)+self.status())
        self.accumulator += offset
        self.programcounter += 1

    def jmp(self, offset):
        # print(" jmp "+str(offset)+self.status())
        self.programcounter = self.programcounter + offset

    def hlt(self, offset):
        # print(" hlt " + str(offset) + self.status())
        raise Exception("Halt ac="+str(self.accumulator)+" pc="+str(self.programcounter))


    def execute(self, instruction):
        cmd, arg = instruction
        print("exec " + cmd + "(",arg,") "+self.status())
        op = self.microcode.get(cmd, None)
        if op != None:
            op(arg)
            return
        print("Invalid opcode: ",cmd)

    def run(self, script):
        bottom = 0
        top = len(script)
        seen = set() # to catch infiniite loops

        self.accumulator = 0
        self.programcounter = 0
        while self.programcounter >= bottom and self.programcounter < top:
            seen.add(self.programcounter)
            instruction = script[self.programcounter]
            self.execute(instruction)
            if self.programcounter in seen:
                raise Exception("Hit a loop! " + self.status())
        raise Exception("Segfault! " + self.status()+" top="+str(top))

def value(arg):
    sign = arg[0]
    n = int(arg[1:])
    if sign == "-":
        n = -n
    return n

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.readlines()
    script = []
    for line in lines:
        cmd,arg = line.rstrip("\n").split(" ")
        script.append((cmd,value(arg)))

    cpu = Cpu()
    try:
        ret = cpu.run(script)
    except Exception as error:
        print(str(error))

if __name__ == '__main__':
    solve(1)
    # solve(2)