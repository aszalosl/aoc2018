#with open("09.in") as f:
#    for l in f:
#        s = l.split()
#p = int(s[0])
#w = int(s[6])

def count(p,w):
    ms = [0]
    j = 0
    ps = [0]*p
    for i in range(1,w+1):
        if i%23 == 0:
            j = (j-7) % len(ms)
            ps[i%p]+=i+ms[j]
            ms=ms[:j] + ms[j+1:]
        else:
            j = (j+2) % len(ms)
            ms = ms[:j] + [i] + ms[j:]
        #print(ms)
    return max(ps)

#print(count(9,25)) # 32
#print(count(10,1618)) # 
#print(count(13,7999)) # 
#print(count(17,1104)) # 
#print(count(21,6111)) # 
#print(count(30,5807)) #
print(count(458,71307)) #398048
print(count(458,7130700)) #398048



