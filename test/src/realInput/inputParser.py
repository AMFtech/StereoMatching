import cPickle	

fileName = "oneHand.dat"
 
eventList = []
with open(fileName, 'rb') as allEvents:
	for line in allEvents:
		eventList.append([int(x) for x in line.split()])
 		
# # print eventList
 
dimRet = 128
initTime = 10000.0
 
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
 
	if evt[4] == 1:
		retinaR[x][y].append(evt[0]/10000.0)
	elif evt[4] == 0:
		retinaL[x][y].append(evt[0]/10000.0)

for y in range(0, dimRet):
	for x in range(0, dimRet):
		if retinaR[y][x] == []:
			retinaR[y][x].append(initTime)
		if retinaL[y][x] == []:
			retinaL[y][x].append(initTime) 
 	
cPickle.dump(retinaL, open('retinaLeft.p', 'wb')) 	
cPickle.dump(retinaR, open('retinaRight.p', 'wb')) 	

rL = cPickle.load(open('../realInput/retinaLeft.p', 'rb'))
print rL[94]