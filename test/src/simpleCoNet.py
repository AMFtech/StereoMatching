from pyNN.nest import *
from pyNN.utility import normalized_filename

####### Network Parameters #########
dimensionRetinaX = 5
dimensionRetinaY = 5
  
radiusInhibition = 2
radiusExcitation = 2
disparityMin = 0
disparityMax = 3

#####################################

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.1, max_delay=5.0)

# create population of network neurons layer by layer
#for layer in range(0, dimensionRetinaY):
    
oneNeuralLayer = Population((dimensionRetinaX, dimensionRetinaX), IF_cond_alpha(), label="Layer 0")

# globally set parameters
# neurons.set({'tau_m':20, 'v_rest':-65}) ...

# initialise records for plotting purposes
oneNeuralLayer.record('v')

# create a spike sources firing at spike_times
retinaLeft = Population(dimensionRetinaX, SpikeSourceArray(spike_times=[30.]), label="Left Retina")
retinaRight = Population(dimensionRetinaX, SpikeSourceArray(spike_times=[30.]), label="Right Retina")

# connect neurons
Projection(retinaLeft, neuronMid, OneToOneConnector(), StaticSynapse(weight=0.5), receptor_type='excitatory')
Projection(retinaRight, neuronInh, OneToOneConnector(), StaticSynapse(weight=0.9, delay=4.5), receptor_type='inhibitory')
Projection(neuronMid, neuronExc, OneToOneConnector(), StaticSynapse(weight=0.1, delay=4.5), receptor_type='excitatory')

Projection(spike_source, neuronInh, OneToOneConnector(), StaticSynapse(weight=0.5, delay=3.0), receptor_type='excitatory')

run(100.0)

# plot results
filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
all_neurons.write_data(filename, annotations={'script_name': __file__})

from pyNN.utility.plotting import Figure, Panel
figure_filename = filename.replace("pkl", "png")
Figure(
    Panel(neuronMid.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[neuronMid.label], yticks=True, ylim=(-66, -48)),
    Panel(neuronInh.get_data().segments[0].filter(name='v')[0],
          data_labels=[neuronInh.label], yticks=True, ylim=(-100, 60)),
    Panel(neuronExc.get_data().segments[0].filter(name='v')[0],
          data_labels=[neuronExc.label], yticks=True, ylim=(-75, -40)),
    title="1Exc1Inh",
    annotations="Simulated with NEST"
).save(figure_filename)
print(figure_filename)

end()

