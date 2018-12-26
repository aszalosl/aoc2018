# -*- coding: utf-8 -*-

#FILE="240.in"
FILE="24.in"
EXTRA = 61

def weak_imm(line):
    weak, immune = [], []
    for l in line.split(';'):
        ls = l.split()
        if ls[0]=="weak":
            for w in ls[2:]:
                weak.append(w)
        elif ls[0]=="immune":
            for w in ls[2:]:
                immune.append(w)
    return weak, immune

imm = {}
inf = {}
    
with open(FILE) as f:
    id = 1
    for l in f:
        if l.strip() == "Immune System:":
            state = 1
        elif l.strip() == "Infection:":
            state = 2
        elif len(l.strip()) > 2:
            lw = l.split()
            gr = {}
            gr['unit'] = int(lw[lw.index("units")-1])
            gr['hp'] = int(lw[lw.index("hit")-1])
            gr['damage'] = int(lw[lw.index("damage")-2])
            if state == 1:
                gr['damage'] += EXTRA
            gr['dtype'] = lw[lw.index("damage")-1]
            gr['init'] = int(lw[lw.index("initiative")+1])
            gr['weak']=[]
            gr['immune'] = []
            if l.find("(")>=0:
                l0 = l[l.index("(")+1:l.index(")")].replace(",", "")
                gr['weak'], gr['immune'] = weak_imm(l0)
            if state == 1:
                imm[id]=gr
            else:
                inf[id]=gr
            id +=1

def danger(attack, defense):
    if attack['dtype'] in defense['weak']:
        return 2
    if attack['dtype'] in defense['immune']:
        return 0
    return 1
 
       
def eff_power(gr):
    return gr['unit']*gr['damage']


def target(my, enemy):
    z = [(eff_power(my[i]), my[i]['init'], i) for i in my]
    z.sort(reverse=True)
    a = []
    targ = []
    for attack in z:
        my_gr = my[attack[2]]
        
        y = [(danger(my_gr,enemy[g])*eff_power(my_gr),eff_power(enemy[g]),\
              enemy[g]['init'],g) for g in enemy\
              if danger(my_gr,enemy[g])> 0 and g not in targ]
        if y:
            y.sort(reverse=True)
            #print("y:", y)
            #print(attack[2],y[0][0],y[0][-1])
            a.append((my_gr['init'], attack[2], y[0][-1]))
            targ.append(y[0][-1])
    return a

#print(imm,inf)
def deal(ds,imm,inf):
    #print("deal: ", ds)
    tie = False
    was = []
    for d in ds:
        _, att, defe = d
        
        if defe in imm and imm[defe]['unit']>0:
            
            eep = danger(inf[att],imm[defe])*eff_power(inf[att])
            u = eep //imm[defe]['hp']
            #print("{}->{} / {} X {}".format(att, defe, eep, min(u,imm[defe]['unit'])))
            if u > 0:
                tie = True
            imm[defe]['unit'] -= min(u,imm[defe]['unit'])
            was.append(defe)
        elif defe in inf and inf[defe]['unit']>0:
            eep = danger(imm[att],inf[defe])*eff_power(imm[att])
            u = eep//inf[defe]['hp']
            #print("{}->{} / {} X {}".format(att, defe, eep, min(u,inf[defe]['unit'])))
            if u> 0:
                tie = True
            inf[defe]['unit'] -= min(u,inf[defe]['unit'])
            was.append(defe)
    return tie


while imm and inf:
#    print("Immune: ", end="")        
#    for g in imm:
#        print("#{} - {} units  ".format(g, imm[g]['unit']), end="")
#    print("\nInfection: ", end="")
#    for g in inf:
#        print("#{} - {} units  ".format(g, inf[g]['unit']),end="")
#    print()          
    t = target(imm,inf) + target(inf,imm)
    t.sort(reverse=True)
    # print("target: ", t)
    if not deal(t,imm,inf):
        break
    #print("\n")
    to_del1 = []
    for g in imm:
        if imm[g]['unit']<=0:
            to_del1.append(g)
    for g in to_del1:
        del imm[g]

    to_del2 = []
    for g in inf:
        if inf[g]['unit']<=0:
            to_del2.append(g)
    for g in to_del2:
        del inf[g]
    print(".",end="")
print()
#print(imm,inf)    
print("Immune: ", sum([imm[g]['unit'] for g in imm]))
print("Infect: ", sum([inf[g]['unit'] for g in inf]))

#print("Answer 1:", summa) #28982 too high
if imm == {}:
    print("immune lost")