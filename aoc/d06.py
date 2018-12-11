import collections

# test
# REGION = 32
# FILE = "060.in"
# real
REGION = 1e4
FILE = "06.in"


def distance(x,y,i):
    return abs(x-xy[i][0])+abs(y-xy[i][1])

xy = []
with open(FILE) as f:
    for line in f:
        l2 = line.replace(",","")
        pair = [int(x) for x in l2.split()]
        xy.append(pair)
xyl = len(xy)
#print(xy)

xs = [p[0] for p in xy]
ys = [p[1] for p in xy]
xl = min(xs)
xh = max(xs)
yl = min(ys)
yh = max(ys)

labels = {}
counter=0 # for part #2
for i in range(xl,xh+1):
    for j in range(yl,yh+1):
        ds = sorted([(distance(i,j,k),k) for k in range(xyl)])
        if sum([d for d,_ in ds]) < REGION:
            counter += 1
        if ds[0][0] < ds[1][0]: # unique minimal
            labels[i,j] = ds[0][1]
border = {labels[x,y] for (x,y) in labels if x==xl or x==xh or y==yl or y==yh}
inner = [labels[k] for k in labels if labels[k] not in border]
cs = collections.Counter(inner)
print(max(cs.values()),"\n", counter)
