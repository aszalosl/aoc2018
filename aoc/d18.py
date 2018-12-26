import collections
OPEN = '.'
TREE =  '|'
LUMBER ='#'
# test
#FILE = "180.in"
SIZE = 10
#puzzle
FILE = "18.in"


with open(FILE) as f:
    field = [line.strip() for line in f.readlines()]
t={}
for j,fs in enumerate(field):
    for i,f in enumerate(fs):
        t[i,j] = f


def neighbours(t, i, j):
    return collections.Counter([t.get((i+x,j+y),"?") for x in range(-1,2) for y in range(-1,2)])  

def next_state(t):
    t2 = {}
    for xy in t:
        x,y = xy
        n = neighbours(t,x,y)
        if t[x,y] == OPEN:
            na = TREE if n[TREE]>=3 else OPEN
        elif t[x,y] == TREE:
            na = LUMBER if n[LUMBER]>=3 else TREE
        elif t[x,y] == LUMBER:
            na = LUMBER if n[LUMBER]>=2 and n[TREE]>=1 else OPEN
        t2[x,y]= na
    return t2


def draw(t,x,y):
    for j in range(x):
        for i in range(y):
            print(t.get((i,j),'?'), end="")
        print()
    print()
    
timeline=[]  
for i in range(1000):
    s = collections.Counter([t[i] for i in t])
    timeline.append(s[TREE]*s[LUMBER])
    t = next_state(t)
    if i%100==0:
        print(".",end='')

print("Part1: ", timeline[10])    

t1 = 1000000000 % 28 
t5 = 500 % 28
m = max(timeline[500:])
print(m,[i for i,x in enumerate(timeline) if x == m])    
