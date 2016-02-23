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
# neurons per population and the length of runtime in ms for the simulation,
# as well as the expected weight each spike will contain
# n_neurons = 100
run_time = 3000
# weight_to_spike = 2.0
# neural parameters of the ifcur model used to respond to injected spikes.
# (cell params for a synfire chain)
cell_params_inh = {'tau_m': 2.07, 'tau_refrac': 2.0,'tau_syn_E': 2.0, 'tau_syn_I': 2.0, 'v_reset': -84.0}
cell_params_col = {'tau_m': 2.07, 'tau_refrac': 2.0,'tau_syn_E': 2.0, 'tau_syn_I': 2.0, 'v_reset': -90.0}
# create synfire populations (if cur exp)
collector = Frontend.Population(1, Frontend.IF_curr_exp, cell_params_col, label='collector')
inh_left = Frontend.Population(1, Frontend.IF_curr_exp, cell_params_inh, label='inh_left')
inh_right = Frontend.Population(1, Frontend.IF_curr_exp, cell_params_inh, label='inh_right')
# Create injection populations

ret_left = Frontend.Population(1, ExternalDevices.SpikeInjector,{'port':12345}, label='ret_left')
# rets = []
# for x in range(0, 13):
#     rets.append(Frontend.Population(1, ExternalDevices.SpikeInjector,{'port':13400+x,}, label='ret_left_'.format(x)))
ret_right = Frontend.Population(1, ExternalDevices.SpikeInjector,{'port':12346}, label='ret_right')
# Create a connection from the injector into the populations
excDelay = 1.6
minDelay = 0.2
w1 = 22.5
w2 = 20.5
Frontend.Projection(ret_left, inh_left, Frontend.OneToOneConnector(weights=w1, delays=0.2), target='excitatory')
Frontend.Projection(ret_left, inh_right, Frontend.OneToOneConnector(weights=-w1, delays=0.2), target='inhibitory')
Frontend.Projection(ret_left, collector, Frontend.OneToOneConnector(weights=w2, delays=1.6), target='excitatory')
   
Frontend.Projection(ret_right, inh_right, Frontend.OneToOneConnector(weights=w1, delays=0.2), target='excitatory')
Frontend.Projection(ret_right, inh_left, Frontend.OneToOneConnector(weights=-w1, delays=0.2), target='inhibitory')
Frontend.Projection(ret_right, collector, Frontend.OneToOneConnector(weights=w2, delays=1.6), target='excitatory')
     
Frontend.Projection(inh_left, collector, Frontend.OneToOneConnector(weights=w2, delays=0.2), target='inhibitory')
Frontend.Projection(inh_right, collector, Frontend.OneToOneConnector(weights=w2, delays=0.2), target='inhibitory')

# record spikes from the synfire chains so that we can read off valid results
# in a safe way afterwards, and verify the behavior
collector.record()
inh_left.record()
inh_right.record()
# Activate the sending of live spikes
ExternalDevices.activate_live_output_for(inh_left, database_notify_host="localhost",database_notify_port_num=19996)
ExternalDevices.activate_live_output_for(collector, database_notify_host="localhost",database_notify_port_num=19996)
ExternalDevices.activate_live_output_for(inh_right, database_notify_host="localhost",database_notify_port_num=19996)
# Create a sender of packets for the forward population
def send_spike_retina(label, sender):
    print "Sending spike from ", label
    sender.send_spike(label, 0, send_full_keys=True)
# if not using the c visualiser, then a new spynnaker live spikes connection
# is created to define that there are python code which receives the
# outputted spikes.
 
def receive_spike_cell(label, time, neuron_ids):
    print label, " received a spike at time ", time
 
def threadLeft_run(liveConnectionRetina):
    retinasSpikes = [(1, 0, 0, 0), (100, 0, 0, 0), (250, 0, 0, 0), (300, 0, 0, 0)]#cp.load(open('../src/realInput/timesorted_50_persAway.p', 'rb'))
    last_spike_time = 0.0
    for spike, index in zip(retinasSpikes, range(0, len(retinasSpikes)-1)):
        t, x, y, r = spike
        tNext = retinasSpikes[index+1][0]    
        send_spike_retina("ret_left", liveConnectionRetina)
        time.sleep((tNext - t)/1000.0)
         
def threadRight_run(liveConnectionRetina):
    retinasSpikes = [(1, 0, 0, 1), (10, 0, 0, 1), (11, 0, 0, 0), (20, 0, 0, 1), (25, 0, 0, 0), (30, 0, 0, 1)]#cp.load(open('../src/realInput/timesorted_50_persAway.p', 'rb'))
    last_spike_time = 0.0
    for spike, index in zip(retinasSpikes, range(0, len(retinasSpikes)-1)):
        t, x, y, r = spike
        tNext = retinasSpikes[index+1][0]  
        if r == 1:  
            send_spike_retina("ret_right", liveConnectionRetina)
        else:
            send_spike_retina("ret_left", liveConnectionRetina)  
        time.sleep((tNext - t)/1000.0)
         
def init_thread(label, sender):
    if label == "ret_left":
        sender_thread = Thread(target=threadLeft_run, args=(sender,))
        sender_thread.start()
    else:
        sender_thread = Thread(target=threadRight_run, args=(sender,))
        sender_thread.start()  
     
live_spikes_connection_receiver = SpynnakerLiveSpikesConnection(receive_labels=["collector", "inh_left", "inh_right"], local_port=19996, send_labels=None)
live_spikes_connection_receiver.add_receive_callback("collector", receive_spike_cell)
live_spikes_connection_receiver.add_receive_callback("inh_left", receive_spike_cell)
live_spikes_connection_receiver.add_receive_callback("inh_right", receive_spike_cell)
 
live_spikes_connection_sender = SpynnakerLiveSpikesConnection(receive_labels=None, local_port=19999, send_labels=["ret_right", "ret_left"])
# Set up callbacks to occur at the start of simulation
# live_spikes_connection_sender.add_start_callback("ret_left", init_thread)
live_spikes_connection_sender.add_start_callback("ret_right", init_thread)
 
# Run the simulation on spiNNaker
 
Frontend.run(run_time)
# Retrieve spikes from the synfire chain population
spikes_collector = collector.getSpikes()
print "Spikes count collector: ", len(spikes_collector)
 
spikes_inh_left = inh_left.getSpikes()
print "Spikes count inh left: ", len(spikes_inh_left)
 
spikes_inh_right = inh_right.getSpikes()
print "Spikes count inh right: ", len(spikes_inh_right)
# If there are spikes, plot using matplotlib
if len(spikes_collector) != 0:
    pylab.figure()
    if len(spikes_collector) != 0:
        pylab.plot([i[1] for i in spikes_collector],
        [i[0] for i in spikes_collector], "b.")
        pylab.ylabel('neuron id')
        pylab.xlabel('Time/ms')
        pylab.title('spikes')
        pylab.show()
else:
    print "No spikes received"
# Clear data structures on spiNNaker to leave the machine in a clean state for
# future executions
Frontend.end()


    

    
          
