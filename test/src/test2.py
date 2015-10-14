from pyNN.nest import *

# setup global parameters of the simulator
setup(timestep=0.1, min_delay=2.0)

# create two cells: 

# IF-neuron responding to a spike with a step increse in synaptic conductance and exponential decay
ifcell = create(IF_cond_exp, {'i_offset': 0.11, 'tau_refrac': 3.0, 'v_thresh': -51.0})

# spike source emitting spikes at predetermined periods. It cannot receive input spikes.
times = map(float, range(5, 105, 10))
source = create(SpikeSourceArray, {'spike_times': times})

# connect the cells
connect(source, ifcell, weight=0.006, synapse_type='excitatory', delay=2.0)
 
#set record variables, run simulation and finish
record_v(ifcell, 'ifcell.dat')
run(200.0)
end()