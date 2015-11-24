
## Simulation Parameters ##

simulationTime = 50.0       # Total simulation time
simulationTimestep = 0.1    # Temporal resolution of the simulation
minSynapseDelay = 0.1       # The smallest time step for a delay in a synapse connection
maxSynapseDelay = 2.0       # The largest time step for a delay in a synapse connection


## Network Parameters ##

dimensionRetinaX = 1        # Defines the dimension of the x-axis of the input spikes from the retina sensor
dimensionRetinaY = 1        # Defines the dimension of the y-axis of the input spikes from the retina sensor
minDisparity = 0            # Defines the minimum detectable disparity
maxDisparity = 0            # Defines the maximum detectable disparity

radiusExcitation = 0
radiusInhibition = max(dimensionRetinaX, dimensionRetinaY)

## Sample Spike Input ##
retLeftSpikes = \
    [[[1,2,3,4,5,6], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]],
     [[100], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]],
     [[100], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]],
     [[100], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]]
    ]

retRightSpikes = \
    [[[100], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]],
     [[100], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]],
     [[100], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]],
     [[100], [100], [100], [100],[100],  [100], [100], [100],[100],  [100], [100], [100]]
    ]    

## Neural Parameters ##

# Synaptic parameters

wInhToOut = -39.5      # Defines the synaptic weight between an inhibitory neuron and a Cell Output neuron
dInhToOut = 0.1         # Defines the delay in transmitting the active potential between an inhibitory neuron and a Cell Output neuron

wSSToOut = 39.5        # Defines the synaptic weight between a Spike Source neuron and a Cell Output neuron
dSSToOut = 0.69         # Defines the delay in transmitting the active potential between a Spike Source neuron and a Cell Output neuron

wSSToSelfInh = 49.5    # Defines the synaptic weight between a Spike Source (SS) neuron and the inhibitory neuron corresponding to this SS neuron
dSSToSelfInh = 0.1      # Defines the delay in transmitting the active potential between a Spike Source (SS) neuron and the inhibitory neuron corresponding to this SS neuron

wSSToOtherInh = -39.5  # Defines the synaptic weight between a Spike Source (SS) neuron and the inhibitory neuron corresponding to the other SS neuron
dSSToOtherInh = 0.1     # Defines the delay in transmitting the active potential between a Spike Source (SS) neuron and the inhibitory neuron corresponding to the other SS neuron

wOutToOutInh = -50.0    # Defines the synaptic weight between individual output neurons which inhibit themselves according to the physical constraints of objects
dOutToOutInh = 0.1      # Defines the delay between inhibition of output neurons 

wOutToOutExc = 0.0    # Defines the synaptic weight between individual output neurons which excite themselves
dOutToOutExc = 0.1      # Defines the delay between excitation of output neurons

# Soma's, membrane's and other parameters, see IF_exp_curr model in pyNN wiki
t_synE = 1.0
t_synI = 1.0
t_memb = 1.07
vResetInh = -92.0
vResetCO = -102.0













    