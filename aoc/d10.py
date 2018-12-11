# position=<-31684, -53051> velocity=< 3,  5>
# 0123456789 123456789 123456789 123456789 123
# position=< 9,  1> velocity=< 0,  2>)
points =[]
# test
#with open("100.in") as f:
#    for l in f:
#        x = int(l[10:12])
#        y = int(l[13:16])
#        u = int(l[28:30])
#        v = int(l[31:34])
#        points.append((x,y,u,v))
# real
with open("10.in") as f:
    for l in f:
        x = int(l[10:16])
        y = int(l[17:24])
        u = int(l[36:38])
        v = int(l[39:42])
        # print(x,y,u,v)
        points.append((x,y,u,v))

def xys(i):
    l = []
    for x,y,u,v in points:
        l.append((x+u*i,y+v*i))
    return l

def limits(l):
    xs = [p[0] for p in l]
    ys = [p[1] for p in l]
    return (min(xs), max(xs), min(ys), max(ys))
sizes = []
for i in range(11000):
    l = xys(i)
    xl,xh,yl,yh = limits(l)
    sizes.append(xh-xl+yh-yl)
    if 0==i%100:
        print(".",end   ="")

i = sizes.index(min(sizes))
print(i)
l = xys(i)
xl,xh,yl,yh = limits(l)
print(xl,xh, yl, yh)
for k in range(yl,yh+1):
    for n in range(xl, xh+1):
        if (n,k) in l:
            print("*", end='')
        else:
            print(".", end='')
    print()

# print(points)

