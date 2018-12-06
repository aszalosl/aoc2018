import string
def react(s):
    change = True
    while change:
        change=False
        for i in range(len(s)-1):
            a = s[i]
            b = s[i+1]
            if (a != b) and (a.upper()==b.upper()):
                s[i] = "*"
                s[i+1] = "*"
                change = True
        s = [i for i in s if i != "*"]
    return len(s)

with open("05.in") as f:
    s0 = f.readline().strip()
#s0 = "dabAcCaCBAcCcaDA"
s = [*s0]
print(react(s))

all = []
for i in list(string.ascii_lowercase):
    s1 = [j for j in s if j != i and j != i.upper()]
    z = react(s1)
    all.append(z)
    #print(i,z)
print(min(all))
