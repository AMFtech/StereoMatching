import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation
from network_parameters import dimensionRetinaX, dimensionRetinaY
from docutils.nodes import row
# from pyNN.nest import *



def plotSimulationResults(network, retinaLeft, retinaRight, simulationTime):
    
    # plot results using pyNN plotting functions
    fixedLayer = 0
    n = dimensionRetinaX
    x = range(0, dimensionRetinaX)
    y = range(0, dimensionRetinaX)
    rows, pixels = np.meshgrid(x,y)
    print "Formatting data for plotting..."
    cellValuesAllTimesteps = getMembranePotential(network, fixedLayer, rows, pixels)
    print "Before reshaping"
    print cellValuesAllTimesteps
    cellValuesAllTimesteps = reshapeDimension(cellValuesAllTimesteps)
    print "After reshaping"
    print cellValuesAllTimesteps
    
    plt.axes([0.025,0.025,0.95,0.95])
    
    fig = plt.figure()
    im = plt.imshow(cellValuesAllTimesteps[0], interpolation='none', origin='upper')
    
    plt.colorbar(shrink=.92)
    plt.xticks([]), plt.yticks([])
    args = (cellValuesAllTimesteps, im)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=simulationTime*10, interval=1000)       
    plt.show()


# def init():
#     global im, cellValuesAllTimesteps
#     im.set_data(cellValuesAllTimesteps[0])

def animate(i, *args):
    im = args[1]
    data = args[0]
    print data[i]
    im.set_data(data[i])
    return im
           
              
def getMembranePotential(network=None, fixedLayer=0, meshRows=0, meshPixels=0):
    cellValues = []
    cellValuesRows = []
    for rows, pixels in zip(meshRows, meshPixels):
        for row,pixel in zip(rows, pixels):
            cellValue = network[fixedLayer][row][pixel].get_population(
                "Cell Output {0} - {1} - {2}".format(pixel+1, fixedLayer+1, row+1)
                    ).get_data().segments[0].filter(name='v')[0]
            cellValuesRows.append(cellValue)
        cellValues.append(cellValuesRows)
        cellValuesRows = []   
    return cellValues
    
def reshapeDimension(cellValues):

    from itertools import chain
    
    for rows in range(0, dimensionRetinaX):
            for colls in range(0, dimensionRetinaX):
                cellValues[rows][colls] = list(chain.from_iterable(cellValues[rows][colls]))
    newlst = []
    for t in range(0,dimensionRetinaX):
        elem = list(zip(*cellValues[t]))
        elem = [list(e) for e in elem]
        newlst.append(elem)
    
    newlst2 = list(zip(*[list(e) for e in newlst]))
    cellValues = [list(e) for e in newlst2]
    print "Reshaping for {0} time steps.".format(len(cellValues))
    return cellValues        
    
    
    
    
    
    
