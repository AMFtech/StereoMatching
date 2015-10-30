from pyNN.nest import *
from pyNN.utility import normalized_filename

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.1, max_delay=5.0)

# create populations of single neurons of type IF_cond_alpha
neuronInhLeft = Population(1, IF_cond_alpha(), label="Inhibitor Left")
neuronInhRight = Population(1, IF_cond_alpha(), label="Inhibitor Right")
neuronCell = Population(1, IF_cond_alpha(), label="Cell Output")

# globally set parameters
# neurons.set({'tau_m':20, 'v_rest':-65}) ...

# initialise records for plotting purposes
all_neurons = neuronInhLeft + neuronInhRight + neuronCell
all_neurons.record('v')
neuronCell.record('spikes')

# create a spike source firing at spike_times
retinaLeft = Population(1, SpikeSourceArray(spike_times=[35., 36., 37., 38., 39., 135., 136., 137., 138.]), label="Spike Source Left")
retinaRight = Population(1, SpikeSourceArray(spike_times=[138., 139.]), label="Spike Source Right")
# connect them in according to the follwing pattern
#                    neuronInh 
#                        |
#    spike_source -- neuronMid 
#                        |
#                    neuronExc 
Projection(retinaLeft, neuronInhLeft, OneToOneConnector(), StaticSynapse(weight=1.9, delay=0.2), receptor_type='excitatory')
Projection(retinaLeft, neuronInhRight, OneToOneConnector(), StaticSynapse(weight=50.0, delay=0.1), receptor_type='inhibitory')
Projection(retinaLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=0.7, delay=0.7), receptor_type='excitatory')

Projection(retinaRight, neuronInhRight, OneToOneConnector(), StaticSynapse(weight=1.9, delay=0.2), receptor_type='excitatory')
Projection(retinaRight, neuronInhLeft, OneToOneConnector(), StaticSynapse(weight=50.0, delay=0.1), receptor_type='inhibitory')
Projection(retinaRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=0.7, delay=0.7), receptor_type='excitatory')

Projection(neuronInhLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=1.0, delay=0.2), receptor_type='inhibitory')
Projection(neuronInhRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=1.0, delay=0.2), receptor_type='inhibitory')

run(200.0)

# plot results
filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
all_neurons.write_data(filename, annotations={'script_name': __file__})

from pyNN.utility.plotting import Figure, Panel
figure_filename = filename.replace("pkl", "png")
Figure(
    Panel(neuronCell.get_data().segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[neuronCell.label], yticks=True, ylim=(-75, -40)),
    Panel(neuronCell.get_data().segments[0].spiketrains, xlabel="Time (ms)", xticks=True),   
    Panel(neuronInhLeft.get_data().segments[0].filter(name='v')[0],
          data_labels=[neuronInhLeft.label], yticks=True, ylim=(-75, -40)),
    Panel(neuronInhRight.get_data().segments[0].filter(name='v')[0],
          data_labels=[neuronInhRight.label], yticks=True, ylim=(-75, -40)),
    title="1Exc1Inh",
    annotations="Simulated with NEST"
).save(figure_filename)
print(figure_filename)

end()

