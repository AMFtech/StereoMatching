import cPickle    


fileName = "../src/realInput/movingPersonFaraway.dat"
 
eventList = []
with open(fileName, 'rb') as allEvents:
    for line in allEvents:
        eventList.append([int(x) for x in line.split()])
         
# # print eventList
 
dimRet = 50
initTime = 10000.0
# totalSimTime = 3000.0
minDisparity = 10
 
retinaL = []
retinaR = []
 
for y in range(0, dimRet):
    retinaR.append([])
    retinaL.append([])
    for x in range(0, dimRet):
        retinaR[y].append([])
        retinaL[y].append([])
 
last_t = [[0.0]*dimRet]*dimRet
for evt in eventList:
    x = evt[1]-1
    y = evt[2]-1
    t = evt[0]/1000.0
    r = evt[4]
     
    lowerBound = (128 - dimRet)/2
    upperBound = (128 + dimRet)/2
    if t < initTime:
        if r == 0:
            if (lowerBound + minDisparity) <= x < upperBound and lowerBound <= y < upperBound:
                if t - last_t[x-(lowerBound + minDisparity)][y-lowerBound] > 0.9:
                    retinaR[x-(lowerBound + minDisparity)][y-lowerBound].append(t)
                last_t[x-(lowerBound + minDisparity)][y-lowerBound] = t    
        elif r == 1:
            if lowerBound <= x < (upperBound - minDisparity) and lowerBound <= y < upperBound:
                if t - last_t[x-lowerBound][y-lowerBound] > 0.9:
                    retinaL[x-lowerBound][y-lowerBound].append(t)
                last_t[x-lowerBound][y-lowerBound] = t
    
            
for y in range(0, dimRet):
    for x in range(0, dimRet):
        if retinaR[y][x] == []:
            retinaR[y][x].append(initTime)
        if retinaL[y][x] == []:
            retinaL[y][x].append(initTime) 

formatedL = retinaL#[list(x) for x in zip(*retinaL)]
formatedR = retinaR#[list(x) for x in zip(*retinaR)]
     
cPickle.dump(formatedL, open('../src/realInput/retinaLeft_50_oneHand_minD_30.p', 'wb'))     
cPickle.dump(formatedR, open('../src/realInput/retinaRight_50_oneHand_minD_30.p', 'wb'))     

rL = cPickle.load(open('../src/realInput/retinaLeft_50_oneHand_minD_30.p', 'rb'))
print rL[10]