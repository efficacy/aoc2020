
rules = {}
containers = {}

def get_containers(key, seen):
    if not key in containers:
        return
    parents = containers[key]
    for colour in parents:
        if not colour in seen:
            seen.add(colour)
            get_containers(colour, seen)


def get_contents(key, seen, multiplier = 1):
    if not key in rules:
        return 0
    contents = rules[key]
    count = multiplier
    for tuple in contents:
        if not tuple in seen:
            quantity, colour = tuple
            seen.add(colour)
            if (quantity > 0):
                inside = get_contents(colour, seen, quantity)
                count += multiplier * inside
    return count

def solve(qpart, filename='input.txt'):
    print("Part " + str(qpart))
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.rstrip("\n")
        words = line.split(" ")
        key = words[0] + " " + words[1]
        stripped = []
        for word in words[3:]:
            if word.endswith(","):
                word = word.rstrip(",")
            if word.endswith("."):
                word = word.rstrip(".")
            if word == "bag" or word == "bags" or word == "contain":
                continue
            if word == "no":
                word = "0"
            if word == "other":
                stripped.append(word) # need an extra word for counting to make sense
            stripped.append(word)
        tuples = []
        for i in range(0,len(stripped),3):
            label = stripped[i + 1] + " " + stripped[i + 2]
            tuples.append((int(stripped[i]), label))
            if not label in containers:
                containers[label] = []
            containers[label].append(key)
        rules[key] = tuples
    # print("rules: " + str(rules))
    # print("conts: " + str(containers))

    if (qpart == 1):
        found = set()
        get_containers("shiny gold", found)
        print(" shiny gold can fit in " + str(len(found)) +" bags")
    else:
        found = set()
        n = get_contents("shiny gold", found) - 1
        print(" shiny gold must contain " + str(n) + " other bags")

if __name__ == '__main__':
    solve(1)
    solve(2)