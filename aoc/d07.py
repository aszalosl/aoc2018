# test version
#FILE = "070.in"
# real version
FILE = "07.in"
#"Step C must be finished before step A can begin."
# 0123456789 123456789 123456789 123456789 1234567
MAX=1000
pairs = []

def first(lst):
    a = {x[0] for x in lst}
    b = {x[1] for x in lst}
    return sorted(list(a-b))

def delete(c,lst):
    return [x for x in lst if x[0] != c]

with open(FILE) as f:
    for line in f:
        pairs.append((line[5], line[36]))
pairs2 = pairs[:] # make a copy
ps = pairs[:] # make a copy
order = []
while len(pairs) > 1:
    f = first(pairs)[0]
    order.append(f)
    pairs = delete(f,pairs)

order.append(pairs[0][0])
order.append(pairs[0][1])
# result 1
print("".join(order))

# test
#l = {k:(ord(k)-64) for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"} 
# real
l = {k:(ord(k)-4) for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"} 
l['*']=0
pairs2.append([order[-1],'*'])

def long(path,time):
    # print(path,time)
    c = path[-1]
    cont = [x[1] for x in pairs2 if x[0]==c]
    if cont:
        return max([long(path+[d], time+l[c]) for d in cont])
    else:
        return time + l[c]
def precond(c, lst):
    return {x[0] for x in lst if x[1]==c} 

ok = [set() for i in range(MAX)]
c = order[0] 
# test version
# jobs = [l[c], l[c]]
# real
jobs = [0,0,0,0,0,]
cs = first(pairs2)
while cs:
    jobs.sort()
    i = jobs[0]
    d = sorted([(long([c],jobs[0]),c) for c in first(pairs2)],reverse=True)
    c = d[0][1]
    while not precond(c,ps) <= ok[i]:
        i+=1
    jobs[0] = i+l[c]
    #print(c,i, jobs,d)
    for j in range(jobs[0],MAX):
        ok[j].add(c)
    pairs2 = delete(c,pairs2)
    cs = first(pairs2)
print(max(jobs))
