from pyNN.nest import setup, run, end
from network_builder import createCooperativeNetwork, createSpikeSource
# from plotter import plotSimulationResults


####### Network Parameters #########

dimensionRetinaX = 3
dimensionRetinaY = 1
  
# radiusInhibition = 1
# radiusExcitation = 1
disparityMin = 0
disparityMax = 1

#################################

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.2, max_delay=5.0)


# create a spike sources firing at specific spiking times
spikingTimingLeft = [[[30.], [300.], [300.]]]
retinaLeft = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingLeft)
spikingTimingRight = [[[40.], [300.], [300.]]]
retinaRight = createSpikeSource(dx = dimensionRetinaX, dy = dimensionRetinaY, timing = spikingTimingRight)

# create network and attach the spike sources 
network = createCooperativeNetwork(dx = dimensionRetinaX, dy = dimensionRetinaY, dz = disparityMax, 
	spikeSourceL = retinaLeft, spikeSourceR = retinaRight)

# run simulation for time in milliseconds
# run(200.0)

# plot results
# plotSimulationResults(network, retinaLeft, retinaRight)

# finalise program and simulation
end()




