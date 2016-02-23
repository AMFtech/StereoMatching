from pyNN.nest import Population, SpikeSourceArray
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, minDisparity, maxDisparity, retLeftSpikes, retRightSpikes
from pyNN.nest import IF_curr_exp
from pyNN.space import Line

retinaNbhoodL = []
retinaNbhoodR = []


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
    
    print "\t Creating Populations..."
    from SimulationAndNetworkSettings import t_synE, t_synI, t_memb, vResetInh, vResetCO
    from pyNN.nest import record
    
    network = []
    for x in range(0, dimensionRetinaX):
        for disp in range(0, maxDisparity+1):
            inhLeftPop = Population(dimensionRetinaY, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh},
                label="Blocker Left {0}".format(x*dimensionRetinaX + disp))
            inhRightPop = Population(dimensionRetinaY, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh},
                label="Blocker Right {0}".format(x*dimensionRetinaX + disp))
            cellOutputPop = Population(dimensionRetinaY, IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetCO},
                label="Cell Output {0}".format(x*dimensionRetinaX + disp))
            
            # reocrd data for plotting purposes
            cellOutputPop.record('v')
            
            network.append((inhLeftPop, inhRightPop, cellOutputPop))
    
    interconnectNetworkNeurons(network)
    
    return network


def interconnectNetworkNeurons(network=None):
    
    assert network is not None, "Network is not initialised! Interconnecting failed."
    
    from pyNN.nest import Projection, OneToOneConnector, StaticSynapse
    from SimulationAndNetworkSettings import wInhToOut, dInhToOut
        
    # connect the inhibitory neurons to the cell output neurons
    print "Interconnecting Neurons..."
    for ensemble in network:
        # connect the left inhibitor to the cell output neuron
        Projection(ensemble[0], ensemble[2], OneToOneConnector(), StaticSynapse(weight=wInhToOut, delay=dInhToOut))
        # connect the right inhibitor to the cell output neuron
        Projection(ensemble[1], ensemble[2], OneToOneConnector(), StaticSynapse(weight=wInhToOut, delay=dInhToOut))
    
    if dimensionRetinaX > 1 and maxDisparity > 0:
        interconnectNeuronsForInternalInhibitionAndExcitation(network)
    
def interconnectNeuronsForInternalInhibitionAndExcitation(network=None):
    
    assert network is not None, "Network is not initialised! Interconnecting for inhibitory and excitatory patterns failed."
    
    from SimulationAndNetworkSettings import radiusExcitation, radiusInhibition
    assert radiusInhibition >= maxDisparity, "Bad radius of inhibition. Uniquness constraint cannot be satisfied."
    assert 0 <= radiusExcitation <= dimensionRetinaX, "Bad radius of excitation."
    # create lists with inhibitory along the Retina Right projective line
    nbhoodInhL = []
    nbhoodInhR = []
    nbhoodExc = []
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
        nbhoodExc.append(sublist)
     
#     print nbhoodInhL
#     print nbhoodInhR
#     print nbhoodExc          
    
    global retinaNbhoodL,retinaNbhoodR
    
    retinaNbhoodL = nbhoodInhL
    retinaNbhoodR = nbhoodInhR

    print "\t Connecting neurons for internal excitation and inhibition..."
    from SimulationAndNetworkSettings import wOutToOutExc, dOutToOutExc, wOutToOutInh, dOutToOutInh
    from pyNN.nest import Projection, OneToOneConnector, StaticSynapse
    
    for row in nbhoodInhL:
        for pop in row:
            for nb in row:
                if nb != pop:
                    Projection(network[pop][2], network[nb][2], 
                        OneToOneConnector(), StaticSynapse(weight=wOutToOutInh, delay=dOutToOutInh))
    for col in nbhoodInhR:
        for pop in col:
            for nb in col:
                if nb != pop:
                    Projection(network[pop][2], network[nb][2], 
                        OneToOneConnector(), StaticSynapse(weight=wOutToOutInh, delay=dOutToOutInh))
    for diag in nbhoodExc:
        for pop in diag:
            for nb in diag:
                if nb != pop:
                    Projection(network[pop][2], network[nb][2], 
                        OneToOneConnector(), StaticSynapse(weight=wOutToOutExc, delay=dOutToOutExc))
    
    print "\t Connecting completed."
    
def connectSpikeSourcesToNetwork(network=None, retinaLeft=None, retinaRight=None):
    
    assert network is not None and retinaLeft is not None and retinaRight is not None, "Network or one of the Retinas is not initialised!"
    print "Connecting Spike Sources to Network..."
    
    from pyNN.nest import Projection, OneToOneConnector, StaticSynapse
    from SimulationAndNetworkSettings import wSSToOtherInh, wSSToSelfInh, wSSToOut, dSSToOtherInh, dSSToSelfInh, dSSToOut
    
    global retinaNbhoodL, retinaNbhoodR
    
    pixel = 0
    for row in retinaNbhoodL:
#         print row, pixel
        for pop in row:
            Projection(retinaLeft[pixel], network[pop][2], 
                OneToOneConnector(), StaticSynapse(weight=wSSToOut, delay=dSSToOut))
            Projection(retinaLeft[pixel], network[pop][0], 
                OneToOneConnector(), StaticSynapse(weight=wSSToSelfInh, delay=dSSToSelfInh))
            Projection(retinaLeft[pixel], network[pop][1], 
                OneToOneConnector(), StaticSynapse(weight=wSSToOtherInh, delay=dSSToOtherInh))
        pixel += 1
    
    pixel = 0    
    for col in retinaNbhoodR:
#         print col, pixel
        for pop in col:
            Projection(retinaRight[pixel], network[pop][2], 
                OneToOneConnector(), StaticSynapse(weight=wSSToOut, delay=dSSToOut))
            Projection(retinaRight[pixel], network[pop][0], 
                OneToOneConnector(), StaticSynapse(weight=wSSToOtherInh, delay=dSSToOtherInh))
            Projection(retinaRight[pixel], network[pop][1], 
                OneToOneConnector(), StaticSynapse(weight=wSSToSelfInh, delay=dSSToSelfInh))
        pixel += 1    
    print "\t Spike Sources connected."
    

    








    
    