
## Simulation Parameters ##

simulationTime = 5000.0       # Total simulation time
simulationTimestep = 0.2    # Temporal resolution of the simulation
minSynapseDelay = 0.2       # The smallest time step for a delay in a synapse connection
maxSynapseDelay = 2.0       # The largest time step for a delay in a synapse connection


## Network Parameters ##

dimensionRetinaX = 3       # Defines the dimension of the x-axis of the input spikes from the retina sensor
dimensionRetinaY = 3       # Defines the dimension of the y-axis of the input spikes from the retina sensor
minDisparity = 0            # Defines the minimum detectable disparity
maxDisparity = 2            # Defines the maximum detectable disparity

radiusExcitation = 0
radiusInhibition = max(dimensionRetinaX, dimensionRetinaY)

## Sample Spike Input ##
# Note that rows in tha array correspond to columns from the retina 


## Neural Parameters ##

# Synaptic parameters

wInhToOut = -20.5#-39.5      # Defines the synaptic weight between an inhibitory neuron and a Cell Output neuron
dInhToOut = minSynapseDelay         # Defines the delay in transmitting the active potential between an inhibitory neuron and a Cell Output neuron

wSSToOut = 20.5#39.5        # Defines the synaptic weight between a Spike Source neuron and a Cell Output neuron
dSSToOut = 1.6#0.8         # Defines the delay in transmitting the active potential between a Spike Source neuron and a Cell Output neuron

wSSToSelfInh = 22.5#49.5#64.0#49.5    # Defines the synaptic weight between a Spike Source (SS) neuron and the inhibitory neuron corresponding to this SS neuron
dSSToSelfInh = minSynapseDelay      # Defines the delay in transmitting the active potential between a Spike Source (SS) neuron and the inhibitory neuron corresponding to this SS neuron

wSSToOtherInh = -22.5#-39.5#-60.0#-39.5  # Defines the synaptic weight between a Spike Source (SS) neuron and the inhibitory neuron corresponding to the other SS neuron
dSSToOtherInh = minSynapseDelay     # Defines the delay in transmitting the active potential between a Spike Source (SS) neuron and the inhibitory neuron corresponding to the other SS neuron

wOutToOutInh = -50.0    # Defines the synaptic weight between individual output neurons which inhibit themselves according to the physical constraints of objects
dOutToOutInh = minSynapseDelay      # Defines the delay between inhibition of output neurons 

wOutToOutExc = 3.0    # Defines the synaptic weight between individual output neurons which excite themselves
dOutToOutExc = minSynapseDelay      # Defines the delay between excitation of output neurons

# Soma's, membrane's and other parameters, see IF_exp_curr model in pyNN wiki
t_synE = 2.0#1.0
t_synI = 2.0#1.0
t_memb = 2.07#1.07
vResetInh = -84.0#-92.0
vResetCO = -90.0#-102.0













    