from pyNN.nest import setup, run, end
from network_builder import createCooperativeNetwork, createSpikeSource
from plotter import plotSimulationResults 
from network_parameters import *

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.1, max_delay=5.0)

# 3,4,5,6,7,8,9,10,11,12,13,15,16,17,
# create a spike sources firing at specific spiking times
spikingTimingLeft = [ [[20, 100, 101, 110, 130], [14, 19, 20,30,40,50, 90, 200.6], [90, 100.5], [100.5], [100.5], [100.5]] ]
retinaLeft = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingLeft, labelSS = "Left Retina")
spikingTimingRight = [ [[2,3,4,5,6, 500.5], [18, 100, 100.6], [ 15, 100, 110, 120, 130], [100.5], [1000.5], [1000.5]] ]
retinaRight = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingRight, labelSS = "Right Retina")

# create network and attach the spike sources 
## TODO: Change to dz= disparityMax when advanced configuration and connections are implemented
network = createCooperativeNetwork(dx = dimensionRetinaX, dy = dimensionRetinaY, dz = dimensionRetinaX, 
	spikeSourceL = retinaLeft, spikeSourceR = retinaRight)

# run simulation for time in milliseconds
simulationTime = 30.0
run(simulationTime)

# plot results s
plotSimulationResults(network, retinaLeft, retinaRight, int(simulationTime), layer=0)

# finalise program and simulation
end()


