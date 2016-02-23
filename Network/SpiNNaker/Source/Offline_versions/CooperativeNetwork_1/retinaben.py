from cPickle import load

retLeftSpikes = load(open('../src/realInput/retinaLeft_40x100_hand25.p', 'rb'))
retRightSpikes = load(open('../src/realInput/retinaRight_40x100_hand25.p', 'rb'))

cntL = 0
cntR = 0

evtcntdist = [0]*20
for yL, yR in zip(retLeftSpikes, retRightSpikes):
    for xL, xR in zip(yL, yR):
        for tL, tR in zip(xL, xR):
            if tL < 10000:
                evtcntdist[int(tL/500)] += 1
            if tR < 10000:
                evtcntdist[int(tR/500)] += 1
                

print evtcntdist
print sum(evtcntdist)