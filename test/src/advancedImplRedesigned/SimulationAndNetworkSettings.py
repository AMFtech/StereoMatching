
## Simulation Parameters ##

simulationTime = 50.0       # Total simulation time
simulationTimestep = 0.1    # Temporal resolution of the simulation
minSynapseDelay = 0.1       # The smallest time step for a delay in a synapse connection
maxSynapseDelay = 2.0       # The largest time step for a delay in a synapse connection


## Network Parameters ##

dimensionRetinaX = 5        # Defines the dimension of the x-axis of the input spikes from the retina sensor
dimensionRetinaY = 1        # Defines the dimension of the y-axis of the input spikes from the retina sensor
minDisparity = 0            # Defines the minimum detectable disparity
maxDisparity = 1            # Defines the maximum detectable disparity

radiusExcitation = 2
radiusInhibition = max(dimensionRetinaX, dimensionRetinaY)