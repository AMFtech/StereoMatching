# imports of both spynnaker and external device plugin.
import spynnaker.pyNN as Frontend
import spynnaker_external_devices_plugin.pyNN as ExternalDevices
from spynnaker_external_devices_plugin.pyNN.connections.spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection

from threading import Thread
import time
# plotter in python
import pylab
# initial call to set up the front end (pynn requirement)
Frontend.setup(timestep=0.2, min_delay=0.2, max_delay=2.0)

run_time = 2000

cell_params_col = {'tau_m': 2.07, 'tau_refrac': 2.0,'tau_syn_E': 2.0, 'tau_syn_I': 2.0, 'v_reset': -90.0}
# create synfire populations (if cur exp)
neuronCount = 1
populationCount = 1
trialCount = 1000000

collector = []
injector = []
for pop in range(0, populationCount):
    collector.append(Frontend.Population(neuronCount, Frontend.IF_curr_exp, cell_params_col, label='c{0}'.format(pop)))
    injector.append(Frontend.Population(neuronCount, ExternalDevices.SpikeInjector,{'port':12000+pop}, label='i{0}'.format(pop)))
    Frontend.Projection(injector[pop], collector[pop], Frontend.OneToOneConnector(weights=22, delays=0.2), target='excitatory') 
    collector[pop].record()
#     ExternalDevices.activate_live_output_for(collector[pop], database_notify_host="localhost",database_notify_port_num=19996)

colLables = [c.label for c in collector]
injLabels = [i.label for i in injector] 
 
def receive_spike_cell(label, time, neuron_ids):
    pass
#     print "received at", time

counter = 0
def thread_run(liveConnectionRetina): 
    global injLabels, counter
    
    strt = time.time()
    while (time.time() - strt) < 1.0:
#         print "trial no.", trial
#         print "{0:.5f}".format(time.time())
        for label in injLabels:
            for neuronID in range(0, neuronCount): 
                liveConnectionRetina.send_spike(label, neuronID, send_full_keys=False)
                counter += 1
    #             print "sent"
    #         print "{0:.5f}".format(time.time())    
#         time.sleep(0.002)
#         print "{0:.5f}".format(time.time())
        
    print counter
    print strt, time.time()
         
def init_thread(label, sender):
        sender_thread = Thread(target=thread_run, args=(sender,))
        sender_thread.start()  
     
    

# live_spikes_connection_receiver = SpynnakerLiveSpikesConnection(receive_labels=colLables, local_port=19996, send_labels=None)
live_spikes_connection_sender = SpynnakerLiveSpikesConnection(receive_labels=None, local_port=19999, send_labels=injLabels)

# for labelc in colLables:
#     live_spikes_connection_receiver.add_receive_callback(labelc, receive_spike_cell)

live_spikes_connection_sender.add_start_callback(injLabels[0], init_thread)

Frontend.run(run_time)
# Retrieve spikes from the synfire chain population
sum_all_spikes = 0
for c in collector:
    spikes_collector = c.getSpikes()
    print "Spikes count ", c.label, len(spikes_collector)
#     print "lost % :", 100.0 - (len(spikes_collector) * 100.0)/ float(neuronCount*trialCount) 
    sum_all_spikes += len(spikes_collector)
# spikes_injector = injector.getSpikes()
# print "Spikes count injector: ", len(spikes_injector)
print "summed spikes: ", sum_all_spikes
print "Total lost %: ", 100.0 - float(sum_all_spikes) * 100.0 / float(counter)
Frontend.end()


    

    
          
