RA = 1
RB = 2
RC = 3
OPS = ["addr","addi","mulr","muli","banr","bani","borr","bori","setr","seti",\
       "gtir","gtri","gtrr","eqir","eqri","eqrr"]        

def no_change(before, after, regC):
    for i in range(4):
        if i != regC and before[i] != after[i]:
            return False
    return True
 
#Addition
def c_addr(before, after, op):
    if after[op[RC]] != before[op[RA]] + before[op[RB]]:
        return False
    return no_change(before, after, op[RC])

def c_addi(before, after, op):
    if after[op[RC]] != before[op[RA]] + op[RB]:
        return False
    return no_change(before, after, op[RC])


#Multiplication
def c_mulr(before, after, op):
    if after[op[RC]] != before[op[RA]] * before[op[RB]]:
        return False
    return no_change(before, after, op[RC])

def c_muli(before, after, op):
    if after[op[RC]] != before[op[RA]] * op[RB]:
        return False
    return no_change(before, after, op[RC])


#Bitwise AND
def c_banr(before, after, op):
    if after[op[RC]] != before[op[RA]] & before[op[RB]]:
        return False
    return no_change(before, after, op[RC])

def c_bani(before, after, op):
    if after[op[RC]] != before[op[RA]] & op[RB]:
        return False
    return no_change(before, after, op[RC])


#Bitwise OR
def c_borr(before, after, op):
    if after[op[RC]] != before[op[RA]] | before[op[RB]]:
        return False
    return no_change(before, after, op[RC])

def c_bori(before, after, op):
    if after[op[RC]] != before[op[RA]] | op[RB]:
        return False
    return no_change(before, after, op[RC])


#Assignment
def c_setr(before, after, op):
    if after[op[RC]] != before[op[RA]]:
        return False
    return no_change(before, after, op[RC])

def c_seti(before, after, op):
    if after[op[RC]] != op[RA]:
        return False
    return no_change(before, after, op[RC])


#Greater
def c_gtir(before, after, op):
    if op[RA] > before[op[RB]] and after[op[RC]] != 1:
        return False
    if op[RA] <= before[op[RB]] and after[op[RC]] != 0:
        return False
    return no_change(before, after, op[RC])

def c_gtri(before, after, op):
    if before[op[RA]] > op[RB] and after[op[RC]] != 1:
        return False
    if before[op[RA]] <= op[RB] and after[op[RC]] != 0:
        return False
    return no_change(before, after, op[RC])

def c_gtrr(before, after, op):
    if before[op[RA]] > before[op[RB]] and after[op[RC]] != 1:
        return False
    if before[op[RA]] <= before[op[RB]] and after[op[RC]] != 0:
        return False
    return no_change(before, after, op[RC])


#Equal
def c_eqir(before, after, op):
    if op[RA] == before[op[RB]] and after[op[RC]] != 1:
        return False
    if op[RA] != before[op[RB]] and after[op[RC]] != 0:
        return False
    return no_change(before, after, op[RC])

def c_eqri(before, after, op):
    if before[op[RA]] == op[RB] and after[op[RC]] != 1:
        return False
    if before[op[RA]] != op[RB] and after[op[RC]] != 0:
        return False
    return no_change(before, after, op[RC])

def c_eqrr(before, after, op):
    if before[op[RA]] == before[op[RB]] and after[op[RC]] != 1:
        return False
    if before[op[RA]] != before[op[RB]] and after[op[RC]] != 0:
        return False
    return no_change(before, after, op[RC])

def check_all(b, a, c):
    chk = set()
    if c_addr(b,a,c):
        chk.add("addr")
    if c_addi(b,a,c):
        chk.add("addi")
    if c_mulr(b,a,c):
        chk.add("mulr")
    if c_muli(b,a,c):
        chk.add("muli")
    if c_banr(b,a,c):
        chk.add("banr")
    if c_bani(b,a,c):
        chk.add("bani")
    if c_borr(b,a,c):
        chk.add("borr")
    if c_bori(b,a,c):
        chk.add("bori")
    if c_setr(b,a,c):
        chk.add("setr")
    if c_seti(b,a,c):
        chk.add("seti")
    if c_gtir(b,a,c):
        chk.add("gtir")
    if c_gtri(b,a,c):
        chk.add("gtri")
    if c_gtrr(b,a,c):
        chk.add("gtrr")
    if c_eqir(b,a,c):
        chk.add("eqir")
    if c_eqri(b,a,c):
        chk.add("eqri")
    if c_eqrr(b,a,c):
        chk.add("eqrr")
    #print(chk)
    return chk

def load_all(file):
    with open (file) as f:
        lines = [l.strip() for l in f.readlines()]
    samples = []
    i = 0
    while lines[i][:8] == "Before: ":
        b = [int(x) for x in lines[i][9:-1].split(",")]
        c = [int(x) for x in lines[i+1].split()]
        a = [int(x) for x in lines[i+2][9:-1].split(",")]
        # print(b, c, a)
        samples.append((c,b,a))
        i += 4
    program = []
    for j in range(i,len(lines)):
        if lines[j]:
            ns = [int(x) for x in lines[j].split()]
            program.append(ns)
    return samples, program
                   

def part1(sample):
    cnt = 0
    for cba in sample:
        c,b,a = cba
        like = len(check_all(b,a,c))
        if like>=3:
            cnt += 1
    return cnt


def unique(d):
    # horizontal
    for i in range(16):
        s = 0
        for j in range(16):
            s += d.get((i,j),0)
        #print("i{}:{} ".format(i,s), end="")
        if s==1:
            for j in range(16):
                if d.get((i,j),0)==1:
                    return i,j
    # vertical
    for j in range(16):
        s = 0
        for i in range(16):
            s += d.get((i,j),0)
        #print("j{}:{} ".format(i,s), end="")
        if s==1:
            for i in range(16):
                if d.get((i,j),0)==1:
                    return i,j
    # no more
    return None


def get_opcodes(sample):
    codes = [[] for i in range(16)]
    for cba in sample:
        c,b,a=cba
        like = check_all(b,a,c)
        codes[c[0]].append(like)
    #print(codes)
    cs = []
    for i in range(16):
        s0 = codes[i][0]
        for s in codes[i]:
            s0 &= s
        cs.append(s0)
    d = {}
    for k in range(16):
        for mi in range(16):
            if OPS[mi] in cs[k]:
                d[k,mi]=1

    opcodes = {}
    cc = unique(d)
    while cc != None:
        k,mi = cc
        opcodes[k]=OPS[mi]
        for z in range(16):
            d[k,z]=0
            d[z,mi]=0
        cc = unique(d)
    return opcodes


def part2(opcodes, program):
    regs = [0,0,0,0]
    for i,p in enumerate(program):
        oc = opcodes[p[0]] 
        if oc == "addr":
            regs[p[RC]] = regs[p[RA]]+regs[p[RB]]
        elif oc == "addi":
            regs[p[RC]] = regs[p[RA]]+p[RB]

        elif oc == "mulr":
            regs[p[RC]] = regs[p[RA]]*regs[p[RB]]
        elif oc == "muli":
            regs[p[RC]] = regs[p[RA]]*p[RB]

        elif oc == "banr":
            regs[p[RC]] = regs[p[RA]]&regs[p[RB]]
        elif oc == "bani":
            regs[p[RC]] = regs[p[RA]]&p[RB]
            
        elif oc == "borr":
            regs[p[RC]] = regs[p[RA]]|regs[p[RB]]
        elif oc == "bori":
            regs[p[RC]] = regs[p[RA]]|p[RB]
            
        elif oc == "setr":
            regs[p[RC]] = regs[p[RA]]
        elif oc == "seti":
            regs[p[RC]] = p[RA]
        
        elif oc == "gtir":
            regs[p[RC]] = 1 if p[RA] > regs[p[RB]] else 0
        elif oc == "gtri":
            regs[p[RC]] = 1 if regs[p[RA]] > p[RB] else 0           
        elif oc == "gtrr":
            regs[p[RC]] = 1 if regs[p[RA]] > regs[p[RB]] else 0
            
        elif oc == "eqir":
            regs[p[RC]] = 1 if p[RA] == regs[p[RB]] else 0
        elif oc == "eqri":
            regs[p[RC]] = 1 if regs[p[RA]] == p[RB] else 0           
        elif oc == "eqrr":
            regs[p[RC]] = 1 if regs[p[RA]] == regs[p[RB]] else 0
        else:
            print("error: ", p)
    return regs[0]

sample, program = load_all("16.in")

print(part1(sample))
opcodes = get_opcodes(sample)

print(part2(opcodes, program))      
