from pyNN.nest import *
from pyNN.utility import normalized_filename

####### Network Parameters #########
dimensionRetinaX = 3
dimensionRetinaY = 3
  
radiusInhibition = 1
radiusExcitation = 1
disparityMin = 0
disparityMax = 1

#####################################

# setup timestep of simulation and minimum and maximum synaptic delays
setup(timestep=0.1, min_delay=0.2, max_delay=5.0)

# create population of network neurons layer by layer
#for layer in range(0, dimensionRetinaY):
    
oneNeuralLayer = Population((dimensionRetinaX, dimensionRetinaX), IF_cond_alpha(), label="Layer 0")

# globally set parameters
# neurons.set({'tau_m':20, 'v_rest':-65}) ...

# initialise records for plotting purposes
oneNeuralLayer.record('spikes')
oneNeuralLayer.record('v')

# create a spike sources firing at spike_times
spikingTimingLeft = [20.0, 50.0, 80.0]
retinaLeft = Population(1, SpikeSourceArray(spike_times = [spikingTimingLeft[0]]), label="Left Retina")

spikingTimingRight = [21.0, 60.0, 51.0]
retinaRight = Population(1, SpikeSourceArray(spike_times = [spikingTimingRight[0]]), label="Right Retina")

for pixel in range(1, dimensionRetinaX):
    retinaLeft += Population(1, SpikeSourceArray(spike_times = [spikingTimingLeft[pixel]]), label="Left Retina")
    retinaRight += Population(1, SpikeSourceArray(spike_times = [spikingTimingRight[pixel]]), label="Right Retina")

retinaLeft.record('spikes')
retinaRight.record('spikes')

# connect neurons
connectionPaternRetinaLeft = []
for pixel in range(0, dimensionRetinaX):
    for disp in range(disparityMin, disparityMax+1):
        # connect each pixel with as many cells on the same row as disparity values allow. Weight and delay are set to 1 and 0 respectively.
        indexInNetworkLayer = pixel*dimensionRetinaX + pixel + disp
        if indexInNetworkLayer > dimensionRetinaX*dimensionRetinaX - 1:
            break
        connectionPaternRetinaLeft.append((pixel, indexInNetworkLayer, 0.189, 0.2))   
print connectionPaternRetinaLeft

connectionPaternRetinaRight = []
for pixel in range(0, dimensionRetinaX):
    for disp in range(disparityMin, disparityMax+1):
        # connect each pixel with as many cells on the same row as disparity values allow. Weight and delay are set to 1 and 0 respectively.
        indexInNetworkLayer = pixel*dimensionRetinaX + pixel - disp*dimensionRetinaX
        if indexInNetworkLayer < 0:
            break
        connectionPaternRetinaRight.append((pixel, indexInNetworkLayer, 0.189, 0.2))   
print connectionPaternRetinaRight
       
connectionRetinaLeft = Projection(retinaLeft, oneNeuralLayer, FromListConnector(connectionPaternRetinaLeft), StaticSynapse(), receptor_type='excitatory')
connectionRetinaRight = Projection(retinaRight, oneNeuralLayer, FromListConnector(connectionPaternRetinaRight), StaticSynapse(), receptor_type='excitatory')

run(200.0)

# plot results
filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
oneNeuralLayer.write_data(filename, annotations={'script_name': __file__})
retinaLeft.write_data(filename, annotations={'script_name': __file__})
retinaRight.write_data(filename, annotations={'script_name': __file__})

cellActivity = oneNeuralLayer.get_data().segments[0]
retinaLeftActivity = retinaLeft.get_data().segments[0]
retinaRightActivity = retinaRight.get_data().segments[0]

from pyNN.utility.plotting import Figure, Panel
figure_filename = filename.replace("pkl", "png")
Figure(Panel(cellActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True), 
       Panel(cellActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True, ylim=(-66, -48)), 
       Panel(retinaLeftActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
       Panel(retinaRightActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
       title="Simple CoNet", annotations="Simulated with NEST").save(figure_filename)
print(figure_filename)

end()

