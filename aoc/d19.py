ops = {
    "addr": lambda rs, a, b: rs[a] + rs[b],
    "addi": lambda rs, a, b: rs[a] + b,

    "mulr": lambda rs, a, b: rs[a] * rs[b],
    "muli": lambda rs, a, b: rs[a] * b,

    "banr": lambda rs, a, b: rs[a] & rs[b],
    "bani": lambda rs, a, b: rs[a] & b,

    "borr": lambda rs, a, b: rs[a] | rs[b],
    "bori": lambda rs, a, b: rs[a] | b,

    "setr": lambda rs, a, b: rs[a],
    "seti": lambda rs, a, b: a,
    
    "gtir": lambda rs, a, b: 1 if a > rs[b] else 0,
    "gtri": lambda rs, a, b: 1 if rs[a] > b else 0,
    "gtrr": lambda rs, a, b: 1 if rs[a] > rs[b] else 0,
    
    "eqir": lambda rs, a, b: 1 if a == rs[b] else 0,
    "eqri": lambda rs, a, b: 1 if rs[a] == b else 0,
    "eqrr": lambda rs, a, b: 1 if rs[a] == rs[b] else 0}

#FILE = "190.in"
FILE = "19.in"

with open(FILE) as f:
    start = f.readline().split()
    prg = [l.strip().split() for l in f.readlines()]

ipr = int(start[1])
def run(rs):
    ip = rs[ipr]
    while ip < len(prg) and 0<= ip:
        if ip == 13:
            print(rs)
            break
        if len(rs)<6:
            break
        print(ip, rs, prg[ip], end="")
        op, a, b, c = prg[ip]  
        rs = rs[:int(c)]+[ops[op](rs, int(a), int(b))] + rs[int(c)+1:]
        print(rs)
        rs[ipr] += 1
        ip = rs[ipr]
    return rs[0]

#print(run([0,0,0,0,0,0]))
print(run([1,0,0,0,0,0]))




