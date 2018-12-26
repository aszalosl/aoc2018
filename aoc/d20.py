from collections import defaultdict

W=1 
S=2 
E=4
N=8
MUCH = 1000000

def discover(line):
    x,y = 0,0
    edge = defaultdict(int)
    stack = []
    for c in line:
        if c == 'W':
            edge[x,y] |= W
            x-=1
            edge[x,y] |= E
        elif  c == 'E':
            edge[x,y] |= E
            x+=1
            edge[x,y] |= W
        elif  c == 'S':
            edge[x,y] |= S
            y+=1
            edge[x,y] |= N
        elif  c == 'N':
            edge[x,y] |= N
            y-=1
            edge[x,y] |= S
        elif  c == '(':
            stack.append((x,y))
        elif  c == ')':
            _ = stack.pop()
        elif  c == '|':
            x,y = stack[-1]
    return edge

def dijkstra(edge):
    distance = {}
    for xy in edge:
        distance[xy]=MUCH
    #distance[0,0]=0
    queue = [((0,0),0)]
    while queue:
        xy,d0 = queue.pop(0)
        #print(xy,d0)
        d = distance[xy]
        if d0<d:
            distance[xy]=d0
            x,y = xy
            d1 = d0+1
            if edge[xy] & W:
                queue.append(((x-1,y),d1))
            if edge[xy] & E:
                queue.append(((x+1,y),d1))
            if edge[xy] & N:
                queue.append(((x,y-1),d1))
            if edge[xy] & S:
                queue.append(((x,y+1),d1))
    answer1 = max([distance[i] for i in distance])
    answer2 = sum([1 for i in distance if distance[i]>=1000])
    return answer1,answer2

def draw(edge,x1,x2,y1,y2):
    for y in range(y1,y2+1):
        for x in range(x1,x2+1):
            print(" {:2} ".format(edge.get((x,y),"?")), end='')
        print()

## test
#line = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"
## puzzle
with open("20.in") as f:
    line = f.readline()[1:-2]
#print(">",line,"<")        

edge = discover(line)
#draw(edge,-3,3,-3,4)
#print(edge)    
print(dijkstra(edge))


# ?   ?   ?   ?   ?    6   3 
# ?   ?   ?   ?   ?   10  10 
# ?    6   5   5   5   9  10 
###########################
#?   10 # 6 | 1 # 6   3  10
##########-################ 
# 6  13 #15 # 5 #15  15   9 
#14   3 #12 # 5 #11  10   2 
#10  12 # 5 # 5 # 9  12   9 
# 8  ?  #?  #?  #?   ?   ?  