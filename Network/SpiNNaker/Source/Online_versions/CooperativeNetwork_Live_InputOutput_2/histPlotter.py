import numpy as np
import matplotlib.pyplot as plt
from SimulationAndNetworkSettings import maxDisparity

disps = []

with open('dipsarities.txt', 'r') as f:
    disps = [int(x) for x in f.readlines()]

print disps

dispcounts = [0]*maxDisparity
for x in range(0, len(disps)):
    dispcounts[disps[x]-1] += 1      

print dispcounts

disparityValues = np.arange(maxDisparity)
width = 0.7     

ax = plt.axes()
ax.set_xticks(disparityValues + (width / 2))
ax.set_xticklabels(dispcounts)

plt.bar(disparityValues, dispcounts, width, color='b')
plt.show()