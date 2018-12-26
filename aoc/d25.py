# -*- coding: utf-8 -*-
import collections
#FILE="250.in"
FILE="25.in"

## load data
points = []
with open(FILE) as f:
    for l in f:
        points.append([int(x) for x in l.split(',')])
ps = len(points)
for i in range(ps):
    points[i].append(i) # representative
    points[i].append(0) # height


def close(i,j):
    d = 0
    for k in range(4):
        d += abs(points[i][k]-points[j][k])
    return d<=3

def representative(i):
    while points[i][-2] != i:
        iold = i
        i = points[i][-2]
        points[iold][-2] = points[i][-2]
    return i


def join(i,j):
    x = representative(i)
    y = representative(j)
    if x != y:
        if points[x][-1]>points[y][-1]:
            points[y][-2] = x
        else:
            points[x][-2] = y
    
for i in range(1,ps):
    for j in range(i):
        if close(i,j):
            join(i,j)


z = collections.Counter([representative(i) for i in range(ps)])
print(len(z))