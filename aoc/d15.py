#import ipdb
FILE="15.in"
NBS = [(-1,0),(1,0),(0,-1),(0,1)]  # neighbours
APG = -3  #attack power of a Goblin

def read_problem(file):
    "read from the given file"
    c = {}
    with open(file) as f:
        for j,line in enumerate(f):
            for i,ch in enumerate(line):
                if ch=="." or ch=="G" or ch=="E":
                    c[i,j]=ch
    return c


def draw(x,y,c,d):
    "for testing"
    for j in range(y):
        for i in range(x):
            if (i,j) in d:
                print(d[i,j],end="")
            elif (i,j) in c:
                print(c[i,j],end="")
            else:
                print("#",end="")
        print()
    print()


def elf_goblin(hp):
    "Where are the fighters?"
    return [x for x in hp]


def final(hp,c):
    "game over?"
    e = 0
    g = 0
    for x in hp:
        if c[x] == 'E':
            e += 1
        elif c[x] == 'G':
            g += 1
        else:
            print("Error @ ", x,": ", c[x])
    return e*g == 0

def vect_add(p,q):
    return p[0]+q[0],p[1]+q[1]

def next_to(type, c, hp):
    "find the positions next to the 'type' enemy"
    ps = set() # set of positions
    for xy in hp:
        if c[xy] == type:
            for d in NBS:
                if c.get(vect_add(xy,d),'-') == '.':
                    ps.add(vect_add(xy,d))
    return ps


def reachable(p0,ps,c):
    "Which position of ps is reachable from p0?"
    seen={}
    was = set()
    min_l=-1
    to_check = [(p0,0)]
    was.add(p0)
    while to_check:
        p,l = to_check.pop(0)
        if p in ps:
            if min_l == -1:
                min_l = l
            if l == min_l:
                seen[p]=l
        if min_l>=0 and l>min_l:
            return seen
        for d in NBS:
            q = vect_add(p,d)
            if c.get(q,'-') == '.' and q not in was:
                to_check.append((q,l+1))
                was.add(q)  
    return seen


def target(p,ps,c):
    "Where to go from p?"
    #print("call from target", p)
    seen = reachable(p,ps,c)
    if seen:
        #print(p,    "t - seen: ", seen)
        r = sorted([(q[1],q[0]) for q in seen])
        #print("r", r)
        return r[0][1],r[0][0]
    else:
        return None


def direction(p,t,c):
    "Where to go from p to t?"
    ns=[vect_add(p,d) for d in NBS] # neighbour of p
    #print("call from dir", ns)
    seen=reachable(t,ns,c)
    #print("d-seen:", seen)
    dir = sorted([(q[1],q[0]) for q in seen])[0]
    #print(dir)
    return dir[1],dir[0]


def in_contact(p,c,enemy):
    l = []
    for d in NBS:
        q=vect_add(p,d)
        if c.get(q,'-') == enemy:
            l.append((hp[q],q[1],q[0]))
    return sorted(l)
    
def move_one(p,c,ape):
    "Move the fighter @ p" 
    if c[p] == '.':
        return
    global hp
    enemy = 'G' if c[p] == 'E' else 'E'
    contacted = in_contact(p,c,enemy)
    if not contacted:
        t = target(p,next_to(enemy,c,hp),c)
        if t is not None:
            d = direction(p,t,c)
            c[d] = c[p]
            c[p] = '.'
            hp[d] = hp[p]
            del hp[p]
        else:
            d = p
    else:
        d = p
    contacted = in_contact(d,c,enemy)
    if contacted: 
        t = contacted[0]
        if c[t[2],t[1]] == "E":
            hp[t[2],t[1]] += APG
        else:
            hp[t[2],t[1]] += ape
        if hp[t[2],t[1]] <= 0:
            c[t[2],t[1]] = '.'
            del hp[t[2],t[1]]


def full_round(c,hp,ape):
    ge = elf_goblin(hp)
    geo = sorted([(x[1],x[0]) for x in ge])
    for i,f in enumerate(geo):
        fast = move_one((f[1],f[0]),c,ape)
        if final(hp,c) and i<len(geo)-1:
            return False
    else:
        return True


def size(c):
    mx = max([xy[0] for xy in c])
    my = max([xy[1] for xy in c])
    return mx+2,my+2


def process(file,ape):
    global c
    global hp
    c = read_problem(file)
    mx, my = size(c)
    elves = sum(1 for p in c if c[p]=='E')
    #draw(mx,my,c,{})
    #ipdb.set_trace()
    hp = {p:200 for p in c if c[p] == 'E' or c[p] == 'G'}
    i = 0
    #draw(mx,my,c,{})
    while not final(hp,c):
        full = full_round(c,hp,ape)
        if full:
            i += 1
        #print(i,hp)
        #draw(mx,my,c,{})
    #print(hp)
    z = sum([hp[p] for p in hp])
    draw(mx,my,c,{})
    if len(hp)<elves:
        print("Not enough!", end=" ")
    print("{}={}*{}, {}/{}\n".format(i*z,i,z, len(hp),elves))
    return i*z        

# Part 1
##assert process("152.in",-3) == 27730
##assert process("153.in",-3) == 36334
##assert process("154.in",-3) == 39514
##assert process("155.in",-3) == 27755
##assert process("156.in",-3) == 28944
#process('15.in',-3)
# Part 2
##assert process("158.in",-15) ==4988
##assert process("158.in",-14) ==4864
##assert process("159.in",-4) ==31284
##assert process("159.in",-3) ==39514
##assert process("15a.in",-15) ==3478
##assert process("15a.in",-14) ==2788
##assert process("15b.in",-12) ==6474
##assert process("15b.in",-11) ==6030
##assert process("15c.in",-34) ==1140
##assert process("15c.in",-33) ==1155
process('15.in',-20) # OK or less
##process('15.in',-10) # more
##process('15.in',-15) # more
##process('15.in',-17) # more
##process('15.in',-18) # more
##process('15.in',-19) # more

