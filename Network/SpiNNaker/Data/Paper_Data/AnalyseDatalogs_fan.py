import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

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


ordered_disps = [0]*16
for d in disps:
	ordered_disps[d] += 1
print(ordered_disps)
print(sum(ordered_disps))
print(len(ordered_disps))
# print(sum(ordered_disps[:8]), sum(ordered_disps[9:]))

# ax.scatter(range(0, len(disps)), disps)


ax.set_ylabel("Number of events")
ax.set_xlabel("Disparity")

ax.bar(range(len(ordered_disps)), ordered_disps, width=0.8, align='center')
ax.set(xticks=range(len(ordered_disps)), xlim=[-1, len(ordered_disps)])


# Generate some test data
# x = range(0, len(disps))
# y = disps


# heatmap, xedges, yedges = np.histogram2d(y, x, bins=(16, 100))
# # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

# im = ax.imshow(heatmap, extent=[0,10,0,16], aspect=0.4, interpolation='none',  origin='lower')
# ax.set_xlabel("Time in s")
# ax.set_ylabel("Disparity")

# ax.set_aspect(0.5)

# cbar = plt.colorbar(im,fraction=0.046, pad=0.03)
# cbar.set_label('Number of events per time slot (0.1 s)', rotation=270)
# cbar.ax.get_yaxis().labelpad = 15


plt.show()	




