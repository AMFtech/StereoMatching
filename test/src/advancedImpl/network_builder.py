from pyNN.nest import *

'''
Creating an Assembly of Populations of one spiking neuron with an assigned timing for the spikes.
This solution allows spiking to occur at arbitrary point within the simulation time.
'''
def createSpikeSource(dx=1, dy=1, timing=[[]]):
	if len(timing) < dy :
		print "WARNING: Dimension of Timing Vector is mismatching the Spike Source's Dimension!"
		"Timing Vector will be automatically padded with []"
		for padding in range(0, dy - len(timing)):
			timing.append([])
	if dy >= 1:
		oneLayer = None
		if dx >= 1:
			oneLayer = Population(1, SpikeSourceArray(spike_times = timing[0][0]), 
				label="Left Retina -- Layer 1 -- Pixel 1")
			for pixel in range(1, dx):
				oneLayer += Population(1, SpikeSourceArray(spike_times = timing[0][pixel]), 
					label="Left Retina -- Layer 1 -- Pixel {0}".format(pixel+1))
		else :
			print "WARNING: No Spike Sources created! "
			return oneLayer
		spikeSource = oneLayer
		for layer in range(1, dy):
			oneLayer = Population(1, SpikeSourceArray(spike_times = timing[layer][0]), 
				label="Left Retina -- Layer 2 -- Pixel 1")
			for pixel in range(1, dx):
				oneLayer += Population(1, SpikeSourceArray(spike_times = timing[layer][pixel]), 
					label="Left Retina -- Layer {0} -- Pixel {1}".format(layer+1, pixel+1))	
			spikeSource += oneLayer
		return spikeSource
	else :
		return None						
		


def createCooperativeNetwork(spikeSourceL, spikeSourceR, dx=0, dy=0, dz=0):
	return None