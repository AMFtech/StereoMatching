# imports of both spynnaker and external device plugin.
import spynnaker.pyNN as Frontend
import spynnaker_external_devices_plugin.pyNN as ExternalDevices
from spynnaker_external_devices_plugin.pyNN.connections.spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection

from threading import Thread
import time
# plotter in python
import matplotlib.pyplot as plt
# initial call to set up the front end (pynn requirement)
Frontend.setup(timestep=0.2, min_delay=0.2, max_delay=2.0)

run_time = 2000

cell_params_col = {'tau_m': 2.07, 'tau_refrac': 2.0,'tau_syn_E': 2.0, 'tau_syn_I': 2.0, 'v_reset': -90.0}
# create synfire populations (if cur exp)
neuronCount = 100
populationCount = 20

spikeTimes = []
initialTime = 0.0
numberOfSteps = 155
timeStep = 1000/float(numberOfSteps)
for x in range(0, numberOfSteps):
    nextTime = initialTime + x*timeStep
    spikeTimes.append(nextTime)
    
counter_received_spikes = []
collector_labels = []
collector = []
source = []
for pop in range(0, populationCount):
    collector.append(Frontend.Population(neuronCount, Frontend.IF_curr_exp, cell_params_col, label='{0}'.format(pop)))
    source.append(Frontend.Population(neuronCount, Frontend.SpikeSourceArray, {'spike_times': spikeTimes} , label='s{0}'.format(pop)))
    Frontend.Projection(source[pop], collector[pop], Frontend.OneToOneConnector(weights=22, delays=0.2), target='excitatory') 
    collector[pop].record()
    counter_received_spikes.append(0)
    collector_labels.append('{0}'.format(pop))

def receive_spike_cell(label, time, neuron_ids):
    if time < 5050 :
        counter_received_spikes[int(label)] += len(neuron_ids) 

for col in collector:     
    ExternalDevices.activate_live_output_for(col, database_notify_host="localhost",database_notify_port_num=19996)
    
live_spikes_connection_receiver = SpynnakerLiveSpikesConnection(receive_labels=collector_labels, local_port=19996, send_labels=None)

for label in collector_labels:
    live_spikes_connection_receiver.add_receive_callback(label, receive_spike_cell)


Frontend.run(run_time)

total_spikes_count = 0
for col in collector:
    total_spikes_count += len(col.getSpikes())

print "Spikes count collector:", total_spikes_count
print "Spikes count received:", sum(counter_received_spikes)

Frontend.end()


    

    
          
