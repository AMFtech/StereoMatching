import cPickle    


fileName = "movingPersonFaraway.dat"
 
eventList = []
with open(fileName, 'rb') as allEvents:
    for line in allEvents:
        line = [int(x) for x in line.split()]
        eventList.append((float(line[0])/1000.0, line[1], line[2], line[4]))
         
# # print eventList
sortedEventList = sorted(eventList, key=lambda x: x[0])

dimRetX = 5
dimRetY = 120
initTime = 10000.0

croppedEventList = [(x[0], x[1]-(128 - dimRetX)/2, x[2]-(128 - dimRetX)/2, x[3]) for x in sortedEventList if (128 - dimRetX)/2 <= x[1] < (128 + dimRetX)/2 and (128 - dimRetX)/2 <= x[2] < (128 + dimRetX)/2]
 
timefilteredEventlist = [croppedEventList[0]]
prevSpike = croppedEventList[0]
for x in croppedEventList[1:]:
    if x[0] - prevSpike[0] > 0.9 or x[3] != prevSpike[3]:
        timefilteredEventlist.append(x)
    prevSpike = x
     
cPickle.dump(timefilteredEventlist, open('../realInput/timesorted_5_persAway.p', 'wb'))    

rL = cPickle.load(open('../realInput/timesorted_5_persAway.p', 'rb'))
print rL[2]