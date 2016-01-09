import spynnaker_external_devices_plugin.pyNN as ExternalDevices

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
        colOfPixels = Population(dimensionRetinaY, SpikeSourceArray, {'spike_times': spikeTimes[x]}, label="{0} - Population {1}".format(label, x), structure=Line())
        retina.append(colOfPixels)
        colOfPixels.record('spikes')
    
    return retina