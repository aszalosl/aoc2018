d_freq=[]
with open("01.in") as file:
    for sor in file:
        d_freq.append(int(sor))

print(sum(d_freq))
freq=set()
nincs_meg = True 
act_fr = 0
while nincs_meg:
    for i in d_freq:
        freq.add(act_fr)
        act_fr += i
        if act_fr in freq:
            print(act_fr)
            nincs_meg=False
            break
        else:
            freq.add(act_fr)