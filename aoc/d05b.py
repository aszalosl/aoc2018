import string

def to_delete(a,b):
    return not a is None and (a != b) and (a.upper()==b.upper())

def react(s,skip):
    ls = len(s)
    other = [None]*ls
    mo = 0
    ms = 0
    while True:
        if ms == len(s):
            return mo
        elif s[ms].lower() == skip:
            ms += 1
        elif to_delete(other[mo], s[ms]):
            ms += 1
            mo -= 1
        else:
            mo += 1
            other[mo]=s[ms]
            ms += 1
        #print(other[0:mo+1],s[ms:])

with open("05.in") as f:
    s0 = f.readline().strip()
#s0 = "dabAcCaCBAcCcaDA"
s = [*s0]
print(react(s, None))


all = []
for i in list(string.ascii_lowercase):
    z = react(s, i)
    all.append(z)
    print(i,z)
print(min(all))
