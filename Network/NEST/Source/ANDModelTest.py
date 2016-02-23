from pyNN.nest import *
from pyNN.utility import normalized_filename
from numpy import arange
import matplotlib.pyplot as plt


timeStep = 0.2
minDelay = timeStep
maxDelay = 10.0 * minDelay
simTime = 20.0
spikeTimes = [3]

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=timeStep, min_delay=minDelay, max_delay=maxDelay)

# create populations of single neurons of type IF_cond_alpha
neuronInhLeft = Population(1, IF_curr_exp(), label="Inhibitor Left")
neuronInhRight = Population(1, IF_curr_exp(), label="Inhibitor Right")
neuronCell = Population(1, IF_curr_exp(), label="Cell Output")

# globally set parameters
# neurons.set({'tau_m':20, 'v_rest':-65}) ...

# initialise records for plotting purposes
all_neurons = neuronInhLeft + neuronInhRight + neuronCell
all_neurons.record('v')
neuronCell.record('spikes', 'v')
# neuronInhLeft.record('spikes', 'v')
# neuronInhRight.record('spikes', 'v')

all_neurons.set(tau_syn_E=2.0)
all_neurons.set(tau_syn_I=2.0)
all_neurons.set(tau_m=2.07)
neuronInhLeft.set(v_reset=-84.0)
neuronInhRight.set(v_reset=-84.0)
neuronCell.set(v_reset=-90.0)
# create a spike source firing at spike_times
retinaLeft = Population(1, SpikeSourceArray(spike_times=[3]), label="Spike Source Left")
retinaRight = Population(1, SpikeSourceArray(spike_times=[1]), label="Spike Source Right")
# connect them in according to the follwing pattern

excDelay = 1.6
stdDelay = minDelay

Projection(retinaLeft, neuronInhLeft, OneToOneConnector(), StaticSynapse(weight=22.5, delay=stdDelay))
Projection(retinaLeft, neuronInhRight, OneToOneConnector(), StaticSynapse(weight=-22.5, delay=stdDelay))
Projection(retinaLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=20.5, delay=excDelay))

Projection(retinaRight, neuronInhRight, OneToOneConnector(), StaticSynapse(weight=22.5, delay=stdDelay))
Projection(retinaRight, neuronInhLeft, OneToOneConnector(), StaticSynapse(weight=-22.5, delay=stdDelay))
Projection(retinaRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=20.5, delay=excDelay))

Projection(neuronInhLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=-20.5, delay=stdDelay))
Projection(neuronInhRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=-20.5, delay=stdDelay))

run(simTime)

# plot results
memPot = [voltage for vL in neuronCell.get_data().segments[0].filter(name='v') for voltage in vL]

plt.plot(arange(0.0, simTime+timeStep, timeStep), memPot)
for s in spikeTimes:
    plt.plot([s, s], [-40, -100], 'k-', lw=2)
plt.axis([0.0, 10, -100.0, -40.0])
plt.xticks(arange(0.0, simTime+timeStep, timeStep*5))
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.show()


print "Totally: {0} spikes Cell Output".format(len(neuronCell.get_data().segments[0].spiketrains[0]))
print "Totally: {0} spikes Left Inhibitor".format(len(neuronInhLeft.get_data().segments[0].spiketrains[0]))
print "Totally: {0} spikes Right Inhibitor".format(len(neuronInhRight.get_data().segments[0].spiketrains[0]))

end()

