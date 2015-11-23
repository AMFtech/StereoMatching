from pyNN.nest import Population, SpikeSourceArray
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, minDisparity, maxDisparity, retLeftSpikes, retRightSpikes
from pyNN.nest.standardmodels.cells import IF_curr_exp

def createSpikeSource(label):
    assert label == "Retina Left" or label == "Retina Right", "Unknown Retina Identifier! Creating Retina Failed."
    retina = Population((dimensionRetinaX, dimensionRetinaY), SpikeSourceArray(), label=label)
    
    if label == "Retina Right":
        spikeTimes = retRightSpikes
    else:
        spikeTimes = retLeftSpikes     
    
    assert len(spikeTimes) >= dimensionRetinaY and len(spikeTimes[0]) >= dimensionRetinaX, "Check dimensionality of retina's spiking times!"        
    # iterate over all neurons in the SpikeSourcaArray and set every one's parameters individually        
    print "Creating Spike Source: {0}".format(label)
    for row in range(0, dimensionRetinaY):
        for pixel in range(0, dimensionRetinaX):
            retina[row * dimensionRetinaY + pixel].set_parameters(spike_times = spikeTimes[row][pixel])
#             print retina[row * dimensionRetinaY + pixel].get_parameters()        
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
    
    inhLeftPop = Population((dimensionRetinaX, dimensionRetinaY, maxDisparity+1), IF_curr_exp(), label="Inhibitory Population of Left Retina")
    inhRightPop = Population((dimensionRetinaX, dimensionRetinaY, maxDisparity+1), IF_curr_exp(), label="Inhibitory Population of Right Retina")
    cellOutputPop = Population((dimensionRetinaX, dimensionRetinaY, maxDisparity+1), IF_curr_exp(), label="Cell Output Population of Network")
    
    # set essential neural parameters
    from SimulationAndNetworkSettings import t_synE, t_synI, t_memb, vResetInh, vResetCO
    inhLeftPop.set(tau_syn_E=t_synE, tau_syn_I=t_synI, tau_m=t_memb, v_reset=vResetInh)
    inhRightPop.set(tau_syn_E=t_synE, tau_syn_I=t_synI, tau_m=t_memb, v_reset=vResetInh)
    cellOutputPop.set(tau_syn_E=t_synE, tau_syn_I=t_synI, tau_m=t_memb, v_reset=vResetCO)
    
    # reocrd data for plotting purposes
    from pyNN.nest import record
    inhLeftPop.record('v', 'spikes')
    inhRightPop.record('v', 'spikes')
    cellOutputPop.record('v', 'spikes')
    inhLeftPop.record('spikes')
    inhRightPop.record('spikes')
    cellOutputPop.record('spikes')
    
    network = inhLeftPop + inhRightPop + cellOutputPop
    
    network.record('v')
    network.record('spikes')
    
    interconnectNetworkNeurons(network)
    
    return network

def connectSpikeSourcesToNetwork(network=None, retinaLeft=None, retinaRight=None):
    
    assert network is not None and retinaLeft is not None and retinaRight is not None, "Network or one of the Retinas is not initialised!"
    print "Connecting Spike Sources to Network..."
    
    inhLeft = network.get_population("Inhibitory Population of Left Retina")
    inhRight = network.get_population("Inhibitory Population of Right Retina")
    cellOut = network.get_population("Cell Output Population of Network") 
    
    retLeftToCO = []
    retLeftToInhLeft = []
    retLeftToInhRight = []
    retRightToCO = []
    retRightToInhRight = []
    retRightToInhLeft = []

    from SimulationAndNetworkSettings import wSSToOtherInh, wSSToSelfInh, wSSToOut, dSSToOtherInh, dSSToSelfInh, dSSToOut
    
    # connect neurons with retina according to the AND-ensemble pattern
    indexLimiter = maxDisparity+1
    for pixelLID, pixelRID in zip(retinaLeft, retinaRight):
        indexL = retinaLeft.id_to_index(pixelLID)
        indexR = retinaRight.id_to_index(pixelRID) 
        
        # reset limiter for the next layer
        if indexL % dimensionRetinaX == 0:
            indexLimiter = maxDisparity + 1
            
        if indexL % dimensionRetinaX > dimensionRetinaX - maxDisparity - 1: 
            indexLimiter -= 1
          
        for disp in range(minDisparity, indexLimiter):
            indexLNet = indexL * (maxDisparity+1) + disp  
            indexRNet = indexLNet
            
            retLeftToCO.append([indexL, indexLNet, wSSToOut, dSSToOut])
            retLeftToInhLeft.append([indexL, indexLNet, wSSToSelfInh, dSSToSelfInh])
            retLeftToInhRight.append([indexL, indexLNet, wSSToOtherInh, dSSToOtherInh])    
                
            retRightToCO.append([indexR + disp, indexRNet, wSSToOut, dSSToOut])
            retRightToInhRight.append([indexR + disp, indexRNet, wSSToSelfInh, dSSToSelfInh])
            retRightToInhLeft.append([indexR + disp, indexRNet, wSSToOtherInh, dSSToOtherInh])
          
#     print retLeftToCO 
#     print retRightToCO 
    from pyNN.nest import Projection, FromListConnector
    
    Projection(retinaLeft, cellOut, FromListConnector(retLeftToCO))  
    Projection(retinaLeft, inhLeft, FromListConnector(retLeftToInhLeft)) 
    Projection(retinaLeft, inhRight, FromListConnector(retLeftToInhRight)) 
    
    Projection(retinaRight, cellOut, FromListConnector(retRightToCO)) 
    Projection(retinaRight, inhLeft, FromListConnector(retRightToInhLeft)) 
    Projection(retinaRight, inhRight, FromListConnector(retRightToInhRight)) 
    

def interconnectNetworkNeurons(network=None):
    
    assert network is not None, "Network is not initialised! Interconnecting failed."
    
    from pyNN.nest import Projection, FromListConnector
    from SimulationAndNetworkSettings import wInhToOut, dInhToOut
        
    inhLeft = network.get_population("Inhibitory Population of Left Retina")
    inhRight = network.get_population("Inhibitory Population of Right Retina")
    cellOut = network.get_population("Cell Output Population of Network")
    
    leftToCO = []
    rightToCO = []
    # create lists with connecting patterns
    for idL, idR, idCO in zip (inhLeft, inhRight, cellOut):
        leftToCO.append([inhLeft.id_to_index(idL), cellOut.id_to_index(idCO), wInhToOut, dInhToOut])
        rightToCO.append([inhRight.id_to_index(idR), cellOut.id_to_index(idCO), wInhToOut, dInhToOut])

    # connect the inhibitory neurons to the cell output neurons
    print "Interconnecting Neurons..."
    Projection(inhLeft, cellOut, FromListConnector(leftToCO))
    Projection(inhRight, cellOut, FromListConnector(rightToCO))
    
    interconnectNeuronsForInternalInhibitionAndExcitation(network)
    
def interconnectNeuronsForInternalInhibitionAndExcitation(network=None):
    
    assert network is not None, "Network is not initialised! Interconnecting for inhibitory and excitatory patterns failed."
    
    cellOut = network.get_population("Cell Output Population of Network")
    
    from SimulationAndNetworkSettings import radiusExcitation, radiusInhibition
    assert radiusInhibition >= maxDisparity, "Bad radius of inhibition. Uniquness constraint cannot be satisfied."
    assert 0 <= radiusExcitation <= dimensionRetinaX, "Bad radius of excitation."
    # create lists with inhibitory along the Retina Right projective line
    nbhoodInhL = []
    nbhoodInhR = []
    nbhoodExc = []
    # used for the triangular form of the matrix in order to remain within the square
    indexLimiter = maxDisparity+1
    rowCounter = -1
    for id in cellOut[0::maxDisparity+1]:
        rowCounter += 1
        # take first index of each row
        rowID = cellOut.id_to_index(id)
        
        # reset limiter for the next layer
        if rowCounter % dimensionRetinaX == 0:
            indexLimiter = maxDisparity + 1
        
        if rowCounter % dimensionRetinaX > dimensionRetinaX - maxDisparity - 1: 
            indexLimiter -= 1
            if indexLimiter <= 0:
                break
        allXRForOneXLVal = []   
        for disp in range(minDisparity, indexLimiter):
            #compute for according index in the network for the left inhibition
            # for each pixel count up along the row until disparityMax (or limiter is reached)
            indexNet = rowID + disp  
            allXRForOneXLVal.append(indexNet)
            # compute it now for the right
            # for all diagonal elements count up until disparity max is reached
            if indexNet % (maxDisparity + 1) == 0:
                if maxDisparity == 0:
                    nbhoodInhR.append([indexNet])
                else:    
                    nbhoodInhR.append([x for x in range(indexNet, indexNet - maxDisparity**2 - 1, -maxDisparity) \
                                       if x/(dimensionRetinaX*(maxDisparity+1)) == indexNet/(dimensionRetinaX*(maxDisparity+1))])
            
        nbhoodInhL.append(allXRForOneXLVal)  
    
    # generate all the diagonal connections
    for diag in map(None, *nbhoodInhL):
        sublist = []
        for elem in diag:
            if elem is not None:
                sublist.append(elem)
        nbhoodExc.append(sublist)
    
    print nbhoodInhL
    print nbhoodInhR
    print nbhoodExc          
            
    print "Connecting neurons for internal excitation and inhibition..."
    from SimulationAndNetworkSettings import wOutToOutExc, dOutToOutExc, wOutToOutInh, dOutToOutInh
    connectionListInhL = []
    connectionListInhR = []
    connectionListExc = []
    for neuronID in cellOut:
        neuronIndex = cellOut.id_to_index(neuronID)
        
        for inhL in nbhoodInhL:
            if neuronIndex in inhL:
                for dist in range(1, min(len(inhL), radiusInhibition)):
                    if neuronIndex + dist <= max(inhL):
                        connectionListInhL.append([neuronIndex, neuronIndex+dist, wOutToOutInh, dOutToOutInh])
                    if neuronIndex - dist >= min(inhL):    
                        connectionListInhL.append([neuronIndex, neuronIndex-dist, wOutToOutInh, dOutToOutInh])          
                break       
        
        for inhR in nbhoodInhR:
            if neuronIndex in inhR:
                for dist in range(1, min(len(inhR), radiusInhibition)):
                    if neuronIndex + dist*maxDisparity <= max(inhR):
                        connectionListInhR.append([neuronIndex, neuronIndex+dist*maxDisparity, wOutToOutInh, dOutToOutInh])
                    if neuronIndex - dist*maxDisparity >= min(inhR):    
                        connectionListInhR.append([neuronIndex, neuronIndex-dist*maxDisparity, wOutToOutInh, dOutToOutInh])
        
        for exc in nbhoodExc:
            if neuronIndex in exc:
                for dist in range(1, min(len(exc), radiusExcitation**2)):
                    if neuronIndex + dist*(maxDisparity+1) in exc:
                        connectionListExc.append([neuronIndex, neuronIndex+dist*(maxDisparity+1), wOutToOutExc, dOutToOutExc])
                    if neuronIndex - dist*(maxDisparity+1) in exc:    
                        connectionListExc.append([neuronIndex, neuronIndex-dist*(maxDisparity+1), wOutToOutExc, dOutToOutExc])
                    if neuronIndex + dist*(maxDisparity+1)*dimensionRetinaX in exc:
                        connectionListExc.append([neuronIndex, neuronIndex+dist*(maxDisparity+1)*dimensionRetinaX, wOutToOutExc, dOutToOutExc])
                    if neuronIndex - dist*(maxDisparity+1)*dimensionRetinaX in exc:    
                        connectionListExc.append([neuronIndex, neuronIndex-dist*(maxDisparity+1)*dimensionRetinaX, wOutToOutExc, dOutToOutExc])    
             
    print connectionListInhL            
    print connectionListInhR
    print connectionListExc
    
    from pyNN.nest import Projection, FromListConnector
    Projection(cellOut, cellOut, FromListConnector(connectionListInhL))
    Projection(cellOut, cellOut, FromListConnector(connectionListInhR))
#     Projection(cellOut, cellOut, FromListConnector(connectionListExc))
    
    
    








    
    