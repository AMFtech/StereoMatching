from SimulationAndNetworkSettings import simulationTime, simulationTimestep, maxSynapseDelay, minSynapseDelay
import spynnaker.pyNN as Frontend
# import pyNN.spiNNaker as Frontend2
from NetworkBuilder import createCooperativeNetwork, createSpikeSource

def main():
    # setup simulation parameters
    Frontend.setup(timestep=simulationTimestep, min_delay=minSynapseDelay, max_delay=maxSynapseDelay, threads=4)

    # create left and right retina inputs
    retinaLeft = createSpikeSource("RetL")
    retinaRight = createSpikeSource("RetR")
    
    # create network and attach the retinas 
    network = createCooperativeNetwork(retinaLeft=retinaLeft, retinaRight=retinaRight)
    
    # run simulation
    print "Simulation started..."
    Frontend.run(simulationTime)                                            
    print "Simulation ended."
    
    # finalise simulation
    Frontend.end()
    
    # finalise logging
    from NetworkVisualiser import logFile
    logFile.close()
    
main()
