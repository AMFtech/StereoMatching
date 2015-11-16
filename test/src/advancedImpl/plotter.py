import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation
from network_parameters import dimensionRetinaX, dimensionRetinaY
# from pyNN.nest import *



def plotSimulationResults(network, retinaLeft, retinaRight, simulationTime, layer=0):
    
    # plot results using pyNN plotting functions
    fixedLayer = layer
    n = dimensionRetinaX
    x = range(0, dimensionRetinaX)
    y = range(0, dimensionRetinaX)
    rows, pixels = np.meshgrid(x,y)
    print "Formatting data for plotting..."
    cellValuesAllTimesteps = getMembranePotentialNetwork(network, fixedLayer, rows, pixels)
    cellValuesAllTimesteps = reshapeDimensionNetwork(cellValuesAllTimesteps)
    
#     cellSpikesAllTimesteps = getSpikesNetwork(network, fixedLayer, rows, pixels)
    
#     retinaLSpikesAllTimes = getSpikesRetina(retinaLeft, fixedLayer)
#     retinaLSpikesAllTimes = reshapeDimensionRetina(retinaLSpikesAllTimes)
#     
#     retinaRSpikesAllTimes = getSpikesRetina(retinaRight, fixedLayer)
#     retinaRSpikesAllTimes = reshapeDimensionRetina(retinaRSpikesAllTimes)    
    
#     fig, (retL, retR, net) = plt.subplots(1,3)
    fig = plt.figure()
    
#     imL = retL.imshow()
#     imR = retR.imshow()
    
    initialData = createInitialisingData(maxDepolarisation=-50.0, maxPolarisation=-80.0)
    imNet = plt.imshow(initialData, cmap='RdYlGn', interpolation='none', origin='upper')
    
    plt.colorbar()
#     plt.xticks([0, dimensionRetinaX]) 
#     plt.yticks([0, dimensionRetinaX])
    args = (cellValuesAllTimesteps, imNet)#, imL, imR)
    anim = animation.FuncAnimation(fig, animate, fargs=args, frames=simulationTime*10, interval=50)       
    plt.show()


def createInitialisingData(maxDepolarisation=-50.0, maxPolarisation=-75.0):
    from itertools import repeat
    initData = []
    for pixels in range(0, dimensionRetinaX):
        initData.append([maxPolarisation]+list(repeat(maxDepolarisation, dimensionRetinaX-1)))
    return initData        

def animate(i, *args):
    imNet = args[1]
#     imR = args[2]
#     imL = args[3]
    
    dataNet = args[0]
#     print data[i]
    imNet.set_data(dataNet[i])
#     imR.set_data(dataNet[i])
#     imL.set_data(dataNet[i])
    if i == 1:
        print "Replaying Animation..."
    return imNet
           
              
def getMembranePotentialNetwork(network=None, fixedLayer=0, meshRows=0, meshPixels=0):
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

def getSpikesNetwork(network=None, fixedLayer=0, meshRows=0, meshPixels=0):
    cellValues = []
    cellValuesRows = []
    for rows, pixels in zip(meshRows, meshPixels):
        for row,pixel in zip(rows, pixels):
            cellValue = network[fixedLayer][row][pixel].get_population(
                "Cell Output {0} - {1} - {2}".format(pixel+1, fixedLayer+1, row+1)
                    ).get_data().segments[0].spiketrains
            cellValuesRows.append(cellValue)
        cellValues.append(cellValuesRows)
        cellValuesRows = []   
    return cellValues

def getSpikesRetina(retina=None, fixedLayer=0):
    retinaValues = []
    for pixel in range(0, dimensionRetinaX):
        retinaValue = retina[fixedLayer][pixel].get_data().segments[0].spiketrains
        retinaValues.append(retinaValue) 
    return retinaValues
    
def reshapeDimensionNetwork(cellValues):

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
    print "Reshaping Network for {0} time steps.".format(len(cellValues))
    return cellValues     

def reshapeDimensionRetina(retinaValues):
    # implement somehow sorting by time of individual cells this is useless
#     from itertools import chain, repeat
#     
#     maxEventsCount = 0
#     for pixel in range(0, dimensionRetinaX):
#         retinaValues[pixel] = list(chain.from_iterable(retinaValues[pixel]))
#         if len(retinaValues[pixel]) > maxEventsCount:
#             maxEventsCount = len(retinaValues[pixel])
#             
#     
#     for pixel in range(0, dimensionRetinaX):
#         if len(retinaValues[pixel]) < maxEventsCount:
#             retinaValues[pixel].extend(repeat([], maxEventsCount - len(retinaValues[pixel])))                                 
#         
#     reshaped = zip(*retinaValues)
#     reshaped = [list(e) for e in reshaped]
#     
#     print "Reshaping Retina for {0} time steps.".format(len(retinaValues))
#     return reshaped    
    pass
    
    
    
    
    
