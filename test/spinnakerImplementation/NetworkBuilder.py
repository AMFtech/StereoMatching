from pyNN.spiNNaker import Population, SpikeSourceArray
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, minDisparity, maxDisparity, retLeftSpikes, retRightSpikes
from pyNN.spiNNaker import IF_curr_exp
from pyNN.space import Line

retinaNbhoodL = []
retinaNbhoodR = []
sameDisparityInd = []


def createSpikeSource(label):
    assert label == "Retina Left" or label == "Retina Right", "Unknown Retina Identifier! Creating Retina Failed."
    if label == "Retina Right":
        spikeTimes = retRightSpikes
    else:
        spikeTimes = retLeftSpikes   
        
    assert len(spikeTimes) >= dimensionRetinaY and len(spikeTimes[0]) >= dimensionRetinaX, "Check dimensionality of retina's spiking times!"        
    # iterate over all neurons in the SpikeSourcaArray and set every one's parameters individually        
    print "Creating Spike Source: {0}".format(label)
    
    retina = []
    for x in range(0, dimensionRetinaX):
        retina.append(Population(dimensionRetinaY, SpikeSourceArray, {'spike_times': spikeTimes[x]}, label="{0} - Population {1}".format(label, x), structure=Line()))

    return retina


def createCooperativeNetwork(retinaLeft=None, retinaRight=None):
    
    assert retinaLeft is not None and retinaRight is not None, "Retinas are not initialised! Creating Network Failed."
    network = createNetwork()
    connectSpikeSourcesToNetwork(network, retinaLeft, retinaRight)
    return network


def createNetwork():
    
    # the dimesion is X x Y x maxDisparity+1 because disparity 0 means no shift in pixel location
    # however the network should still exist and contain only one disparity map. 
    assert dimensionRetinaX > maxDisparity >= 0, "Maximum Disparity Constant is illegal!"
    print "Creating Cooperative Network..."
    
    
    from SimulationAndNetworkSettings import t_synE, t_synI, t_memb, vResetInh, vResetCO
    from pyNN.spiNNaker import record
    
    network = []
    numberOfPopulations = (2*dimensionRetinaX*(maxDisparity+1) - (maxDisparity+1)**2 + maxDisparity + 1)/2
    print "\t Creating {0} Populations...".format(numberOfPopulations)
    for x in range(0, numberOfPopulations):
        inhLeftPop = Population(dimensionRetinaY, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh},
            label="Blocker Left {0}".format(x))
        inhRightPop = Population(dimensionRetinaY, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh},
            label="Blocker Right {0}".format(x))
        cellOutputPop = Population(dimensionRetinaY, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetCO},
            label="Cell Output {0}".format(x))
        
        # reocrd data for plotting purposes
        cellOutputPop.record('spikes')
            
        network.append((inhLeftPop, inhRightPop, cellOutputPop))
        
    interconnectNetworkNeurons(network)
    
    return network


def interconnectNetworkNeurons(network=None):
    
    assert network is not None, "Network is not initialised! Interconnecting failed."
    
    from pyNN.spiNNaker import Projection, OneToOneConnector
    from SimulationAndNetworkSettings import wInhToOut, dInhToOut
        
    # connect the inhibitory neurons to the cell output neurons
    print "Interconnecting Neurons..."
    for ensemble in network:
        # connect the left inhibitor to the cell output neuron
        Projection(ensemble[0], ensemble[2], OneToOneConnector(weights=wInhToOut, delays=dInhToOut), target='inhibitory')
        # connect the right inhibitor to the cell output neuron
        Projection(ensemble[1], ensemble[2], OneToOneConnector(weights=wInhToOut, delays=dInhToOut), target='inhibitory')
    
    if dimensionRetinaX > 1 and maxDisparity > 0:
        interconnectNeuronsForInternalInhibitionAndExcitation(network)
    
def interconnectNeuronsForInternalInhibitionAndExcitation(network=None):
    
    assert network is not None, "Network is not initialised! Interconnecting for inhibitory and excitatory patterns failed."
    
    from SimulationAndNetworkSettings import radiusExcitation, radiusInhibition
    from SimulationAndNetworkSettings import wOutToOutExc, dOutToOutExc, wOutToOutInh, dOutToOutInh
    assert radiusInhibition >= maxDisparity, "Bad radius of inhibition. Uniquness constraint cannot be satisfied."
    assert 0 <= radiusExcitation <= dimensionRetinaX, "Bad radius of excitation."
    # create lists with inhibitory along the Retina Right projective line
    nbhoodInhL = []
    nbhoodInhR = []
    nbhoodExcX = []
    nbhoodEcxY = []
    # used for the triangular form of the matrix in order to remain within the square
    print "\t Generating inhibitory and excitatory connectivity patterns..."
    # generate rows
    limiter = maxDisparity+1
    ensembleIndex = 0
    
    while ensembleIndex < len(network):
        if ensembleIndex/(maxDisparity+1) > dimensionRetinaX - maxDisparity - 1:
            limiter -= 1
            if limiter == 0:
                break
            
        nbhoodInhL.append([ensembleIndex+disp for disp in range(0, limiter)])
        ensembleIndex += limiter
    
    ensembleIndex = len(network)
    
    # generate columns
    nbhoodInhR = [[x] for x in nbhoodInhL[0]]
    shiftGlob = 0
    for x in nbhoodInhL[1:]:
        shiftGlob += 1
        shift = 0
    #     print "--", x, shiftGlob
        for e in x:
            if (shift+1) % (maxDisparity+1) == 0:
                nbhoodInhR.append([e])
            else:
                nbhoodInhR[shift+shiftGlob].append(e)
            shift += 1     
      
    # generate all diagonals
    for diag in map(None, *nbhoodInhL):
        sublist = []
        for elem in diag:
            if elem is not None:
                sublist.append(elem)
        nbhoodExcX.append(sublist)
    
    # generate all y-axis excitation
    for x in range(0, dimensionRetinaY):
        for e in range(1, radiusExcitation+1):
            if x+e < dimensionRetinaY:
                nbhoodEcxY.append((x, x+e, wOutToOutExc, dOutToOutExc))
            if x-e >= 0:
                nbhoodEcxY.append((x, x-e, wOutToOutExc, dOutToOutExc))    
     
#     print nbhoodInhL
#     print nbhoodInhR
#     print nbhoodExcX  
#     print nbhoodEcxY        
    
    global retinaNbhoodL,retinaNbhoodR, sameDisparityInd 
    
    retinaNbhoodL = nbhoodInhL
    retinaNbhoodR = nbhoodInhR
    sameDisparityInd = nbhoodExcX

    print "\t Connecting neurons for internal excitation and inhibition..."
    
    from pyNN.spiNNaker import Projection, OneToOneConnector, FromListConnector
    
    for row in nbhoodInhL:
        for pop in row:
            for nb in row:
                if nb != pop:
                    Projection(network[pop][2], network[nb][2], 
                        OneToOneConnector(weights=wOutToOutInh, delays=dOutToOutInh), target='inhibitory')
    for col in nbhoodInhR:
        for pop in col:
            for nb in col:
                if nb != pop:
                    Projection(network[pop][2], network[nb][2], 
                        OneToOneConnector(weights=wOutToOutInh, delays=dOutToOutInh), target='inhibitory')
                    
    for diag in nbhoodExcX:
        for pop in diag:
            for nb in range(1, radiusExcitation+1):
                if diag.index(pop)+nb < len(diag):
                    Projection(network[pop][2], network[diag[diag.index(pop)+nb]][2], 
                        OneToOneConnector(weights=wOutToOutExc, delays=dOutToOutExc), target='excitatory')
                if diag.index(pop)-nb >= 0:
                    Projection(network[pop][2], network[diag[diag.index(pop)-nb]][2], 
                        OneToOneConnector(weights=wOutToOutExc, delays=dOutToOutExc), target='excitatory')
    
    for ensemble in network:
        Projection(ensemble[2], ensemble[2], FromListConnector(nbhoodEcxY), target='excitatory')
                    
#     print "\t Connecting completed."
    
def connectSpikeSourcesToNetwork(network=None, retinaLeft=None, retinaRight=None):
    
    assert network is not None and retinaLeft is not None and retinaRight is not None, "Network or one of the Retinas is not initialised!"
    print "Connecting Spike Sources to Network..."
    
    from pyNN.spiNNaker import Projection, OneToOneConnector
    from SimulationAndNetworkSettings import wSSToOtherInh, wSSToSelfInh, wSSToOut, dSSToOtherInh, dSSToSelfInh, dSSToOut
    
    global retinaNbhoodL, retinaNbhoodR
    
    pixel = 0
    for row in retinaNbhoodL:
#         print row, pixel
        for pop in row:
            Projection(retinaLeft[pixel], network[pop][2], 
                OneToOneConnector(weights=wSSToOut, delays=dSSToOut), target='excitatory')
            Projection(retinaLeft[pixel], network[pop][0], 
                OneToOneConnector(weights=wSSToSelfInh, delays=dSSToSelfInh), target='excitatory')
            Projection(retinaLeft[pixel], network[pop][1], 
                OneToOneConnector(weights=wSSToOtherInh, delays=dSSToOtherInh), target='inhibitory')
        pixel += 1
    
    pixel = 0    
    for col in retinaNbhoodR:
#         print col, pixel
        for pop in col:
            Projection(retinaRight[pixel], network[pop][2], 
                OneToOneConnector(weights=wSSToOut, delays=dSSToOut), target='excitatory')
            Projection(retinaRight[pixel], network[pop][0], 
                OneToOneConnector(weights=wSSToOtherInh, delays=dSSToOtherInh), target='inhibitory')
            Projection(retinaRight[pixel], network[pop][1], 
                OneToOneConnector(weights=wSSToSelfInh, delays=dSSToSelfInh), target='excitatory')
        pixel += 1    
    print "\t Spike Sources connected."
    

    








    
    