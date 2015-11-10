import numpy as np
import matplotlib.pyplot as plt

from network_parameters import dimensionRetinaX, dimensionRetinaY, disparityMin, disparityMax
from docutils.nodes import row
# from pyNN.nest import *


def plotSimulationResults(network, retinaLeft, retinaRight):
    
    # plot results using pyNN plotting functions
    fixedLayer = 0
    time = 45
    n = dimensionRetinaX
    x = range(0, dimensionRetinaX)
    y = range(0, dimensionRetinaX)
    rows, pixels = np.meshgrid(x,y)
    cellValues = getMembranePotential(network, fixedLayer, rows, pixels, time)
    print cellValues
    plt.axes([0.025,0.025,0.95,0.95])
    plt.imshow(cellValues, interpolation='none', cmap='gray', origin='upper')
    plt.colorbar(shrink=.92)
    
    plt.xticks([]), plt.yticks([])
    # savefig('../figures/imshow_ex.png', dpi=48)
    plt.show()
    
def getMembranePotential(network=None, fixedLayer=0, meshRows=0, meshPixels=0, time=0):
    cellValues = []
    cellValuesRows = []
    for rows, pixels in zip(meshRows, meshPixels):
        for row,pixel in zip(rows, pixels):
            cellValue = network[fixedLayer][row][pixel].get_population(
                "Cell Output {0} - {1} - {2}".format(pixel+1, fixedLayer+1, row+1)
                    ).get_data().segments[0].filter(name='v')[0][time][0]
            cellValuesRows.append(cellValue)
        cellValues.append(cellValuesRows)
        cellValuesRows = []   
    return cellValues
    

