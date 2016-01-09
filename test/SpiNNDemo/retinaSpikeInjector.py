import cPickle as cp
import time
from threading import Thread

    
def runThread(liveConnectionRetinas):
    retinasSpikes = [(10, 2, 1, 1), (11, 2, 1, 0), (115, 2, 1, 0), (120, 2, 1, 0), (117, 2, 1, 1),(170, 2, 1, 1)]#cp.load(open('../src/realInput/timesorted_50_persAway.p', 'rb'))
    
    populationLabel = ""
    last_spike_time = 0.0
    for spike, index in zip(retinasSpikes, range(0, len(retinasSpikes)-1)):
        # extract label (x coordinate), neuronid (y coordinate)
        t, x, y, r = spike
        tNext = retinasSpikes[index+1][0]
        if r == 1:
            populationLabel = "RetL_{0}".format(x)
        else:
            populationLabel = "RetR_{0}".format(x)    
        #imlement some sort of timer to inject spikes at times t   
         
        liveConnectionRetinas.send_spike(label=populationLabel, neuron_id=y, send_full_keys=True)
        print "Spike has been injected."
        time.sleep((tNext - t)/1000.0)
    

def startInjecting(label, liveConnectionRetinas): 
    retinasThreads = Thread(target=runThread, args=(liveConnectionRetinas,))
    retinasThreads.start()