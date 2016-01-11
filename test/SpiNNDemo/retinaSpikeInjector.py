import cPickle as cp
import time
from multiprocessing import Process

    
def runThread(liveConnectionRetinas):
    retinasSpikes = cp.load(open('../src/realInput/timesorted_5_persAway.p', 'rb'))#[(10, 1, 3, 1), (11, 2, 3, 0), (120, 0, 2, 1), (121, 1, 2, 0),(170, 2, 2, 1)]
    print retinasSpikes[0], retinasSpikes[1], retinasSpikes[2]
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
#         print "Spike has been injected."
        time.sleep((tNext - t)/1000.0)
    

def startInjecting(label, liveConnectionRetinas): 
    retinasThreads = Process(target=runThread, args=(liveConnectionRetinas,))
    retinasThreads.start()