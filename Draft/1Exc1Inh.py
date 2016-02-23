from pyNN.nest import *
from pyNN.utility import normalized_filename

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.1, max_delay=5.0)

# create populations of single neurons of type IF_cond_alpha
neuronInh = Population(1, IF_cond_alpha(), label="Inhibited")
neuronExc = Population(1, IF_cond_alpha(), label="Excited")
neuronMid = Population(1, IF_cond_alpha(), label="Middle")

# globally set parameters
# neurons.set({'tau_m':20, 'v_rest':-65}) ...

# initialise records for plotting purposes
all_neurons = neuronExc + neuronInh + neuronMid
all_neurons.record('v')

# create a spike source firing at spike_times
spike_source = Population(1, SpikeSourceArray(spike_times=[30.]), label="Spike Source")

# connect them in according to the follwing pattern
#                    neuronInh 
#                        |
#    spike_source -- neuronMid 
#                        |
#                    neuronExc 
conSpksrcToNrnmid = Projection(spike_source, neuronMid, OneToOneConnector(), StaticSynapse(weight=0.5), receptor_type='excitatory')
conNrnmidToNrninh = Projection(neuronMid, neuronInh, OneToOneConnector(), StaticSynapse(weight=0.9, delay=4.5), receptor_type='inhibitory')
conNrnmidToNrnexc = Projection(neuronMid, neuronExc, OneToOneConnector(), StaticSynapse(weight=0.1, delay=4.5), receptor_type='excitatory')

conSpksrcToNrninh = Projection(spike_source, neuronInh, OneToOneConnector(), StaticSynapse(weight=0.5, delay=3.0), receptor_type='excitatory')

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

