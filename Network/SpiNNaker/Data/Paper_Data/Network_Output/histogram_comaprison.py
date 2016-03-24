import random
import numpy
from matplotlib import pyplot

no_inh = [344, 447, 1110, 2276, 1740, 517, 160, 159, 162, 283, 705, 1611, 1299, 439, 75, 464]
with_inh = [38, 263, 1052, 3103, 2062, 439, 27, 8, 52, 259, 1090, 2152, 1673, 667, 68, 31]

bins = range(0, 16)

fig = pyplot.figure()
ax = fig.add_subplot(111)


ax.bar(bins, no_inh, alpha=0.5, width=0.5, label='Without blocker neurons', color='r', align='center')
ax.bar(bins, with_inh, alpha=0.5, label='With blocker neurons', color='b', align='center')
ax.legend(loc='upper right')
ax.set_xticks(range(0, 16))

# pyplot.show()

print "No inh SNR = ", (no_inh[3]+no_inh[4]+no_inh[2]+no_inh[11]+no_inh[10]+no_inh[12])/float(sum(no_inh[:2]+no_inh[5:10]+no_inh[13:]))
print "With inh SNR = ", (with_inh[3]+with_inh[4]+with_inh[2]+with_inh[11]+with_inh[10]+with_inh[12])/float(sum(with_inh[:2]+with_inh[5:10]+with_inh[13:]))