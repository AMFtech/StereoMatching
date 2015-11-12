from pyNN.nest import *
from network_parameters import disparityMax, disparityMin 

'''
Creating an Assembly of Populations of one spiking neuron with an assigned timing for the spikes.
This solution allows spiking to occur at arbitrary point within the simulation time.
'''
def createSpikeSource(dx=1, dy=1, timing=[[]], labelSS=""):

	if len(timing) < dy:
		print "WARNING:\ncreateSpikeSource: Dimension of Timing Vector is mismatching the Spike Source's Dimension!"
		"Timing Vector will be automatically padded with []"
		for padding in range(0, dy - len(timing)):
			timing.append([])
	spikeSource = []		
	for layer in range(1, dy+1):
		oneLayer = []
		for pixel in range(1, dx+1):
			onePixel = Population(1, SpikeSourceArray(spike_times = timing[layer-1][pixel-1]), 
				label="{2} - Layer {1} - Pixel {0}".format(pixel, layer, labelSS))
			onePixel.record('spikes')
			oneLayer.append(onePixel)
			
		spikeSource.append(oneLayer)		
	print "Successfully created Spike Source"	
	return spikeSource					
		


def createCooperativeNetwork(spikeSourceL, spikeSourceR, dx=1, dy=1, dz=1):

	if spikeSourceL is None or spikeSourceR is None:
		print "WARNING:\ncreateCooperativeNetwork: Spike Source is None. No Network created!"
		return None
	if dx < 1 or dy < 1 or dz < 1:
		print "WARNING:\ncreateCooperativeNetwork: One or more Dimensions are less than or equal to 0. No Network created!"
		return None

	print "Creating Network..."
	network = createNetwork(dx=dx, dy=dy, dz=dz) 
	print "Network successfully created."
	print "Connetcting Spike-sources..."
	connectSpikeSourcesToNetwork(sourceL=spikeSourceL, sourceR=spikeSourceR, network=network, dy=dy, dx=dx, dz=dz)
	print "Spike-sources successfully connected."
# 	interconnectLayersForInternalExcitationAndInhibition(network)
	return network

def createNetwork(dx=1, dy=1, dz=1):
	# dx, dy and dz are already >= 1 so no need to check them
	pixels = []
	rows = []
	layers = []
	for yCells in range(1, dy+1):
		for zCells in range(1, dz+1):	
			for xCells in range(1, dx+1):
				pixels.append(createANDCell(xCells, yCells, zCells))
			rows.append(pixels)	
			pixels = []
		layers.append(rows)
		rows = []	
	return layers

def createANDCell(xlabel, ylabel, zlabel):
	# create populations of single neurons of type IF_curr_exp and connect them
 	internalWeightInhibition = -39.5
	internalDelayInhibition = 0.1
	
	neuronInhLeft = Population(1, IF_curr_exp(), label="Inhibitor Left {0} - {1} - {2}".format(xlabel, ylabel, zlabel))
	neuronInhRight = Population(1, IF_curr_exp(), label="Inhibitor Right {0} - {1} - {2}".format(xlabel, ylabel, zlabel))
	neuronCell = Population(1, IF_curr_exp(), label="Cell Output {0} - {1} - {2}".format(xlabel, ylabel, zlabel))

	neuronInhLeft.set(tau_syn_E=1.0, tau_syn_I=1.0, tau_m=1.07, v_reset=-92.0)
	neuronInhRight.set(tau_syn_E=1.0, tau_syn_I=1.0, tau_m=1.07, v_reset=-92.0)
	neuronCell.set(tau_syn_E=1.0, tau_syn_I=1.0, tau_m=1.07, v_reset=-102.0)
	
	neuronCell.record('spikes', 'v')
	neuronInhLeft.record('spikes', 'v')
	neuronInhRight.record('spikes', 'v')
	
	Projection(neuronInhLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=internalWeightInhibition, delay=internalDelayInhibition))
	Projection(neuronInhRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=internalWeightInhibition, delay=internalDelayInhibition))

	andNeuron = neuronInhLeft + neuronInhRight + neuronCell
	andNeuron.record('spikes')
	andNeuron.record('v')
# 	print andNeuron
	return andNeuron

def connectSpikeSourcesToNetwork(sourceL=None, sourceR=None, network=None, dx=1, dy=1, dz=1):
						
	weightExcitationSelfBlocker = 49.5
	weightInhibitionOtherBlocker = -39.5
	weightExcitationCell = 39.5
	
	delayExcitationSelfBlocker = 0.1
	delayInhibitionOtherBlocker = 0.1
	delayExcitationCell = 0.65#1.174
	
	for layer in range(0, dy):
		for pixel in range(0, dx):
			# connect spike sources to cells within the disparityMax range
			for disp in range(disparityMin, disparityMax+1):
				indexInNetworkLayerL = pixel + disp
				if indexInNetworkLayerL <= dx - 1:
					# Left Retina is being connected
					Projection(sourceL[layer][pixel], 
							network[layer][indexInNetworkLayerL][pixel].get_population("Inhibitor Left {0} - {1} - {2}".format(pixel+1, layer+1, indexInNetworkLayerL+1)), 
							OneToOneConnector(), StaticSynapse(weight=weightExcitationSelfBlocker, delay=delayExcitationSelfBlocker))
					Projection(sourceL[layer][pixel], 
							network[layer][indexInNetworkLayerL][pixel].get_population("Cell Output {0} - {1} - {2}".format(pixel+1, layer+1, indexInNetworkLayerL+1)), 
							OneToOneConnector(), StaticSynapse(weight=weightExcitationCell, delay=delayExcitationCell))
					Projection(sourceL[layer][pixel], 
							network[layer][indexInNetworkLayerL][pixel].get_population("Inhibitor Right {0} - {1} - {2}".format(pixel+1, layer+1, indexInNetworkLayerL+1)), 
							OneToOneConnector(), StaticSynapse(weight=weightInhibitionOtherBlocker, delay=delayInhibitionOtherBlocker))	
				# Right Retina is being connected, swap x and z coordinates!
				indexInNetworkLayerR = pixel - disp
				if indexInNetworkLayerR >= 0:
					Projection(sourceR[layer][indexInNetworkLayerR], 
							network[layer][pixel][indexInNetworkLayerR].get_population("Inhibitor Right {0} - {1} - {2}".format(indexInNetworkLayerR+1, layer+1, pixel+1)), 
							OneToOneConnector(), StaticSynapse(weight=weightExcitationSelfBlocker, delay=delayExcitationSelfBlocker))
					Projection(sourceR[layer][indexInNetworkLayerR], 
							network[layer][pixel][indexInNetworkLayerR].get_population("Cell Output {0} - {1} - {2}".format(indexInNetworkLayerR+1, layer+1, pixel+1)), 
							OneToOneConnector(), StaticSynapse(weight=weightExcitationCell, delay=delayExcitationCell))
					Projection(sourceR[layer][indexInNetworkLayerR], 
							network[layer][pixel][indexInNetworkLayerR].get_population("Inhibitor Left {0} - {1} - {2}".format(indexInNetworkLayerR+1, layer+1, pixel+1)), 
							OneToOneConnector(), StaticSynapse(weight=weightInhibitionOtherBlocker, delay=delayInhibitionOtherBlocker))
							
					
					
					
	
