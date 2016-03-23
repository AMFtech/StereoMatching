import matplotlib.pyplot as plt
import numpy as np

# fileName = "NSTlogo_datalog_1s.txt"
fileName = "NSTlogo_manual_42x25_datalog.txt"

evts = []
with open(fileName, 'rb') as allEvents:
	for line in allEvents:
		evts.append([int(x) for x in line.split()])

secList = [0]*10
for e in evts:
	secList[int(e[0]*0.0002)] += 1 

disps = [x[3] for x in evts]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.hist(disps, bins=15)

ordered_disps = [0]*16
for d in disps:
	ordered_disps[d] += 1
print(ordered_disps)

# ax.plot([0, len(disps)],[3, 3], '--', c='cyan')
# ax.plot([0, len(disps)],[8, 8], '--', c="green")
# ax.plot([0, len(disps)],[12, 12], '--', c="orange")
# ax.scatter(range(0, len(disps)), disps)


ax.set_ylabel("Number of events")
ax.set_xlabel("Disparity")
# ax.annotate('N', 
#              xy=(2, 12.5),  
#              xycoords='data',
#              textcoords='offset points')

# ax.annotate('S', 
#              xy=(2, 8.5),  
#              xycoords='data',
#              textcoords='offset points')

# ax.annotate('T', 
#              xy=(2, 3.5),  
#              xycoords='data',
#              textcoords='offset points')

# ax.set_xlim([0, len(disps)])

# print(float(sum(disps))/len(disps))
print(len([x for x in disps if x > 10]))
print(len([x for x in disps if x < 10 and x > 6]))
print(len([x for x in disps if x < 6]))
# print(secList)
# print(sum(secList))	

plt.show()



