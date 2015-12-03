from pyNN.spiNNaker import *
import matplotlib.pyplot as plt
# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.1, max_delay=1.0)

# create populations of single neurons of type IF_cond_alpha
t_synE = 1.0
t_synI = 1.0
t_memb = 1.07
vResetInh = -92.0
vResetCO = -102.0
# 'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh
neuronInhLeft = Population(1, IF_curr_exp, {},
            label="Blocker Left")
neuronInhRight = Population(1, IF_curr_exp, {},
            label="Blocker Right")
neuronCell = Population(1, IF_curr_exp, {},
            label="Cell Output")

# globally set parameters
# neurons.set({'tau_m':20, 'v_rest':-65}) ...

# initialise records for plotting purposes
neuronCell.record_v()

# create a spike source firing at spike_times
retinaLeft = Population(1, SpikeSourceArray, {'spike_times': [1]}, label="Retina Left")
retinaRight = Population(1, SpikeSourceArray, {'spike_times': [100]}, label="Retina Right")
# connect them in according to the follwing pattern

excDelay = 0.1

Projection(retinaLeft, neuronInhLeft, OneToOneConnector(weights=.95, delays=0.1))
Projection(retinaLeft, neuronInhRight, OneToOneConnector(weights=-.95, delays=0.1))
Projection(retinaLeft, neuronCell, OneToOneConnector(weights=5.0, delays=excDelay))

Projection(retinaRight, neuronInhLeft, OneToOneConnector(weights=.95, delays=0.1))
Projection(retinaRight, neuronInhRight, OneToOneConnector(weights=-.95, delays=0.1))
Projection(retinaRight, neuronCell, OneToOneConnector(weights=.95, delays=excDelay))
  
Projection(neuronInhLeft, neuronCell, OneToOneConnector(weights=-.95, delays=0.1))
Projection(neuronInhRight, neuronCell, OneToOneConnector(weights=-.95, delays=0.1))

simTime = 20.0
run(simTime)

# plot results
memPotCO = zip(*neuronCell.get_v())[2]

plt.plot(memPotCO)
plt.axis([0.0, simTime*10, -75.0, -40.0])
plt.show()


end()

