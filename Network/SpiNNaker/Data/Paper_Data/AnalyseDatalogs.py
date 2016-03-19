import matplotlib.pyplot as plt

fileName = "Fan_dataset2_rectifiedCoordinates_datalog.txt"

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

ordered_disps = [0]*17
for d in disps:
	ordered_disps[d] += 1

print(ordered_disps)	

# print(secList)
# print(sum(secList))	

plt.show()