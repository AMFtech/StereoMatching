import pyNN.nest as sim
from pyNN.utility import normalized_filename
from numpy import arange

sim.setup(timestep=0.1, min_delay=0.1)

neurons = sim.Population(1, sim.IF_curr_exp())
spike_sourceE = sim.Population(1, sim.SpikeSourceArray(spike_times=[33.1, 330.2, 330.3]))
spike_sourceI = sim.Population(1, sim.SpikeSourceArray(spike_times=[33.1, 330.2, 330.3]))

connection = sim.Projection(spike_sourceE, neurons, sim.OneToOneConnector(), sim.StaticSynapse(weight=22.5, delay=0.1))
connection = sim.Projection(spike_sourceI, neurons, sim.OneToOneConnector(), sim.StaticSynapse(weight=-22.5, delay=0.1))
# electrode = sim.DCSource(start=2.0, stop=92.0, amplitude=0.014)
# electrode.inject_into(neurons)

neurons.record(['v'])  #, 'u'])
neurons.set(tau_syn_E=1.0)
neurons.set(tau_syn_I=1.0)
neurons.set(tau_m=5.0)
neurons.set(v_reset=-72.0)

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
