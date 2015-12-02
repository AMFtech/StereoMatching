from pyNN.spiNNaker import Population, SpikeSourceArray
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, minDisparity, maxDisparity, retLeftSpikes, retRightSpikes
from pyNN.spiNNaker import IF_curr_exp
from pyNN.space import Line

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
    from pyNN.spiNNaker import record
    
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
    
    from pyNN.spiNNaker import Projection, OneToOneConnector
    from SimulationAndNetworkSettings import wInhToOut, dInhToOut
        
    # connect the inhibitory neurons to the cell output neurons
    print "Interconnecting Neurons..."
    for ensemble in network:
        # connect the left inhibitor to the cell output neuron
        Projection(ensemble[0], ensemble[2], OneToOneConnector(weights=wInhToOut, delays=dInhToOut))
        # connect the right inhibitor to the cell output neuron
        Projection(ensemble[1], ensemble[2], OneToOneConnector(weights=wInhToOut, delays=dInhToOut))
    
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
        if neuronIndex % 1000 == 0:
            print "\t {0} out of {1} neurons calculated.".format(neuronIndex, len(cellOut))
        for inhL in nbhoodInhL:
            if neuronIndex in inhL:
                for dist in range(1, min(len(inhL), radiusInhibition)):
                    if neuronIndex + dist <= max(inhL):
                        connectionListInhL.append([neuronIndex, neuronIndex+dist, wOutToOutInh, dOutToOutInh])
                    if neuronIndex - dist >= min(inhL):    
                        connectionListInhL.append([neuronIndex, neuronIndex-dist, wOutToOutInh, dOutToOutInh]) 
                break       
#         print "\t Creating connector list for inhibilion Right..."
        for inhR in nbhoodInhR:
            if neuronIndex in inhR:
                for dist in range(1, min(len(inhR), radiusInhibition)):
                    if neuronIndex + dist*maxDisparity <= max(inhR):
                        connectionListInhR.append([neuronIndex, neuronIndex+dist*maxDisparity, wOutToOutInh, dOutToOutInh])
                    if neuronIndex - dist*maxDisparity >= min(inhR):    
                        connectionListInhR.append([neuronIndex, neuronIndex-dist*maxDisparity, wOutToOutInh, dOutToOutInh])    
                break
#         print "\t Creating connector list for excitation..."   
        for exc in nbhoodExc:
            if neuronIndex in exc:
                for distX in range(1, min(radiusExcitation+1, dimensionRetinaX)):
                    nbPlus = neuronIndex + distX*(maxDisparity+1)
                    # make sure that neighbouring neurons remain within this layer
                    if nbPlus/(dimensionRetinaX*(maxDisparity+1)) == neuronIndex/(dimensionRetinaX*(maxDisparity+1)):
                        if nbPlus in exc:
                            connectionListExc.append([neuronIndex, nbPlus, wOutToOutExc, dOutToOutExc])
                            for distY in range(1, radiusExcitation+1):
                                nbUp = nbPlus + distY*(maxDisparity+1)*dimensionRetinaX
                                nbDn = nbPlus - distY*(maxDisparity+1)*dimensionRetinaX
                                if nbUp in exc:
                                    connectionListExc.append([neuronIndex, nbUp, wOutToOutExc, dOutToOutExc])
                                if nbDn in exc:
                                    connectionListExc.append([neuronIndex, nbDn, wOutToOutExc, dOutToOutExc])    
                    nbMinus = neuronIndex - distX*(maxDisparity+1)
                    # same in the other direction
                    if nbMinus/(dimensionRetinaX*(maxDisparity+1)) == neuronIndex/(dimensionRetinaX*(maxDisparity+1)):
                        if nbMinus in exc:    
                            connectionListExc.append([neuronIndex, nbMinus, wOutToOutExc, dOutToOutExc])
                            for distY in range(1, radiusExcitation+1):
                                nbUp = nbMinus + distY*(maxDisparity+1)*dimensionRetinaX
                                nbDn = nbMinus - distY*(maxDisparity+1)*dimensionRetinaX
                                if nbUp in exc:
                                    connectionListExc.append([neuronIndex, nbUp, wOutToOutExc, dOutToOutExc])
                                if nbDn in exc:
                                    connectionListExc.append([neuronIndex, nbDn, wOutToOutExc, dOutToOutExc])
                # now iterate over all neighbouring layers
                for distYOverSpiking in range(1, min(radiusExcitation+1, dimensionRetinaY)):
                    # no need to check if it is within the possible nodes because the network is identical in every layer 
                    # and there always exist such neighbouring neuron    
                    nbUp = neuronIndex + distYOverSpiking*(maxDisparity+1)*dimensionRetinaX
                    nbDn = neuronIndex - distYOverSpiking*(maxDisparity+1)*dimensionRetinaX
                    if nbUp in exc:
                        connectionListExc.append([neuronIndex, nbUp, wOutToOutExc, dOutToOutExc])
                    if nbDn in exc:
                        connectionListExc.append([neuronIndex, nbDn, wOutToOutExc, dOutToOutExc])    
                break    
# #     print connectionListInhL            
# #     print connectionListInhR
# #     print connectionListExc
#     dump(connectionListInhL, open('./precomputedLObj/connectionListInhL_64x_64y_30d_5e.p', 'wb'))
#     dump(connectionListInhR, open('./precomputedLObj/connectionListInhR_64x_64y_30d_5e.p', 'wb'))
#     dump(connectionListExc, open('./precomputedLObj/connectionListExc_64x_64y_30d_5e.p', 'wb'))
    print "\t Connecting from generated lists..."
    
    from pyNN.nest import Projection, FromListConnector
#     if connectionListInhL != []:
#     l1 = open('./precomputedLObj/connectionListInhL_64x_64y_30d_5e.p', 'rb')
#     connectionListInhL = load(l1)
#     l1.close()
#     print "Freeing inhl"
    print "starting 1 conn"
    t1 = Thread(target=Projection, args=(cellOut, cellOut, FromListConnector(connectionListInhL)))
    t1.start()
#         Projection(cellOut, cellOut, FromListConnector(connectionListInhL))
#     if connectionListInhR != []:  
#     l2 = open('./precomputedLObj/connectionListInhR_64x_64y_30d_5e.p', 'rb')
#     connectionListInhR = load(l2)
#     l2.close()
#     print "Freeing inhr"
    print "starting 2 conn"
    t2 = Thread(target=Projection, args=(cellOut, cellOut, FromListConnector(connectionListInhR)))
    t2.start()        
#         Projection(cellOut, cellOut, FromListConnector(connectionListInhR))
#     if connectionListExc != []: 
#     l3 = open('./precomputedLObj/connectionListExc_64x_64y_30d_5e.p', 'rb')
#     connectionListExc = load(l3)
#     l3.close()       
    print "starting 3 conn"  
    t3 = Thread(target=Projection, args=(cellOut, cellOut, FromListConnector(connectionListExc)))
    t3.start()       
#         Projection(cellOut, cellOut, FromListConnector(connectionListExc))
    t1.join()
    t2.join()
    t3.join()
    print "\t Connecting completed."
    
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
#     print retLeftToInhLeft
#     print retLeftToInhRight
#     print retRightToCO 
#     print retRightToInhLeft
#     print retRightToInhRight
#     dump(retLeftToCO, open('./precomputedLObj/retLeftToCO_64x_64y_30d_5e.p', 'wb'))
#     dump(retLeftToInhLeft, open('./precomputedLObj/retLeftToInhLeft_64x_64y_30d_5e.p', 'wb'))
#     dump(retLeftToInhRight, open('./precomputedLObj/retLeftToInhRight_164x_64y_30d_5e.p', 'wb'))
#     dump(retRightToCO, open('./precomputedLObj/retRightToCO_64x_64y_30d_5e.p', 'wb'))
#     dump(retRightToInhLeft, open('./precomputedLObj/retRightToInhLeft_64x_64y_30d_5e.p', 'wb'))
#     dump(retRightToInhRight, open('./precomputedLObj/retRightToInhRight_64x_64y_30d_5e.p', 'wb'))

#     l1 = open('./precomputedLObj/retLeftToCO_64x_64y_30d_5e.p', 'rb')
#     retLeftToCO = load(l1)
#     l1.close()
#     
#     l2 = open('./precomputedLObj/retLeftToInhLeft_64x_64y_30d_5e.p', 'rb')
#     retLeftToInhLeft = load(l2)
#     l2.close()
#     
#     l3 = open('./precomputedLObj/retLeftToInhRight_164x_64y_30d_5e.p', 'rb')
#     retLeftToInhRight = load(l3)
#     l3.close()
#     
#     l4 = open('./precomputedLObj/retRightToCO_64x_64y_30d_5e.p', 'rb')
#     retRightToCO = load(l4)
#     l4.close()
#     
#     l5 = open('./precomputedLObj/retRightToInhLeft_64x_64y_30d_5e.p', 'rb')
#     retRightToInhLeft = load(l5)
#     l5.close()
#     
#     l6 = open('./precomputedLObj/retRightToInhRight_64x_64y_30d_5e.p', 'rb')
#     retRightToInhRight = load(l6)
#     l6.close()
    
    from pyNN.nest import Projection, FromListConnector
    print "\t Connecting Left..."
    t1 = Thread(target=Projection, args=(retinaLeft, cellOut, FromListConnector(retLeftToCO)))
    t2 = Thread(target=Projection, args=(retinaLeft, inhLeft, FromListConnector(retLeftToInhLeft)))
    t3 = Thread(target=Projection, args=(retinaLeft, inhRight, FromListConnector(retLeftToInhRight)))
    t1.start()
    t2.start()
    t3.start()
#     Projection(retinaLeft, cellOut, FromListConnector(retLeftToCO))  
#     Projection(retinaLeft, inhLeft, FromListConnector(retLeftToInhLeft)) 
#     Projection(retinaLeft, inhRight, FromListConnector(retLeftToInhRight)) 
#     print "\t Connecting Left completed."
    print "\t Connecting Right..."
    t4 = Thread(target=Projection, args=(retinaRight, cellOut, FromListConnector(retRightToCO)))
    t5 = Thread(target=Projection, args=(retinaRight, inhLeft, FromListConnector(retRightToInhLeft)))
    t6 = Thread(target=Projection, args=(retinaRight, inhRight, FromListConnector(retRightToInhRight)))
    t4.start()
    t5.start()
    t6.start()    
#     Projection(retinaRight, cellOut, FromListConnector(retRightToCO)) 
#     Projection(retinaRight, inhLeft, FromListConnector(retRightToInhLeft)) 
#     Projection(retinaRight, inhRight, FromListConnector(retRightToInhRight)) 
#     print "\t Connecting Right completed."
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    








    
    