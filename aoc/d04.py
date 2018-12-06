import datetime
import operator

days = {}
guards = {}
with open("04.in") as f:
    for line in f:
        d = datetime.datetime.strptime(line[1:17],"%Y-%m-%d %H:%M")+datetime.timedelta(0,3600)
        mykey = (d.month,d.day)
        if mykey not in days:
            days[mykey] = []
        mytime = d.hour*60+d.minute-60
        if line[19:] == "falls asleep\n":
            days[mykey].append((mytime,-1))
        elif line[19:] == "wakes up\n":
            days[mykey].append((mytime,1))
        else:
            guards[mykey] = int(line[26:].split()[0])
        
for d in days:
    days[d].sort()

#part one - maximum sleeps
sleep = {}
for d in days:
    g = guards[d]    
    for b,s in days[d]:
        sleep[g] = sleep.get(g,0)+b*s
max_id = max(sleep.items(), key=operator.itemgetter(1))[0]

minutes = [0]*60
for d in guards:
    if guards[d] == max_id:
        ts = days[d]
        for i in range(1,len(ts),2):
            for j in range(ts[i-1][0], ts[i][0]):
                minutes[j] += 1
most = minutes.index(max(minutes))
print(most*max_id)

# part two
sleeps = {}
for g in set(guards.values()):
    sleeps[g] = [0]*60

for d in days:
    g = guards[d]
    ts = days[d]
    for i in range(1,len(ts),2):
        for j in range(ts[i-1][0], ts[i][0]):
            sleeps[g][j] += 1
ms = {g:max(sleeps[g]) for g in guards.values()}
max_id = max(ms.items(), key=operator.itemgetter(1))[0]
best = sleeps[max_id]
max_min = best.index(max(best))
print(max_id*max_min)
