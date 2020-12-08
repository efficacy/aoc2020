class Cpu:
    def __init__(self):
        self.microcode = {
            "nop": self.nop,
            "acc": self.acc,
            "jmp": self.jmp
        }

    def nop(self, _):
        self.programcounter += 1

    def acc(self, offset):
        print(" acc offset=",offset," starting ac=",self.accumulator)
        self.accumulator += offset
        self.programcounter += 1
        print(" new ac=",self.accumulator)

    def jmp(self, offset):
        print(" jmp offset=",offset," starting pc=",self.programcounter)
        self.programcounter = self.programcounter + offset
        print(" new pc=",self.programcounter)

    def execute(self, instruction):
        cmd, arg = instruction
        print("exec ",cmd,"(",arg,") ac=",self.accumulator," pc=",self.programcounter)
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
                print("Hit a loop!")
                return
        print("Segfault pc=",self.programcounter," code length=",top)

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
    ret = cpu.run(script)
    print("terminated. final acc value is: ", cpu.accumulator)

if __name__ == '__main__':
    solve(1)
    # solve(2)