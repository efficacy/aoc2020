
class Cpu:
    def __init__(self):
        self.microcode = {
            "nop": self.nop,
            "acc": self.acc,
            "jmp": self.jmp,
            "hlt": self.hlt
        }
        self.reset()

    def reset(self):
        self.accumulator = 0
        self.programcounter = 0
        self.seen = set()

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
        # print("exec " + cmd + "(",arg,") "+self.status())
        op = self.microcode.get(cmd, None)
        if op != None:
            op(arg)
            return
        print("Invalid opcode: ",cmd)

def value(arg):
    sign = arg[0]
    n = int(arg[1:])
    if sign == "-":
        n = -n
    return n

def run(script, cpu):
    cpu.reset()
    while True:
        cpu.seen.add(cpu.programcounter)
        instruction = script[cpu.programcounter]
        cpu.execute(instruction)
        if cpu.programcounter in cpu.seen:
            raise Exception("Hit a loop! " + cpu.status())
        if cpu.programcounter < 0 or cpu.programcounter > len(script):
            raise Exception("Segfault! " + cpu.status())
        if (cpu.programcounter == len(script)):
            return cpu

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.readlines()
    script = []
    for line in lines:
        cmd,arg = line.rstrip("\n").split(" ")
        script.append((cmd,value(arg)))

    cpu = Cpu()
    if qpart == 1:
        try:
            ret = run(script, cpu)
        except Exception as error:
            print(str(error))
    else:
        for i in range(0,len(script)):
            cmd,arg = script[i]
            if cmd == "nop":
                print("replacing nop at ",i)
                script2 = script.copy()
                script2[i] = ("jmp",arg)
                try:
                    run(script2, cpu)
                    print("found a working versin by changing instruction " + str(i) + " to jmp, ac=" + str(cpu.accumulator))
                    return
                except Exception as error:
                    print(str(error))
            elif cmd == "jmp":
                print("replacing jmp at ",i)
                script2 = script.copy()
                script2[i] = ("nop", arg)
                try:
                    run(script2, cpu)
                    print("found a working versin by changing instruction " + str(i) + " to nop, ac=" + str(cpu.accumulator))
                    return
                except Exception as error:
                    print(str(error))
    print("tried all of them :(")

if __name__ == '__main__':
    solve(1)
    solve(2)