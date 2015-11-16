from pyNN.nest import Population, SpikeSourceArray
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, maxDisparity, retLeftSpikes, retRightSpikes
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
    for row in range(0, dimensionRetinaY):
        for pixel in range(0, dimensionRetinaX):
            retina[row * dimensionRetinaY + pixel].set_parameters(spike_times = spikeTimes[row][pixel])
            print retina[row * dimensionRetinaY + pixel].get_parameters()        
    return retina


def createCooperativeNetwork(retinaLeft=None, retinaRight=None):
    
    assert retinaLeft is not None and retinaRight is not None, "Retinas are not initialised! Creating Network Failed."
    network = createNetwork()
    connectSpikeSourcesToNetwork(network, retinaLeft, retinaRight)
    interconnectCellOutputNeurons(network)
    return network


def createNetwork():
    
    # the dimesion is X x Y x maxDisparity+1 because disparity 0 means no shift in pixel location
    # however the network should still exist and contain only one disparity map. 
    assert dimensionRetinaX > maxDisparity >= 0, "Maximum Disparity Constant is illegal!"
    inhLeftPop = Population((dimensionRetinaX, dimensionRetinaY, maxDisparity+1), IF_curr_exp, label="Inhibitory Population of Left Retina")
    inhRightPop = Population((dimensionRetinaX, dimensionRetinaY, maxDisparity+1), IF_curr_exp, label="Inhibitory Population of Right Retina")
    cellOutputPop = Population((dimensionRetinaX, dimensionRetinaY, maxDisparity+1), IF_curr_exp, label="Cell Output Population of Network")
    
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
    return network

def connectSpikeSourcesToNetwork(network=None, retinaLeft=None, retinaRight=None):
    pass

def interconnectCellOutputNeurons(network=None):
    pass
    
    