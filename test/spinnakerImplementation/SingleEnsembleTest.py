
import matplotlib.pyplot as plt
from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.2, max_delay=1.0)

# create populations of single neurons of type IF_cond_alpha
t_synE = 1.0
t_synI = 1.0
t_memb = 1.07
vResetInh = -92.0
vResetCO = -102.0
# 'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh
neuronInhLeft = Population(1, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh},
            label="Blocker Left")
neuronInhRight = Population(1, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh},
            label="Blocker Right")
neuronCell = Population(1, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetCO},
            label="Cell Output")

# globally set parameters
# neurons.set({'tau_m':20, 'v_rest':-65}) ...

# initialise records for plotting purposes
neuronCell.record_v()
neuronInhLeft.record_v()
neuronInhRight.record_v()

# create a spike source firing at spike_times
retinaLeft = Population(1, SpikeSourceArray, {'spike_times': [1, 1.2, 1.8]}, label="Retina Left")
retinaRight = Population(1, SpikeSourceArray, {'spike_times': [20]}, label="Retina Right")
# connect them in according to the follwing pattern

excDelay = 0.8
minDelay = 0.2

Projection(retinaLeft, neuronInhLeft, OneToOneConnector(weights=49.5, delays=minDelay), target='excitatory')
Projection(retinaLeft, neuronInhRight, OneToOneConnector(weights=39.5, delays=minDelay), target='inhibitory')
Projection(retinaLeft, neuronCell, OneToOneConnector(weights=39.5, delays=excDelay), target='excitatory')

Projection(retinaRight, neuronInhRight, OneToOneConnector(weights=49.5, delays=minDelay), target='excitatory')
Projection(retinaRight, neuronInhLeft, OneToOneConnector(weights=39.5, delays=minDelay), target='inhibitory')
Projection(retinaRight, neuronCell, OneToOneConnector(weights=39.5, delays=excDelay), target='excitatory')
  
Projection(neuronInhLeft, neuronCell, OneToOneConnector(weights=39.5, delays=minDelay), target='inhibitory')
Projection(neuronInhRight, neuronCell, OneToOneConnector(weights=39.5, delays=minDelay), target='inhibitory')

simTime = 20.0
run(simTime)

# plot results
memPotCO = zip(*neuronCell.get_v())[2]
# print memPotCO
plt.plot(memPotCO)
plt.axis([0.0, simTime*10, -75.0, -40.0])

# memPotInhL = zip(*neuronInhLeft.get_v())[2]
# 
# plt.plot(memPotInhL)
# plt.axis([0.0, simTime*10, -75.0, -40.0])

# memPotInhR = zip(*neuronInhRight.get_v())[2]
# 
# plt.plot(memPotInhR)
# plt.axis([0.0, simTime*10, -75.0, -40.0])
plt.show()


end()

