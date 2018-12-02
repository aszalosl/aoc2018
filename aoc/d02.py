import collections

def nearby():
    """find the solution of part B"""
    for i in ids:
        for j in ids:
            if i != j:
                if sum([1 for x,y in zip(i,j) if x!=y]) == 1:
                    print("".join([x for x,y in zip(i,j) if x==y]))
                    return
    
two = 0
three = 0
ids = []
with open("02.in") as file:
    for line in file:
        ids.append(line.strip())
        c = collections.Counter(line).values()
        if 2 in c:
            two += 1
        if 3 in c:
            three += 1
print(two*three)
nearby()
