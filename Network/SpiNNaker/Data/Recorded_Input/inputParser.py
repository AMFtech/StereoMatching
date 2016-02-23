import cPickle	


fileName = "artificial_events.dat"
experimentName = fileName[:-4]

eventList = []
with open(fileName, 'rb') as allEvents:
	for line in allEvents:
		eventList.append([int(x) for x in line.split()])
  		
# # print eventList
  
dimRetX = 40
dimRetY = 30
initTime = 10000.0
  
retinaL = []
retinaR = []
  
for y in range(0, dimRetX):
	retinaR.append([])
	retinaL.append([])
	for x in range(0, dimRetY):
		retinaR[y].append([])
		retinaL[y].append([])
  
last_tL = [[0.0]]#[[0.0]*dimRetY]*dimRetX
last_tR = [[0.0]]#[[0.0]*dimRetY]*dimRetX
for x in range(0, dimRetX):
	for y in range(0, dimRetY):
		last_tL[x].append(-3.0)
		last_tR[x].append(-3.0)
	last_tL.append([])
	last_tR.append([])	


for evt in eventList:
	x = evt[1]-1
	y = evt[2]-1
 	t = evt[0]/1000.0
  	
 	lowerBoundX = (128 - dimRetX)/2
 	upperBoundX = (128 + dimRetX)/2
  	
 	lowerBoundY = (128 - dimRetY)/2
 	upperBoundY = (128 + dimRetY)/2
  	
	if lowerBoundX <= x < upperBoundX and lowerBoundY <= y < upperBoundY:
		if evt[4] == 0:
			if t - last_tR[x-lowerBoundX][y-lowerBoundY] > 3.0 and t <= initTime:
# 				print "r", x, y, x-lowerBoundX, y-lowerBoundY
				retinaR[x-lowerBoundX][y-lowerBoundY].append(t)
				last_tR[x-lowerBoundX][y-lowerBoundY] = t	
		elif evt[4] == 1:
			
			if t - last_tL[x-lowerBoundX][y-lowerBoundY] > 3.0 and t <= initTime:
# 				print "l", x, y, x-lowerBoundX, y-lowerBoundY
				retinaL[x-lowerBoundX][y-lowerBoundY].append(t)
				last_tL[x-lowerBoundX][y-lowerBoundY] = t
				
 	
 			
for y in range(0, dimRetX):
	for x in range(0, dimRetY):
		if retinaR[y][x] == []:
			retinaR[y][x].append(initTime)
		if retinaL[y][x] == []:
			retinaL[y][x].append(initTime) 
 
formatedL = retinaL#[list(x) for x in zip(*retinaL)]
formatedR = retinaR#[list(x) for x in zip(*retinaR)]
  	
cPickle.dump(formatedL, open('../realInput/retinaLeft_{0}x{1}_{2}.p'.format(dimRetX, dimRetY, experimentName), 'wb')) 	
cPickle.dump(formatedR, open('../realInput/retinaRight_{0}x{1}_{2}.p'.format(dimRetX, dimRetY, experimentName), 'wb')) 	
 
rL = cPickle.load(open('../realInput/retinaLeft_{0}x{1}_{2}.p'.format(dimRetX, dimRetY, experimentName), 'rb'))
print rL[16]