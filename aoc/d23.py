import itertools
# -*- coding: utf-8 -*-
#FILE = "230.in" # part1
#FILE = "231.in" # part2
FILE = "23.in"

bots = []


def inside(bots, x, y, z, i):
    "point x,y,z is in radius bot #i?"
    d = abs(x-bots[i][0]) + abs(y-bots[i][1]) + abs(z-bots[i][2])
    return d <= bots[i][3]


def strong(bots,i):
    "how many bots are inside radius of bot #i?"
    counter = 0
    sb = len(bots)
    for j in range(sb):
        if inside(bots, bots[j][0], bots[j][1], bots[j][2], i):
            counter += 1
    return counter    


def ranges(bots, x,y,z):
    "how many bots reach the point x,y,z?"
    counter = 0
    sb = len(bots)
    for j in range(sb):
        if inside(bots, x,y,z, j):
            counter += 1
    return counter


with open(FILE) as f:
    for l in f:
        l0 = "".join([i for i in l if i.isdigit() or i in ['-',',']])
        bots.append([int(x) for x in l0.split(',')])

strongs = [(s[3],i) for i,s in enumerate(bots)]
strongs.sort(reverse=True)
ms = strongs[0][0]
candidates = [i[1] for i in strongs if i[0] == ms]
part1 = strong(bots,candidates[0])
print("Part 1: ", part1)

xmy = []
xpy = []
xmz = []
xpz = []
ymz = []
ypz = []

for b in bots:
    x,y,z,r = b
    xmy.append((x-y-r,-1))
    xmy.append((x-y+r, 1))
    xpy.append((x+y-r,-1))
    xpy.append((x+y+r, 1))
    xmz.append((x-z-r,-1))
    xmz.append((x-z+r, 1))
    xpz.append((x+z-r,-1))
    xpz.append((x+z+r, 1))
    ymz.append((y-z-r,-1))
    ymz.append((y-z+r, 1))
    ypz.append((y+z-r,-1))
    ypz.append((y+z+r, 1))

def innest(arr):
    arr.sort()
    delta = [i[1] for i in arr]
    acc = list(itertools.accumulate(delta))
    minacc = min(acc)
    i_s = [i for i,x in enumerate(acc) if x==minacc]
    return [(arr[i][0],arr[i+1][0]) for i in i_s]

xym1,xym2 = innest(xmy)[0]
xyp1,xyp2 = innest(xpy)[0]
x0 = (xym1+xyp1+xym2+xyp2)//4
y0 = (xyp1-xym1+xyp2-xym2)//4
xzm1,xzm2 = innest(xmz)[0]
xzp1,xzp2 = innest(xpz)[0]
z1 = (xzp1-xzm1+xzp2-xzm2)//4

r0 = ranges(bots, x0,y0,z1)
#print("cover: ",r0)
l=min(x0,y0,z1)
h = 0
while l>h:
    m = (l+h)//2
    if ranges(bots, x0-m,y0-m,z1-m) == r0: 
        h = m+1 
    else:
        l = m-1
x = x0-m
y = y0-m
z = z1-m
#print("after binary", ranges(bots, x,y,z))    

while ranges(bots, x-1,y-1,z-1) >= r0:
    x-=1
    y-=1
    z-=1
    r = ranges(bots, x,y,z) 
    if r > r0:
        r0 = r
#print("after linear", ranges(bots, x,y,z))    

while ranges(bots, x-1,y,z) >= r0:
    x-=1
    r = ranges(bots, x,y,z) 
    if r > r0:
        r0 = r
#print("after x", ranges(bots, x,y,z))    

while ranges(bots, x,y-1,z) >= r0:
    y-=1
    r = ranges(bots, x,y,z) 
    if r > r0:
        r0 = r
#print("after y", ranges(bots, x,y,z))    
        
while ranges(bots, x,y,z-1) >= r0:
    z-=1
    r = ranges(bots, x,y,z) 
    if r > r0:
        r0 = r
#print("after z", ranges(bots, x,y,z))    

print("Part 2: ", x+y+z)