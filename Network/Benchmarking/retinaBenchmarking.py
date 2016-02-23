import cPickle

fileName = "../src/realInput/oneHand.dat"
 
eventList = []
with open(fileName, 'rb') as allEvents:
    for line in allEvents:
        line = [int(x) for x in line.split()]
        eventList.append((float(line[0])/1000.0, line[1], line[2], line[4]))
         
# # print eventList
sortedEventList = sorted(eventList, key=lambda x: x[0])

dimRet = 128

croppedEventList = [(x[0], x[1]-(128 - dimRet)/2, x[2]-(128 - dimRet)/2, x[3]) for x in sortedEventList if (128 - dimRet)/2 <= x[1] < (128 + dimRet)/2 and (128 - dimRet)/2 <= x[2] < (128 + dimRet)/2]
 
timefilteredEventlist = [croppedEventList[0]]
prevSpike = croppedEventList[0]
for x in croppedEventList[1:]:
    if x[0] - prevSpike[0] > 0.9 or x[3] != prevSpike[3]:
        timefilteredEventlist.append(x)
    prevSpike = x

evntsCount = [[]] 
sec = 0    
for x in timefilteredEventlist:
    if int(x[0] / 1000) == sec:
        evntsCount[sec].append(x[0])
    else:
        evntsCount.append([])
        sec += 1  
        
evntsCount = map(len, evntsCount)    
print evntsCount
print "total events count: ", sum(evntsCount)
print "max events count per sec", max(evntsCount)

    