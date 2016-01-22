import pyNN.nest as sim
from pyNN.utility import normalized_filename
from numpy import arange
import matplotlib.pyplot as plt

timeStep = 0.2
minDelay = timeStep
maxDelay = 10.0 * minDelay
simTime = 10.0
spikeTimes = [5]

sim.setup(timestep=timeStep, min_delay=minDelay, max_delay=maxDelay)

neurons = sim.Population(1, sim.IF_curr_exp())
spike_sourceE = sim.Population(1, sim.SpikeSourceArray(spike_times=spikeTimes))
# spike_sourceI = sim.Population(1, sim.SpikeSourceArray(spike_times=[33.1, 330.2, 330.3]))

connection = sim.Projection(spike_sourceE, neurons, sim.OneToOneConnector(), sim.StaticSynapse(weight=22.5, delay=minDelay))
# connection = sim.Projection(spike_sourceI, neurons, sim.OneToOneConnector(), sim.StaticSynapse(weight=-22.5, delay=0.1))
# electrode = sim.DCSource(start=2.0, stop=92.0, amplitude=0.014)
# electrode.inject_into(neurons)

neurons.record(['v'])  #, 'u'])
neurons.set(tau_syn_E=2.0)
neurons.set(tau_syn_I=2.0)
neurons.set(tau_m=2.07)
neurons.set(v_reset=-90.0)

sim.run(simTime)

filename = normalized_filename("Results", "test", "pkl", "nest", sim.num_processes())
# neurons.write_data(filename, annotations={'script_name': __file__})

memPot = [voltage for vL in neurons.get_data().segments[0].filter(name='v') for voltage in vL]

plt.plot(arange(0.0, simTime+timeStep, timeStep), memPot)
for s in spikeTimes:
    plt.plot([s, s], [-40, -100], 'k-', lw=2)
plt.axis([0.0, 10, -100.0, -40.0])
plt.xticks(arange(0.0, simTime+timeStep, timeStep*5))
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.show()

sim.end()
