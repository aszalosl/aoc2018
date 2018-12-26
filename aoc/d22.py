import collections
from enum import Enum

class Region(Enum):
    ROCKY = 1
    WET = 2
    NARROW = 3


def regions(depth,sx,sy,tx,ty):
    rt = {}
    el = {}
    for i in range(sx+1):
        for j in range(sy+1):
            if i == 0 and j == 0:
                gi = 0
            elif i == tx and j == ty:
                gi = 0
            elif j == 0:
                gi = i*16807
            elif i == 0:
                gi = j*48271
            else:
                gi = el[i-1,j]*el[i,j-1]
            el[i,j] = (gi+depth)%20183
            m = el[i,j] % 3
            if m == 0:
                rt[i,j] = Region.ROCKY
            elif m == 1:
                rt[i,j] = Region.WET
            elif m == 2:
                rt[i,j] = Region.NARROW
    return rt


def draw_map(rt, sx, sy):
    for j in range(sy+1):
        for i in range(sx+1):
            if rt[i,j] == Region.ROCKY:
                print(".",end="")
            elif rt[i,j] == Region.WET:
                print("=",end="")
            elif rt[i,j] == Region.NARROW:
                print("|",end="")
        print()


def rl(rt,sx,sy):
    "calculate the risk level"
    risk_level = 0
    for j in range(sy+1):
        for i in range(sx+1):
            if rt[i,j] == Region.WET:
                risk_level += 1
            if rt[i,j] == Region.NARROW:
                risk_level += 2
    return risk_level

## Part 1
## test
#rt = regions(510,10,10,10,10)
#rint(rl(rt,10,10))
## puzzle
# rt = regions(4080,14,785,14,785)
# print(rl(rt,14,785))        # 11843


class Equip(Enum):
    TORCH = 1
    CLIMBING = 2
    NEITHER = 3

def good_at(region,equip):
    if region == Region.ROCKY:
        return equip == Equip.CLIMBING or equip == Equip.TORCH
    if region == Region.WET:
        return equip == Equip.CLIMBING or equip == Equip.NEITHER
    if region == Region.NARROW:
        return equip == Equip.NEITHER or equip == Equip.TORCH
    
def expands(u,v,e,t,rt,times):
    if (u,v) in rt:
        if good_at(rt[u,v],e) and times.get((u,v,e),t+2)>t+1:
            return (t+1,u,v,e)
    return None
            
def code(e):
    if e == Equip.TORCH:
        return "T"
    if e == Equip.CLIMBING:
        return "@"
    if e == Equip.NEITHER:
        return "-"
    
def find_it(tx,ty,mx,my,depth):
    rt = regions(depth,mx,my,tx,ty)
    fringe = []
    times = {}
    fringe.append((0,0,0,Equip.TORCH))
    while fringe:
        fringe.sort(key=lambda x: x[0]) # sort by time
        node = fringe.pop(0)
        # print(node)
        t0,x,y,e = node
        if (x,y,e) not in times or times[x,y,e]>t0:
            times[x,y,e]=t0
            t7 = t0+7
            t8 = t0+8
            # change
            if e != Equip.CLIMBING and good_at(rt[x,y], Equip.CLIMBING) and\
                times.get((x,y,Equip.CLIMBING),t8)>t7:
                    fringe.append((t7,x,y,Equip.CLIMBING))
                    
            if e != Equip.TORCH and good_at(rt[x,y],Equip.TORCH) and\
                times.get((x,y,Equip.TORCH),t8)>t7:
                    fringe.append((t7,x,y,Equip.TORCH))
                    
            if e != Equip.NEITHER and good_at(rt[x,y],Equip.NEITHER) and\
                times.get((x,y,Equip.NEITHER),t8)>t7:
                    fringe.append((t7,x,y,Equip.NEITHER))
    
            # print("({},{}){}={}".format(x,y,code(e),t0), end=" ")
            if (x-1,y) in rt:
                n1 = expands(x-1,y,e,t0,rt,times)
                if n1:
                    fringe.append(n1)
            if (x,y-1) in rt:
                n2 = expands(x,y-1,e,t0,rt,times)
                if n2:
                    fringe.append(n2)
            if (x+1,y) in rt:
                n3 = expands(x+1,y,e,t0,rt,times)
                if n3:
                    fringe.append(n3)
            if (x,y+1) in rt:
                n4 = expands(x,y+1,e,t0,rt,times)
                if n4:
                    fringe.append(n4)
                    
    print(times.get((tx,ty,Equip.TORCH),'-'))


#ind_it(10,10,16,16,510)
find_it(14,785,60,850,4080) # 1078
