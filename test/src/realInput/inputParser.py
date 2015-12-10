import cPickle	

fileName = "movingPersons.dat"
 
eventList = []
with open(fileName, 'rb') as allEvents:
	for line in allEvents:
		eventList.append([int(x) for x in line.split()])
 		
# # print eventList
 
dimRet = 20
initTime = 100000.0
 
retinaL = []
retinaR = []
 
for y in range(0, dimRet):
	retinaR.append([])
	retinaL.append([])
	for x in range(0, dimRet):
		retinaR[y].append([])
		retinaL[y].append([])
 
 
for evt in eventList:
	x = evt[1]-1
	y = evt[2]-1
 	
 	lowerBound = 50
 	upperBound = 70
	if lowerBound <= x < upperBound and lowerBound <= y < upperBound:
		if evt[4] == 0:
			retinaR[x-lowerBound][y-lowerBound].append(evt[0]/1000.0)
		elif evt[4] == 1:
			retinaL[x-lowerBound][y-lowerBound].append(evt[0]/1000.0)

for y in range(0, dimRet):
	for x in range(0, dimRet):
		if retinaR[y][x] == []:
			retinaR[y][x].append(initTime)
		if retinaL[y][x] == []:
			retinaL[y][x].append(initTime) 

formatedL = retinaL#[list(x) for x in zip(*retinaL)]
formatedR = retinaR#[list(x) for x in zip(*retinaR)]
 	
cPickle.dump(formatedL, open('retinaLeft_20_pers.p', 'wb')) 	
cPickle.dump(formatedR, open('retinaRight_20_pers.p', 'wb')) 	

rL = cPickle.load(open('../realInput/retinaLeft_20.p', 'rb'))
print rL[10]