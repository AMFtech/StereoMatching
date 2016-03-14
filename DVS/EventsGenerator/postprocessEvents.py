
xOffset = 10

evts = []
with open('T.dat', 'r') as f:
    evts = [[int(x.split()[0]), int(x.split()[1]), int(x.split()[2]), int(x.split()[3]), int(x.split()[4])] for x in f.readlines()]
    

with open('T.dat', 'w') as f:    
    for e in evts:
        e[1] += xOffset
        f.write(str(e[0] + 50) + " " + str(e[1]) + " " + str(e[2]) + " " + str(e[3]) + " " + str(e[4]) + "\n")
