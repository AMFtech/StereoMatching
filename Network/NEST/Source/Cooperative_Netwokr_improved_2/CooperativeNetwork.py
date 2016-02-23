from pyNN.nest import setup, run, end
from NetworkBuilder import createCooperativeNetwork, createSpikeSource
from NetworkVisualiser import plotSimulationResults 
from SimulationAndNetworkSettings import simulationTime, simulationTimestep, maxSynapseDelay, minSynapseDelay
from multiprocessing import Process

def main():
    # setup timestep of simulation and minimum and maximum synaptic delays
    setup(timestep=simulationTimestep, min_delay=minSynapseDelay, max_delay=maxSynapseDelay)
    
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
    from itertools import repeat
    numberOfLayersToPlot = 4
    layers = zip(repeat(network, numberOfLayersToPlot), range(1, numberOfLayersToPlot+1), repeat(False, numberOfLayersToPlot))
    customLayers = [(network, 20, False),(network, 40, False),(network, 60, False),(network, 80, False)]
    for proc in range(0, numberOfLayersToPlot):
        p = Process(target=plotSimulationResults, args=customLayers[proc])
        p.start()
    
    # finalise program and simulation
    end()

main()
