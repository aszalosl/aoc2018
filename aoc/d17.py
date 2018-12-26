# -*- coding: utf-8 -*-
#FILE = "170.in"
FILE = "17.in"

clay = {}
with open(FILE) as f:
    for l in f:
        ls = [x.strip() for x in l.split(",")]
        intv = ls[1][2:].split('.')
        o = int(ls[0][2:])
        intb, inte = int(intv[0]), int(intv[-1])
        if ls[0][0] == 'x':
            for i in range(intb,inte+1):
                clay[o,i]="#"
        else:
            for i in range(intb,inte+1):
                clay[i,o]="#"
                
def limits():
    xs = [xy[0] for xy in clay]
    ys = [xy[1] for xy in clay]
    return min(xs), min(ys), max(xs), max(ys)


def draw(xb,xe,ye):
    for y in range(-1,ye):
        print("{:4}".format(y),end=" ")
        for x in range(xb, xe+1):
            if (x,y) in clay:
                print(clay[x,y], end="")
            else:
                print(".", end="")
        print()

x_l,y_l,x_h, y_h = limits()
print("min:", y_l)

def walls(x,y):
    # go left
    xl = x
    while clay.get((xl,y),'.') in ['|','.'] and clay.get((xl,y+1),'.') in ['#','~']:
        xl -= 1
    # go right
    xr = x
    while clay.get((xr,y),'.') in ['|','.'] and clay.get((xr,y+1),'.') in ['#','~']:
        xr += 1   
    return xl,xr


def closed(xl,xr,y):
    return clay.get((xl,y),'.')=="#" and clay.get((xr,y),'.')=="#"


def fill_level(x,y,fountains):
    xl,xr = walls(x,y)
    if xl<xr:
        if closed(xl,xr,y):
            #print("fill ", y)
            for i in range(xl+1,xr):
                clay[i,y] = '~'
        else:
            if clay.get((xl,y),'.') != "#":     # open at left
                if (xl,y) not in fountains:
                    fountains.append((xl,y))
                        
            if clay.get((xr,y),'.') != "#":     # open at rigth
                if (xr,y) not in fountains:
                    fountains.append((xr,y))
                
            for i in range(xl+1,xr):
                clay[i,y] = '|'
            #print("half-fill",y,"  F:", fountains)
    

def go_down(x,y, y_h,fountains):       
    while (x,y) not in clay:
        clay[x,y] = "|"
        y += 1
        if y > y_h:
            return y
    return y-1
    
fountains = [(500,1)]
#fountains = [(515,89)]
def calculate():
    while fountains:
        f0 = fountains.pop(0)
        x,y = f0
        # go down
        y = go_down(x,y,y_h,fountains)
        xl,xr=walls(x,y)
        if 0<y<=y_h: #and closed(xl,xr,y):
            fill_level(x,y,fountains)
            while clay.get((x,y),'.')=='~':
                y -= 1
                fill_level(x,y,fountains)
        
        
calculate()
#draw(x_l-3,x_h+3,y_h+2)
#draw(480,530,70)
print(sum([1 for i in clay if clay[i] in ['~','|'] and i[1]>=y_l]))
#31790 sok
print(sum([1 for i in clay if clay[i] == '~']))
