from pyNN.nest import setup, run, end
from network_builder import createCooperativeNetwork, createSpikeSource
from plotter import plotSimulationResults 
from network_parameters import *

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.1, max_delay=5.0)


# create a spike sources firing at specific spiking times
spikingTimingLeft = [[[3],[5], [6], [7]]]
retinaLeft = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingLeft, labelSS = "Left Retina")
spikingTimingRight = [[[3],[5], [8], [13]]]
retinaRight = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingRight, labelSS = "Right Retina")

# create network and attach the spike sources 
## TODO: Change to dz= disparityMax when advanced configuration and connections are implemented
network = createCooperativeNetwork(dx = dimensionRetinaX, dy = dimensionRetinaY, dz = dimensionRetinaX, 
	spikeSourceL = retinaLeft, spikeSourceR = retinaRight)

# run simulation for time in milliseconds
run(15.0)

# plot results s
plotSimulationResults(network, retinaLeft, retinaRight)

# finalise program and simulation
end()


