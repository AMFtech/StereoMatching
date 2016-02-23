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
    network = createCooperativeNetwork(retinaLeft=retinaLeft, retinaRight=retinaRight)
    
    # run simulation for time in milliseconds
    print "Simulation started..."
    Frontend.run(simulationTime)   
    
#     print network[0][1].label
#     spikeList = network[0][1].getSpikes()
#     print spikeList
    # finalise program and simulation
    Frontend.end()
    print "Simulation ended."
    
    from NetworkVisualiser import logFile
    logFile.close()

main()
