import cPickle as cp
import time
from multiprocessing import Process
from SimulationAndNetworkSettings import minDisparity, dimensionRetinaX
    
def runThread(liveConnectionRetinas):
    retinasSpikes = [(10, 0, 0, 1), (11, 0, 0, 0), (1000, 0, 1, 1), (1001, 1, 1, 0), (3000, 0, 2, 1), (3001, 2, 2, 0), (4000, 0, 0, 1)]#cp.load(open('../src/realInput/timesorted_5_persAway.p', 'rb'))#
    
    last_spike_time = 0.0
    for spike, index in zip(retinasSpikes, range(0, len(retinasSpikes)-1)):
        # extract label (x coordinate), neuronid (y coordinate)
        t, x, y, r = spike
        tNext = retinasSpikes[index+1][0]
        if r == 1:
            if x <= dimensionRetinaX - minDisparity-1:
                print "Spike has been sent from RetL_{0}".format(x)
                liveConnectionRetinas.send_spike(label= "RetL_{0}".format(x), neuron_id=y, send_full_keys=True)
        else:
            if x >= minDisparity:
                print "Spike has been sent from RetR_{0}".format(x)
                liveConnectionRetinas.send_spike(label= "RetR_{0}".format(x-minDisparity), neuron_id=y, send_full_keys=True) 
        time.sleep((tNext - t)/1000.0)
    

def startInjecting(label, liveConnectionRetinas): 
    retinasThreads = Process(target=runThread, args=(liveConnectionRetinas,))
    retinasThreads.start()