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
    inhLeftPop.record('spikes', 'v')
    inhRightPop.record('spikes', 'v')
    cellOutputPop.record('spikes', 'v')
    
    network = inhLeftPop + inhRightPop + cellOutputPop
    
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
        
        if indexL > dimensionRetinaX - maxDisparity - 1: 
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
    pass    












    
    