from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, maxDisparity, simulationTime
import matplotlib.pyplot as plt    
import time
from threading import Thread

retinaImg = []   

def setupVisualiser():
    global retinaImg
    for x in range(0, dimensionRetinaX):
        zeroList = []
        for y in range(0, dimensionRetinaY):    
            zeroList.append(0)
        retinaImg.append(zeroList)      
    drawerProcess = Thread(target=drawFrames, args=())
    drawerProcess.start()
        
def plotReceivedSpike(populationID, neuronID): 
    from NetworkBuilder import sameDisparityInd, retinaNbhoodL
    global retinaImg
    disp = 0
    
    for d in range(0, maxDisparity+1):
        if populationID in sameDisparityInd[d]:
            disp = d
            break
    
    pixel = 0    
    for p in range(0, dimensionRetinaX):
        if populationID in retinaNbhoodL[p]:
            pixel = p
            break
        
    retinaImg[pixel][neuronID] = disp 
    
def drawFrames():
    global retinaImg
    
    fig = plt.figure()
    plt.ion()
    imNet = plt.imshow(retinaImg, cmap=plt.cm.coolwarm, vmin=0, vmax=maxDisparity, interpolation='none')
    plt.show()
      
    plt.xticks(range(0, dimensionRetinaX)) 
    plt.yticks(range(0, dimensionRetinaY))
    plt.title("Retina View with Colour-Coded Depth")
     
    while True:  
        for x in range(0, len(retinaImg)): 
            imNet.set_data(retinaImg)
            fig.canvas.draw()
        for x in range(0, dimensionRetinaX):
            for y in range(0, dimensionRetinaY):    
                retinaImg[x][y] = 0   
        time.sleep(0.1)
        
    
    
        