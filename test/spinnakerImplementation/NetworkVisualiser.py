from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, maxDisparity, simulationTime

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
    
    imNet = plt.imshow(initialData, cmap='gray', interpolation='none', origin='upper')
    
    plt.xticks(range(0, dimensionRetinaX)) 
    plt.yticks(range(0, dimensionRetinaY))
    plt.title("Disparity Map {0}".format(disparity))
    args = (framesOfSpikes, imNet)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=int(simulationTime)*10, interval=100)
          
    plt.show()

def createInitialisingData():
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
    
def generateFrames(sortedSpikes):
    
    print "\t Preparing frames..."
    allFrames = []
    for frame in range(0, int(simulationTime)*10):
        allFrames.append([ [ 1 if frame/10.0 in sortedSpikes[x][y] else 0 for y in range(0, dimensionRetinaY) ] for x in range(0, dimensionRetinaX)])
    
    return allFrames
    
    
    
        