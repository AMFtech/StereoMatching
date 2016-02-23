import numpy as np
import matplotlib.pyplot as plt
from SimulationAndNetworkSettings import maxDisparity, experimentName

disps = []

with open('{0}_datalog.txt'.format(experimentName), 'r') as f:
    disps = [int(x.split()[3]) for x in f.readlines()]

print disps

dispcounts = [0]*(maxDisparity+1)
for x in range(0, len(disps)):
    dispcounts[disps[x]] += 1      

print dispcounts

disparityValues = np.arange(maxDisparity+1)
width = 0.7     

ax = plt.axes()
ax.set_xticks(disparityValues + (width / 2))
ax.set_xticklabels(range(0, maxDisparity+1))

plt.bar(disparityValues, dispcounts, width, color='b')
plt.show()