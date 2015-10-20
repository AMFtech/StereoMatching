import pyNN.nest as sim
from pyNN.utility import normalized_filename
from numpy import arange

sim.setup(timestep=0.01, min_delay=1.0)

neurons = sim.Population(1, sim.IF_cond_exp())
spike_source = sim.Population(1, sim.SpikeSourceArray(spike_times=[10.0]))

connection = sim.Projection(spike_source, neurons, sim.OneToOneConnector(), sim.StaticSynapse(weight=0.1, delay=1.0), receptor_type='excitatory')


# electrode = sim.DCSource(start=2.0, stop=92.0, amplitude=0.014)
# electrode.inject_into(neurons)

neurons.record(['v'])  #, 'u'])

neurons.initialize(v=-70.0, u=-14.0)


sim.run(100.0)

filename = normalized_filename("Results", "test", "pkl", "nest", sim.num_processes())
neurons.write_data(filename, annotations={'script_name': __file__})

from pyNN.utility.plotting import Figure, Panel
figure_filename = filename.replace("pkl", "png")
data = neurons.get_data().segments[0]
if data.filter(name="v") == []:
    print "Empty"
    
v = data.filter(name="v")[0]

#u = data.filter(name="u")[0]
Figure(
    Panel(v, ylabel="Membrane potential (mV)", xticks=True,
          xlabel="Time (ms)", yticks=True),
    #Panel(u, ylabel="u variable (units?)"),
    annotations="Simulated with %s" % "NEST"
).save(figure_filename)
print(figure_filename)

sim.end()
