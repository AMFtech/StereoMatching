from SimulationAndNetworkSettings import simulationTime, simulationTimestep, maxSynapseDelay, minSynapseDelay
from pyNN.spiNNaker import setup, run, end
from NetworkBuilder import createCooperativeNetwork, createSpikeSource
from NetworkVisualiser import plotExperiment

def main():
    # setup timestep of simulation and minimum and maximum synaptic delays
    setup(timestep=simulationTimestep, min_delay=minSynapseDelay, max_delay=maxSynapseDelay, threads=4)

    # create a spike sources
    retinaLeft = createSpikeSource("Retina Left")
    retinaRight = createSpikeSource("Retina Right")
    
    # create network and attach the spike sources 
    network = createCooperativeNetwork(retinaLeft=retinaLeft, retinaRight=retinaRight)
    
    # run simulation for time in milliseconds
    print "Simulation started..."
    run(simulationTime)                                            
    print "Simulation ended."
    
    # plot results  
    plotExperiment(retinaLeft, retinaRight, network)
    # finalise program and simulation
    end()

main()
