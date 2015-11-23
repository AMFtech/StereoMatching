from SimulationAndNetworkSettings import dimensionRetinaX, maxDisparity, simulationTime

def plotSimulationResults(network=None):
    
    assert network is not None, "Network is not initialised! Visualising failed."
    
    import matplotlib.pyplot as plt
    from matplotlib import animation
    
    cellOut = network.get_population("Cell Output Population of Network")
    
    fixedLayer = 0
    x = range(0, dimensionRetinaX)
    y = range(0, dimensionRetinaX)
    from numpy import meshgrid
    rows, pixels = meshgrid(x,y)
    
    cellValuesAllTimesteps = getMembranePotentialNetwork(cellOut, fixedLayer, rows, pixels)
    cellValuesAllTimesteps = reshapeDimensionNetwork(cellValuesAllTimesteps)
    
    fig = plt.figure()
    
    initialData = createInitialisingData(maxDepolarisation=-50.0, maxPolarisation=-80.0)
    imNet = plt.imshow(initialData, cmap='RdYlGn', interpolation='none', origin='upper')
    
    plt.colorbar()
    plt.xticks(range(0, maxDisparity+1)) 
    plt.yticks(range(0, dimensionRetinaX))
    args = (cellValuesAllTimesteps, imNet)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=int(simulationTime)*10, interval=100)
    print "Nicely visualising results..."       
    plt.show()

def createInitialisingData(maxDepolarisation=-50.0, maxPolarisation=-75.0):
    from itertools import repeat
    initData = []
    for rows in range(0, dimensionRetinaX):
        initData.append([maxPolarisation]+list(repeat(maxDepolarisation, maxDisparity))) 
    return initData        

def animate(i, *args):
    imNet = args[1]
    dataNet = args[0]
    imNet.set_data(dataNet[i])
    if i == 1:
        print "Replaying Animation..."
    return imNet
    
def getMembranePotentialNetwork(cells=None, fixedLayer=0, meshRows=0, meshPixels=0):
    assert cells is not None, "Cells are not initialised!"   
    cellValues = cells.get_data().segments[0].filter(name='v')[0]
    return cellValues
    
    
def reshapeDimensionNetwork(cellValues):

    assert cellValues is not None, "Cell values are not initialised!"
    
    reshapedCellValues = []
    # slice into chunks of maxDisparity length
    for cellValuesAtT in cellValues:
        reshapedCellValues.append([cellValuesAtT[i:i+maxDisparity+1] for i in range(0, len(cellValuesAtT), maxDisparity+1)])
            
    return reshapedCellValues      
    