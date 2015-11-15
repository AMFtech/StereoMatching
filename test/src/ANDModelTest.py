from pyNN.nest import *
from pyNN.utility import normalized_filename
from matplotlib.pyplot import xlabel

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.01, min_delay=0.1, max_delay=50.0)

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
neuronInhLeft.record('spikes')
neuronInhRight.record('spikes')

all_neurons.set(tau_syn_E=1.0)
all_neurons.set(tau_syn_I=1.0)
all_neurons.set(tau_m=1.07)
neuronInhLeft.set(v_reset=-92.0)
neuronInhRight.set(v_reset=-92.0)
neuronCell.set(v_reset=-102.0)
# create a spike source firing at spike_times
retinaLeft = Population(1, SpikeSourceArray(spike_times=[30, 31, 32, 33, 34, 35, 36, 37, 38, 39]), label="Spike Source Left")
retinaRight = Population(1, SpikeSourceArray(spike_times=[31, 32,33, 34, 35, 36, 37, 38,39,40]), label="Spike Source Right")
# connect them in according to the follwing pattern

excDelay = 0.68

Projection(retinaLeft, neuronInhLeft, OneToOneConnector(), StaticSynapse(weight=49.5, delay=0.1))
Projection(retinaLeft, neuronInhRight, OneToOneConnector(), StaticSynapse(weight=-39.5, delay=0.1))
Projection(retinaLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=39.5, delay=excDelay))

Projection(retinaRight, neuronInhRight, OneToOneConnector(), StaticSynapse(weight=49.5, delay=0.1))
Projection(retinaRight, neuronInhLeft, OneToOneConnector(), StaticSynapse(weight=-39.5, delay=0.1))
Projection(retinaRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=39.5, delay=excDelay))

Projection(neuronInhLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=-39.5, delay=0.1))
Projection(neuronInhRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=-39.5, delay=0.1))

run(50.0)

# plot results
filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
# all_neurons.write_data(filename, annotations={'script_name': __file__})

from pyNN.utility.plotting import Figure, Panel
figure_filename = filename.replace("pkl", "png")
Figure(
    Panel(neuronCell.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)", xlabel="Time (ms)",
          data_labels=[neuronCell.label], yticks=True, xticks=True, ylim=(-110, -40)),  
    Panel(neuronInhLeft.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)", xlabel="Time (ms)",
          data_labels=[neuronInhLeft.label], yticks=True, xticks=True, ylim=(-110, -40)),
    Panel(neuronInhRight.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)", xlabel="Time (ms)",
          data_labels=[neuronInhRight.label], yticks=True, xticks=True, ylim=(-110, -40)),
    title="AND-Cell",
    annotations="Simulated with NEST"
).save(figure_filename)
print(figure_filename)
print "Totally {0} spikes Cell Output".format(len(neuronCell.get_data().segments[0].spiketrains[0]))
print "Totally {0} spikes Left Inhibitor".format(len(neuronInhLeft.get_data().segments[0].spiketrains[0]))
print "Totally {0} spikes Right Inhibitor".format(len(neuronInhRight.get_data().segments[0].spiketrains[0]))

end()

