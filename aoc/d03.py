def check(i):
    x,y,u,v,id = factory[i]
    for j in range(u):
        for k in range(v):
            if b[x+j,y+k] > 1:
                return False
    print(id)
    return True

factory = []
with open("03.in") as file:
    for sor in file:
        ss = sor.split()
        o = ss[2][:-1].split(",")
        d = ss[3].split("x")
        factory.append((int(o[0]),int(o[1]), int(d[0]), int(d[1]), ss[0]))

b = {}
for f in factory:
    for i in range(f[2]):
        for j in range(f[3]):
            x = f[0]+i
            y = f[1]+j
            b[x,y]=b.get((x,y),0)+1
print(sum([1 for k in b if b[k]>1]))

i=0
while not check(i):
    i += 1

