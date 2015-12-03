from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, maxDisparity, simulationTime

def plotSimulationResults(network=None, layer=0, plotGraphMP=False):
    
    assert network is not None, "Network is not initialised! Visualising failed."
    assert layer > 0 and layer <= dimensionRetinaY, "No such layer in the network."
    import matplotlib.pyplot as plt
    from matplotlib import animation
    
    cellOut = zip(*network)[2]
    print cellOut
    
    if plotGraphMP:
        plotGraphOfMembranePotential(network)
    
    x = range(0, dimensionRetinaX)
    y = range(0, dimensionRetinaX)
    from numpy import meshgrid
    rows, pixels = meshgrid(x,y)
    
    cellValuesAllTimesteps = getMembranePotentialNetwork(cellOut, layer, rows, pixels)
#     print cellValuesAllTimesteps
    cellValuesAllTimesteps = reshapeDimensionNetwork(cellValuesAllTimesteps)
    
    fig = plt.figure()
    
    initialData = createInitialisingData(maxDepolarisation=-50.0, maxPolarisation=-80.0)
    imNet = plt.imshow(initialData, cmap='RdYlGn', interpolation='none', origin='upper')
     
    plt.colorbar()
    plt.xticks(range(0, maxDisparity+1)) 
    plt.yticks(range(0, dimensionRetinaX))
    plt.title("Layer {0}".format(layer))
    args = (cellValuesAllTimesteps, imNet)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=int(simulationTime)*10, interval=100)
    print "Nicely visualising results for layer {0}...".format(layer)       
    plt.show()

def createInitialisingData(maxDepolarisation=-50.0, maxPolarisation=-75.0):
    from itertools import repeat
    initData = []
    # initialise with limiting values to adjust the colorbar and color scheme of the squares
    for rows in range(0, dimensionRetinaX, 2):
        initData.append([maxPolarisation]+list(repeat(maxDepolarisation, maxDisparity))) 
        initData.append([maxDepolarisation]+list(repeat(maxPolarisation, maxDisparity)))
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
    cellsAtFixedLayer = [x[fixedLayer] for x in cells]
    print cellsAtFixedLayer
    cellValues = [x.get_data().segments[0].filter(name='v')[0] for x in cellsAtFixedLayer]
#     print "Layer {0}".format(fixedLayer), cellsAtFixedLayer
    print cellValues
    return cellValues
    
    
def reshapeDimensionNetwork(cellValues):

    assert cellValues is not None, "Cell values are not initialised!"
    
    reshapedCellValues = []
    # slice into chunks of maxDisparity length
    for cellValuesAtT in cellValues:
        reshapedCellValues.append([cellValuesAtT[i:i+maxDisparity+1] for i in range(0, len(cellValuesAtT), maxDisparity+1)])
            
    return reshapedCellValues      
    
    
def plotGraphOfMembranePotential(network=None):
    assert network is not None, "Network is not initialised."
      
    from pyNN.utility import normalized_filename
    filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
    
    cells = network.get_population("Cell Output Population of Network")
    inhL = network.get_population("Inhibitory Population of Left Retina")
    inhR = network.get_population("Inhibitory Population of Right Retina")
    
    from pyNN.utility.plotting import Figure, Panel
    figure_filename = filename.replace("pkl", "png")
    Figure(
        Panel(cells.get_data().segments[0].filter(name='v')[0],
              ylabel="Membrane potential (mV)", xlabel="Time (ms)",
              data_labels=[cells.label], yticks=True, xticks=True, ylim=(-110, -40)),
        Panel(inhL.get_data().segments[0].filter(name='v')[0],
              ylabel="Membrane potential (mV)", xlabel="Time (ms)",
              data_labels=[inhL.label], yticks=True, xticks=True, ylim=(-110, -40)),
        Panel(inhR.get_data().segments[0].filter(name='v')[0],
              ylabel="Membrane potential (mV)", xlabel="Time (ms)",
              data_labels=[inhR.label], yticks=True, xticks=True, ylim=(-110, -40)),        
        title="Cooperative Network"
    ).save(figure_filename)  
    print "Graph is saved under the name: {0}".format(figure_filename)
    
    
    