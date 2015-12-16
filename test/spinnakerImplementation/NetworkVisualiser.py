from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, maxDisparity, simulationTime
    
def plotExperiment(retinaLeft, retinaRight, network):
    # TODO: make it work
#     import matplotlib.pyplot as plt
#     plotRetinaSpikes(retinaLeft, "Retina Left")
#     plotRetinaSpikes(retinaRight, "Retina Right")
#     plotDisparityMap(network, 1)
#     plt.show()
    spikesCountL = sum([sum(x.get_spike_counts().values()) for x in retinaLeft])
    spikesCountR = sum([sum(x.get_spike_counts().values()) for x in retinaRight])
    spikesCountN = sum([sum(x[2].get_spike_counts().values()) for x in network])
      
    print "Experiment Results:"
    print "\tTotal Number of Spikes in the Network: %d"%spikesCountN
    print "\tTotal Number of Spikes in the Left Retina: %d"%spikesCountL
    print "\tTotal Number of Spikes in the Right Retina: %d"%spikesCountR
    print "\tTotal Number of non-matched evets: %d"%(spikesCountL+spikesCountR-spikesCountN)

    plotDisparityHistogram(network)
#     plotRetinaSpikes(retinaLeft, "Retina Left")
#     plotColorCodedNetworkSpikes(network)

def plotColorCodedNetworkSpikes(network):
    assert network is not None, "Network is not initialised! Visualising failed."
    import matplotlib as plt
    from NetworkBuilder import sameDisparityInd
    
    cellsOutSortedByDisp = []
    spikes = []
    for disp in range(0, maxDisparity+1):
        cellsOutSortedByDisp.append([network[x][2] for x in sameDisparityInd[disp]])
        spikes.append([x.getSpikes() for x in cellsOutSortedByDisp[disp]])
    
    sortedSpikes = sortSpikesByColor(spikes)
    print sortedSpikes
    framesOfSpikes = generateColoredFrames(sortedSpikes)
    print framesOfSpikes
    
    fig = plt.figure()
    
    initialData = createInitialisingDataColoredPlot()
    
    imNet = plt.imshow(initialData[0], c=initialData[1], cmap=plt.cm.coolwarm, interpolation='none', origin='upper')
    
    plt.xticks(range(0, dimensionRetinaX)) 
    plt.yticks(range(0, dimensionRetinaY))
    plt.title("Disparity Map {0}".format(disparity))
    args = (framesOfSpikes, imNet)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=int(simulationTime)*10, interval=30)
          
    plt.show()
    

def plotDisparityHistogram(network=None):
    assert network is not None, "Network is not initialised! Visualising failed."
    import matplotlib.pyplot as plt
    from NetworkBuilder import sameDisparityInd
    
    spikesPerDisparityMap = []
    for d in range(0, maxDisparity+1):
        cellsOut = [network[x][2] for x in sameDisparityInd[d]]
        spikesPerDisparityMap.append(sum([sum(x.get_spike_counts().values()) for x in cellsOut]))
    
    print spikesPerDisparityMap
    
    plt.bar(range(0, maxDisparity+1), spikesPerDisparityMap, align='center')
    
    plt.show()
    
def plotRetinaSpikes(retina=None, label=""):
    
    assert retina is not None, "Network is not initialised! Visualising failed."
    import matplotlib.pyplot as plt
    from matplotlib import animation
    
    print "Visualising {0} Spikes...".format(label) 

    spikes = [x.getSpikes() for x in retina]
#     print spikes
    
    sortedSpikes = sortSpikes(spikes)
#     print sortedSpikes
    
    framesOfSpikes = generateFrames(sortedSpikes)
#     print framesOfSpikes
    
    x = range(0, dimensionRetinaX)
    y = range(0, dimensionRetinaY)
    from numpy import meshgrid
    rows, pixels = meshgrid(x,y)
    
    fig = plt.figure()
    
    initialData = createInitialisingData()
    
    imNet = plt.imshow(initialData, cmap='green', interpolation='none', origin='upper')
    
    plt.xticks(range(0, dimensionRetinaX)) 
    plt.yticks(range(0, dimensionRetinaY))
    args = (framesOfSpikes, imNet)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=int(simulationTime)*10, interval=30)
          
    plt.show()


def plotDisparityMap(network=None, disparity=0):
    
    assert network is not None, "Network is not initialised! Visualising failed."
    assert disparity >= 0 and disparity <= maxDisparity, "No such disparity map in the network."
    import matplotlib.pyplot as plt
    from matplotlib import animation
    from NetworkBuilder import sameDisparityInd
    
    print "Visualising results for disparity value {0}...".format(disparity) 
    
    cellsOut = [network[x][2] for x in sameDisparityInd[disparity]]

    spikes = [x.getSpikes() for x in cellsOut]
#     print spikes
    
    sortedSpikes = sortSpikes(spikes)
#     print sortedSpikes
    
    framesOfSpikes = generateFrames(sortedSpikes)
#     print framesOfSpikes
    
    x = range(0, dimensionRetinaX)
    y = range(0, dimensionRetinaY)
    from numpy import meshgrid
    rows, pixels = meshgrid(x,y)
    
    fig = plt.figure()
    
    initialData = createInitialisingData()
#     print initialData
    imNet = plt.imshow(initialData, cmap='gray', interpolation='none', origin='upper')
    
    plt.xticks(range(0, dimensionRetinaX)) 
    plt.yticks(range(0, dimensionRetinaY))
    plt.title("Disparity Map {0}".format(disparity))
    args = (framesOfSpikes, imNet)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=int(simulationTime)*10, interval=30)
          
    plt.show()

def createInitialisingData():
    from itertools import repeat
    initData = [ [ 0 if x % 2 == 0 else 1 for y in range(0, dimensionRetinaY) ] for x in range(0, dimensionRetinaX)]
    return initData        

def createInitialisingDataColoredPlot():
    from itertools import repeat
    initData = [ [ 0 if x % 2 == 0 else 1 for y in range(0, dimensionRetinaY) ] for x in range(0, dimensionRetinaX)]
    return initData

def animate(i, *args):
    imNet = args[1]
    dataNet = args[0]
    imNet.set_data(dataNet[i])
    if i == 1:
        print "\t Replaying Animation..."
    return imNet
    
def sortSpikes(spikes):
    
    print "\t Sorting spikes..."
    sortedSpikes = [ [ [] for y in range(0, dimensionRetinaY) ] for x in range(0, dimensionRetinaX)]
    colIndex = 0
    for col in spikes:
        for spike in col: 
            sortedSpikes[colIndex][int(spike[0])].append(round(spike[1], 1)) 
        colIndex += 1
    return sortedSpikes

def sortSpikesByColor(spikes):
    
    print "\t Sorting spikes by disparity..."
    sortedSpikes = [ [ [] for y in range(0, dimensionRetinaY) ] for x in range(0, dimensionRetinaX)]
    colIndex = 0
    for d in range(0, len(spikes)):
        for col in spikes[d] :
            for spike in col: 
                sortedSpikes[colIndex][int(spike[0])].append((round(spike[1], 1), d)) 
            colIndex += 1
        colIndex = 0   
    return sortedSpikes
    
def generateFrames(sortedSpikes):
    
    print "\t Preparing frames..."
    allFrames = []
    for frame in range(0, int(simulationTime)*10):
        allFrames.append([ [ 1 if frame/10.0 in sortedSpikes[x][y] else 0 for y in range(0, dimensionRetinaY) ] for x in range(0, dimensionRetinaX)])
    
    return allFrames

def generateColoredFrames(sortedSpikes):
    
    print "\t Preparing frames..."
    allFrames = []
    fullFrame = [[-1 for x in range(0, dimensionRetinaX)] for y in range(0, dimensionRetinaY)]
    for x in range(0, dimensionRetinaX):
        for y in range(0, dimensionRetinaY): 
            if (sortedSpikes[x][y] != []):
                eventsPerPixel = zip(*sortedSpikes[x][y])
                if float(frame) in eventsPerPixel[0]:
                    fullFrame[x][y] = eventsPerPixel[1][0]
            print fullFrame        
            fullFrame[x][y] = -1
    allFrames.append(list(fullFrame))        
    print allFrames
    return allFrames
    
    
    
        