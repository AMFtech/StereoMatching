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
neuronCount = 150
# populationCount = 7
# trialCount = 1

spikeTimes = []
initialTime = 500.0
numberOfSteps = 500
timeStep = 1000/float(numberOfSteps)
for x in range(0, numberOfSteps):
    nextTime = initialTime + x*timeStep
    spikeTimes.append(nextTime)

collector_ssa = Frontend.Population(neuronCount, Frontend.IF_curr_exp, cell_params_col, label='col')
collector_inj = Frontend.Population(neuronCount, Frontend.IF_curr_exp, cell_params_col, label='col2')
source = Frontend.Population(neuronCount, Frontend.SpikeSourceArray, {'spike_times': spikeTimes} , label='src')
mediator = Frontend.Population(neuronCount, ExternalDevices.SpikeInjector, {'port': 12345} , label='med')

Frontend.Projection(source, collector_ssa, Frontend.OneToOneConnector(weights=22, delays=0.2), target='excitatory') 
Frontend.Projection(mediator, collector_inj, Frontend.OneToOneConnector(weights=-22, delays=0.2), target='excitatory') 

collector_ssa.record()
collector_inj.record()
# source.record()
counter_sent = 0
counter_received = 0
itstimetostop = False
timeatbeg = 0
def receive_spike_cell(label, timet, neuron_ids):
    global live_spikes_connection_sender, counter_received, counter_sent, itstimetostop, timeatbeg
#     if time < 5050:
    if not itstimetostop:
        timeatbeg = time.time()
#         print timeatbeg
        itstimetostop = True
    if time.time() - timeatbeg < 1.1 - 0.5:  
        counter_received += len(neuron_ids)
#            live_spikes_connection_sender.send_spike("med", 0, send_full_keys=True)
  
#         print "received at", time

def th_run(sender):
#     time.sleep(0.5)
#     print "sebnding one"
    global counter_sent
    time_at_beginning = time.time()
    print time_at_beginning
    while time.time() - time_at_beginning < 1.0:
        n = 0
        while n < neuronCount:
            sender.send_spike("med", n, send_full_keys=False)
            n += 1
        counter_sent += neuronCount
#             time.sleep(0.007)
    print time.time()
           

   
def init(label, sender):
    pass
    sender_thread = Thread(target=th_run, args=(sender,))
    sender_thread.start()  
     
ExternalDevices.activate_live_output_for(source, database_notify_host="localhost",database_notify_port_num=19996)
live_spikes_connection_receiver = SpynnakerLiveSpikesConnection(receive_labels=["src"], local_port=19996, send_labels=None)
live_spikes_connection_receiver.add_receive_callback("src", receive_spike_cell)

live_spikes_connection_sender = SpynnakerLiveSpikesConnection(receive_labels=None, local_port=19999, send_labels=["med"])
live_spikes_connection_sender.add_start_callback("med", init)

Frontend.run(run_time)
# Retrieve spikes from the synfire chain population

# print "Spikes count source:", len(source.getSpikes())
# print "Spikes count collector_ssa:", len(collector_ssa.getSpikes())
# print collector_ssa.getSpikes()[:20]
# print "Spikes count collector_inj:", len(collector_inj.getSpikes())

print counter_received, counter_sent
# print collector_inj.getSpikes()[:20]
# print source.getSpikes()

# memPotCO = zip(*collector_ssa.get_v())[2]
# # print memPotCO
# plt.plot(memPotCO)
# plt.axis([0.0, run_time*10, -100.0, -40.0])
# plt.show()
# spikes_injector = injector.getSpikes()
# print "Spikes count injector: ", len(spikes_injector)
Frontend.end()


    

    
          
