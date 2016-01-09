import spynnaker.pyNN as Frontend
import spynnaker_external_devices_plugin.pyNN as ExternalDevices
import pyNN.spiNNaker as Frontend2
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, minDisparity, maxDisparity
from pyNN.space import Line

from NetworkVisualiser import plotReceivedSpike

retinaNbhoodL = []
retinaNbhoodR = []
sameDisparityInd = []

useCVisualiser = False

def createSpikeSource(label):       
    # iterate over all neurons in the SpikeSourcaArray and set every one's parameters individually        
    print "Creating Spike Source: {0}".format(label)
    
    retina = []
    for x in range(0, dimensionRetinaX):
        colOfPixels = Frontend2.Population(dimensionRetinaY, ExternalDevices.SpikeInjector, {'port': 12300+x}, label="{0}_{1}".format(label, x))
        retina.append(colOfPixels)
#         colOfPixels.record('spikes')
    
    return retina


def createCooperativeNetwork(retinaLeft=None, retinaRight=None):
    
    assert retinaLeft is not None and retinaRight is not None, "Retinas are not initialised! Creating Network Failed."
    network = createNetwork()
    liveConnections = connectSpikeSourcesToNetwork(network, retinaLeft, retinaRight)
    return (network, liveConnections)


def createNetwork():
    
    # the dimesion is X x Y x maxDisparity+1 because disparity 0 means no shift in pixel location
    # however the network should still exist and contain only one disparity map. 
    assert dimensionRetinaX > maxDisparity >= 0, "Maximum Disparity Constant is illegal!"
    print "Creating Cooperative Network..."
    
    
    from SimulationAndNetworkSettings import t_synE, t_synI, t_memb, vResetInh, vResetCO
    
    network = []
    numberOfPopulations = (2*dimensionRetinaX*(maxDisparity+1) - (maxDisparity+1)**2 + maxDisparity + 1)/2
    print "\t Creating {0} Populations...".format(numberOfPopulations)
    for x in range(0, numberOfPopulations):
        inhLeftRightPop = Frontend.Population(dimensionRetinaY*2, Frontend.IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetInh},
            label="InhPop {0}".format(x))
        cellOutputPop = Frontend.Population(dimensionRetinaY, Frontend.IF_curr_exp, {'tau_syn_E':t_synE, 'tau_syn_I':t_synI, 'tau_m':t_memb, 'v_reset':vResetCO},
            label="ColPop {0}".format(x))
        
        # reocrd data for plotting purposes
        cellOutputPop.record()
#         cellOutputPop.record_v()
            
        network.append((inhLeftRightPop, cellOutputPop))
        
    interconnectNetworkNeurons(network)
    
    return network


def interconnectNetworkNeurons(network=None):
    
    assert network is not None, "Network is not initialised! Interconnecting failed."
    
    from SimulationAndNetworkSettings import wInhToOut, dInhToOut
        
    # generate connectivity list: 0 till dimensionRetinaY-1 for the  left and dimensionRetinaY till dimensionRetinaY*2 -1 for the right
    connList = []
    for y in range(0, dimensionRetinaY):
        connList.append((y, y, wInhToOut, dInhToOut))
        connList.append((y+dimensionRetinaY, y, wInhToOut, dInhToOut))
          
    # connect the inhibitory neurons to the cell output neurons
    print "Interconnecting Neurons..."
    for ensemble in network:
        Frontend.Projection(ensemble[0], ensemble[1], Frontend.FromListConnector(connList),  target='inhibitory')
    
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
    
    for row in nbhoodInhL:
        for pop in row:
            for nb in row:
                if nb != pop:
                    Frontend.Projection(network[pop][1], network[nb][1], 
                        Frontend.OneToOneConnector(weights=wOutToOutInh, delays=dOutToOutInh), target='inhibitory')
    for col in nbhoodInhR:
        for pop in col:
            for nb in col:
                if nb != pop:
                    Frontend.Projection(network[pop][1], network[nb][1], 
                        Frontend.OneToOneConnector(weights=wOutToOutInh, delays=dOutToOutInh), target='inhibitory')
                    
    for diag in nbhoodExcX:
        for pop in diag:
            for nb in range(1, radiusExcitation+1):
                if diag.index(pop)+nb < len(diag):
                    Frontend.Projection(network[pop][1], network[diag[diag.index(pop)+nb]][1], 
                        Frontend.OneToOneConnector(weights=wOutToOutExc, delays=dOutToOutExc), target='excitatory')
                if diag.index(pop)-nb >= 0:
                    Frontend.Projection(network[pop][1], network[diag[diag.index(pop)-nb]][1], 
                        Frontend.OneToOneConnector(weights=wOutToOutExc, delays=dOutToOutExc), target='excitatory')
    
    for ensemble in network:
        Frontend.Projection(ensemble[1], ensemble[1], Frontend.FromListConnector(nbhoodEcxY), target='excitatory')
                    
#     print "\t Connecting completed."
    
def connectSpikeSourcesToNetwork(network=None, retinaLeft=None, retinaRight=None):
    
    assert network is not None and retinaLeft is not None and retinaRight is not None, "Network or one of the Retinas is not initialised!"
    print "Connecting Spike Sources to Network..."
    
    from SimulationAndNetworkSettings import wSSToOtherInh, wSSToSelfInh, wSSToOut, dSSToOtherInh, dSSToSelfInh, dSSToOut
    
    global retinaNbhoodL, retinaNbhoodR
    
    # left is 0--dimensionRetinaY-1; right is dimensionRetinaY--dimensionRetinaY*2-1
    connListRetLBlockerL = []
    connListRetLBlockerR = []
    connListRetRBlockerL = []
    connListRetRBlockerR = []
    for y in range(0, dimensionRetinaY):
        connListRetLBlockerL.append((y, y, wSSToSelfInh, dSSToSelfInh))
        connListRetLBlockerR.append((y, y+dimensionRetinaY, wSSToOtherInh, dSSToOtherInh))
        connListRetRBlockerL.append((y, y, wSSToOtherInh, dSSToOtherInh))
        connListRetRBlockerR.append((y, y+dimensionRetinaY, wSSToSelfInh, dSSToSelfInh))
        
    pixel = 0
    for row in retinaNbhoodL:
#         print row, pixel
        for pop in row:
            Frontend.Projection(retinaLeft[pixel], network[pop][1], 
                Frontend.OneToOneConnector(weights=wSSToOut, delays=dSSToOut), target='excitatory')
            Frontend.Projection(retinaLeft[pixel], network[pop][0], Frontend.FromListConnector(connListRetLBlockerL), target='excitatory')
            Frontend.Projection(retinaLeft[pixel], network[pop][0], Frontend.FromListConnector(connListRetLBlockerR), target='inhibitory')
        pixel += 1
    
    pixel = 0    
    for col in retinaNbhoodR:
#         print col, pixel
        for pop in col:
            Frontend.Projection(retinaRight[pixel], network[pop][1], 
                Frontend.OneToOneConnector(weights=wSSToOut, delays=dSSToOut), target='excitatory')
            Frontend.Projection(retinaRight[pixel], network[pop][0], Frontend.FromListConnector(connListRetRBlockerR), target='excitatory')
            Frontend.Projection(retinaRight[pixel], network[pop][0], Frontend.FromListConnector(connListRetRBlockerL), target='inhibitory')
        pixel += 1    
    
    liveConnectionNetwork = setupSpikeReceiver(network)
    liveConnectionRetinas = setupSpikeInjectors(retinaLeft, retinaRight)
    
    return (liveConnectionNetwork, liveConnectionRetinas)

def setupSpikeReceiver(network=None):
    print "Setting up Spike Receiver..."
    networkLabels = []
    for pop in network:
        ExternalDevices.activate_live_output_for(pop[1], database_notify_host="localhost", database_notify_port_num=19996)
        networkLabels.append(pop[1].label)
      
    from spynnaker_external_devices_plugin.pyNN.connections.spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection
        
    if not useCVisualiser:
         liveConnection = SpynnakerLiveSpikesConnection(receive_labels=networkLabels, local_port=19996, send_labels=None)   
    for label in networkLabels:
        liveConnection.add_receive_callback(label, receiveSpike)    
    return liveConnection       
    
def setupSpikeInjectors(retinaLeft=None, retinaRight=None):
    print "Setting up Spike Injectors for Retina Left and Retina Right..."
    retinaLabels = []
    for popL, popR in zip(retinaLeft, retinaRight):
        retinaLabels.append(popL.label)
        retinaLabels.append(popR.label)
        
    from spynnaker_external_devices_plugin.pyNN.connections.spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection
    
    liveConnection = SpynnakerLiveSpikesConnection(receive_labels=None, local_port=19999, send_labels=retinaLabels)
    
    from retinaSpikeInjector import startInjecting
    liveConnection.add_start_callback(retinaLabels[0], startInjecting)
    return liveConnection 
    
def injectSpike(label="", neuronID=0, sender=None):
    sender.send_spike(label, neuronID)   

def receiveSpike(label, time, neuronIDs):
    populationNumber = [s for s in label.split()][1]
    for neuronID in neuronIDs:         
        plotReceivedSpike(populationNumber, neuronID)



    
    