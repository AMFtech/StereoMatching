from pyNN.nest import setup, run, end
from network_builder import createCooperativeNetwork, createSpikeSource
from plotter import plotSimulationResults
from network_parameters import *

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.1, max_delay=5.0)


# create a spike sources firing at specific spiking times
spikingTimingLeft = [[[30], [300], [340]],[[30], [150, 151, 152, 153, 154, 156, 158], [340]]]
retinaLeft = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingLeft, labelSS = "Left Retina")
spikingTimingRight = [[[31], [301], [360]],[[30], [152, 160], [340]]]
retinaRight = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingRight, labelSS = "Right Retina")

# create network and attach the spike sources 
## TODO: Change to dz= disparityMax when advanced configuration and connections are implemented
network = createCooperativeNetwork(dx = dimensionRetinaX, dy = dimensionRetinaY, dz = dimensionRetinaX, 
	spikeSourceL = retinaLeft, spikeSourceR = retinaRight)

# run simulation for time in milliseconds
run(200.0)

print network
# plot results
plotSimulationResults(network, retinaLeft, retinaRight)

# finalise program and simulation
end()




