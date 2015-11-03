from pyNN.nest import *

'''
Creating an Assembly of Populations of one spiking neuron with an assigned timing for the spikes.
This solution allows spiking to occur at arbitrary point within the simulation time.
'''
def createSpikeSource(dx=1, dy=1, timing=[[]]):

	if len(timing) < dy :
		print "WARNING:\ncreateSpikeSource: Dimension of Timing Vector is mismatching the Spike Source's Dimension!"
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
			print "WARNING:\ncreateSpikeSource: No Spike Sources created! "
			return oneLayer
		spikeSource = oneLayer
		for layer in range(1, dy):
			oneLayer = Population(1, SpikeSourceArray(spike_times = timing[layer][0]), 
				label="Left Retina -- Layer 2 -- Pixel 1")
			for pixel in range(1, dx):
				oneLayer += Population(1, SpikeSourceArray(spike_times = timing[layer][pixel]), 
					label="Left Retina -- Layer {0} -- Pixel {1}".format(layer+1, pixel+1))	
			spikeSource += oneLayer
		print "Successfully created Spike Source"	
		return spikeSource
	else :
		print "WARNING:\ncreateSpikeSource: No Spike Sources created! "
		return None						
		


def createCooperativeNetwork(spikeSourceL, spikeSourceR, dx=1, dy=1, dz=1):

	if spikeSourceL is None or spikeSourceR is None:
		print "WARNING:\ncreateCooperativeNetwork: Spike Source is None. No Network created!"
		return None
	if dx < 1 or dy < 1 or dz < 1:
		print "WARNING:\ncreateCooperativeNetwork: One or more Dimensions are less than or equal to 0. No Network created!"
		return None

	network = createNetwork(dx=dx, dy=dy, dz=dz)
	connectSpikeSourcesToNetwork(sourceL=spikeSourceL, sourceR=spikeSourceR, network=network)
	# interconnectLayersForExternalExcitationAndInhibition(network)

	print "Successfully created Network"
	return network

def createNetwork(dx=1, dy=1, dz=1):
	# dx, dy and dz are already >= 1 so no need to check them

	pixels = []
	rows = []
	layers = []
	for zCells in range(1, dy):
		for yCells in range(1, dz):
			for xCells in range(1, dx):
				pixels.append(createANDCell(xCells, yCells, zCells))
			rows.append()	
			pixels = []
		layers.append(rows)
		rows = []
	return layers

def createANDCell(xlabel, ylabel, zlabel):
	# create populations of single neurons of type IF_cond_alpha
	neuronInhLeft = Population(1, IF_cond_alpha(), label="Inhibitor Left {0} - {1} - {2}".format(xlabel, ylabel, zlabel))
	neuronInhRight = Population(1, IF_cond_alpha(), label="Inhibitor Right {0} - {1} - {2}".format(xlabel, ylabel, zlabel))
	neuronCell = Population(1, IF_cond_alpha(), label="Cell Output {0} - {1} - {2}".format(xlabel, ylabel, zlabel))

	Projection(neuronInhLeft, neuronCell, OneToOneConnector(), StaticSynapse(weight=1.0, delay=0.2), receptor_type='inhibitory')
	Projection(neuronInhRight, neuronCell, OneToOneConnector(), StaticSynapse(weight=1.0, delay=0.2), receptor_type='inhibitory')

	andNeuron = neuronInhLeft + neuronInhRight + neuronCell

	return andNeuron

def connectSpikeSourcesToNetwork(sourceL, sourceR, network):
	# connect neurons
	connectionPaternRetinaLeft = []
	for pixel in range(0, dimensionRetinaX):
		for disp in range(disparityMin, disparityMax+1):
			# connect each pixel with as many cells on the same row as disparity values allow. Weight and delay are set to 1 and 0 respectively.
			indexInNetworkLayer = pixel * dimensionRetinaX + pixel + disp
			if indexInNetworkLayer > dimensionRetinaX * dimensionRetinaX - 1:
				break
			connectionPaternRetinaLeft.append((pixel, indexInNetworkLayer, 0.189, 0.2))   
	print connectionPaternRetinaLeft

	connectionPaternRetinaRight = []
	for pixel in range(0, dimensionRetinaX):
		for disp in range(disparityMin, disparityMax+1):
			# connect each pixel with as many cells on the same row as disparity values allow. Weight and delay are set to 1 and 0 respectively.
			indexInNetworkLayer = pixel * dimensionRetinaX + pixel - disp * dimensionRetinaX
			if indexInNetworkLayer < 0:
				break
			connectionPaternRetinaRight.append((pixel, indexInNetworkLayer, 0.189, 0.2))   
	print connectionPaternRetinaRight
		   
	connectionRetinaLeft = Projection(retinaLeft, oneNeuralLayer, FromListConnector(connectionPaternRetinaLeft), StaticSynapse(), receptor_type='excitatory')
	connectionRetinaRight = Projection(retinaRight, oneNeuralLayer, FromListConnector(connectionPaternRetinaRight), StaticSynapse(), receptor_type='excitatory')	

					

