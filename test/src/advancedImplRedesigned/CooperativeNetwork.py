from pyNN.nest import setup, run, end
from NetworkBuilder import createCooperativeNetwork, createSpikeSource
from NetworkVisualiser import plotSimulationResults 
from SimulationAndNetworkSettings import simulationTime, simulationTimestep, maxSynapseDelay, minSynapseDelay

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=simulationTimestep, min_delay=minSynapseDelay, max_delay=maxSynapseDelay)

# create a spike sources
retinaLeft = createSpikeSource("Retina Left")
retinaRight = createSpikeSource("Retina Right")

# create network and attach the spike sources 
network = createCooperativeNetwork(retinaLeft=retinaLeft, retinaRight=retinaRight)

# run simulation for time in milliseconds
run(simulationTime)

# plot results s
plotSimulationResults()

# finalise program and simulation
end()


