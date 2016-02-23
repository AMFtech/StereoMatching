from SimulationAndNetworkSettings import simulationTime, simulationTimestep, maxSynapseDelay, minSynapseDelay
import spynnaker.pyNN as Frontend
# import pyNN.spiNNaker as Frontend2
from NetworkBuilder import createCooperativeNetwork, createSpikeSource
# from NetworkVisualiser import plotExperiment

def main():
    # setup timestep of simulation and minimum and maximum synaptic delays
    Frontend.setup(timestep=simulationTimestep, min_delay=minSynapseDelay, max_delay=maxSynapseDelay, threads=4)

    # create a spike sources
    retinaLeft = createSpikeSource("RetL")
    retinaRight = createSpikeSource("RetR")
    
    # create network and attach the spike sources 
    network, (liveConnectionNetwork, liveConnectionRetinas) = createCooperativeNetwork(retinaLeft=retinaLeft, retinaRight=retinaRight)

    # non-blocking run for time in milliseconds
    print "Simulation started..."
    Frontend.run(simulationTime)                                          
    print "Simulation ended."
    
    # plot results  
    #
#     plotExperiment(retinaLeft, retinaRight, network)
    # finalise program and simulation
    Frontend.end()

main()
