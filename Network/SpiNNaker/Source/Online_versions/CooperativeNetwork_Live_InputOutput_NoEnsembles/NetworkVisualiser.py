from NetworkBuilder import sameDisparityInd, retinaNbhoodL
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, maxDisparity, minDisparity, simulationTime, \
    maxSpikeInjectorPopsPerRetina, maxSpikeInjectorNeuronsPerPop
from spynnaker_external_devices_plugin.pyNN.connections.spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection
import spynnaker_external_devices_plugin.pyNN as ExternalDevices
import time
import serial
import numpy as np
from threading import Thread, Timer
import sys
import pygame 

DVSXRES, DVSYRES = 128,128
retinaThreads = dict()
disparityThread = None
ports = [0,1]   #be careful which port is to the left and which to the right camera!!!
logFile = None

lowerBoundX = (DVSXRES-dimensionRetinaX)/2
upperBoundX = (DVSXRES+dimensionRetinaX)/2
lowerBoundY = (DVSYRES-dimensionRetinaY)/2
upperBoundY = (DVSYRES+dimensionRetinaY)/2

def setupVisualiser(network=None, retinaLeft=None, retinaRight=None):
    print "Setting up Visualiser..."
    global retinaThreads, disparityThread, logFile
    
    logFile = open("dipsarities_noinh.txt", 'w')
    
    print "\tSetting up Spike Receiver..."
    networkLabels = []
    for pop in network:
        ExternalDevices.activate_live_output_for(pop[1], database_notify_host="localhost", database_notify_port_num=19996)
        networkLabels.append(pop[1].label)
    
    liveConnection_receiver = SpynnakerLiveSpikesConnection(receive_labels=networkLabels, local_port=19996, send_labels=None) 
    
    disparityThread = spike_plotter()
    
    for label in networkLabels:
        liveConnection_receiver.add_receive_callback(label, disparityThread.plotReceivedSpike)
    
    disparityThread.start()
    
    print "\tSetting up Spike Injectors for Retina Left and Retina Right..."            
    retinaLabels = []
    for popL, popR in zip(retinaLeft, retinaRight):
        retinaLabels.append(popL[1].label)
        retinaLabels.append(popR[1].label)
      
    liveConnection_sender = SpynnakerLiveSpikesConnection(receive_labels=None, local_port=19999, send_labels=retinaLabels)
    bg_col=pygame.Color(230,230,230,0)
    on_col=pygame.Color(10,220,10,0)
    off_col=pygame.Color(220,10,10,0)
    retinaThreads[ports[0]] = dvs_reader(port=ports[0], colors = {"bg": bg_col, "on": on_col, "off": off_col}, label="RetL", liveConnection=liveConnection_sender)
    retinaThreads[ports[1]] = dvs_reader(port=ports[1], colors = {"bg": bg_col, "on": on_col, "off": off_col}, label="RetR", liveConnection=liveConnection_sender)
     
    liveConnection_sender.add_start_callback(retinaLabels[0], startInjecting)
    
    panelsDrawer = Thread(target=setupPanels)
    panelsDrawer.start()

def setupPanels():
    global ports, retinaThreads, disparityThread
    time_period = 20    # targeted duration of a single update cycle in ms
    half_time = 100. # targeted half time for after glow in ms
    decay_alpha = int(255. - 255.*(0.5)**(time_period/half_time)) # alpha of periodically blitted surface
#     print "setting alpha to",decay_alpha
    l=len(ports)
    
    pygame.init()
    colorset="rg"
    if colorset=="bw":
        bg_col=pygame.Color(230,230,230,0)
        on_col=pygame.Color(220,220,220,0)
        off_col=pygame.Color(36,36,36,0)
    if colorset=="rg":
        bg_col=pygame.Color(230,230,230,0)
        on_col=pygame.Color(10,220,10,0)
        off_col=pygame.Color(220,10,10,0)
    
    
    pygame.display.set_caption("2dvs live view")
    winsize=(DVSXRES*l+l+DVSXRES,DVSYRES)
    subsize=(DVSXRES,DVSYRES)
    fade_surface = pygame.Surface(subsize)
    outsurfs = [pygame.Surface(subsize) for i in range(0, l+1)]
    fade_surface.fill(bg_col)
    fade_surface.set_alpha(decay_alpha)
    videoflags=pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF
    screen=pygame.display.set_mode(winsize,videoflags)
    screen.fill(pygame.Color(255,0,0,0),rect=pygame.Rect(subsize[0],0,1,subsize[1])) # red separator
    screen.fill(pygame.Color(255,0,0,0),rect=pygame.Rect(2*subsize[0]+l,0,1,subsize[1])) # red separator
    pygame.event.set_allowed(None) # allow only the 2 event types we process:
    pygame.event.set_allowed([pygame.VIDEORESIZE,pygame.QUIT])
    
    retinaThreads[ports[0]].start()
    retinaThreads[ports[1]].start()
    
    buffill = [0]*(l+1)
    while not pygame.event.peek(pygame.QUIT):
        stime = pygame.time.get_ticks()
        if pygame.event.peek(pygame.VIDEORESIZE):
            """first check if we need to resize and act accordingly"""
            event = pygame.event.get(pygame.VIDEORESIZE)[0]
            winsize=event.dict['size']
            subsize=(winsize[0]/(l+1),winsize[1])
            screen=pygame.display.set_mode(winsize,videoflags) # adjust window size
            screen.fill(pygame.Color(255,0,0,0),rect=pygame.Rect(subsize[0],0,1,subsize[1])) # red separator
            screen.fill(pygame.Color(255,0,0,0),rect=pygame.Rect(2*subsize[0]+l,0,1,subsize[1])) # red separator
            outsurfs = [pygame.Surface(subsize) for i in range(0, l+1)] # the new output surfaces
            
        for j, p in enumerate(ports):
            """blit updated surfaces to screen"""
            cv=retinaThreads[p].cv
            screen.blit(pygame.transform.scale(cv,subsize,outsurfs[j]), (j*subsize[0]+j,0))
        screen.blit(pygame.transform.scale(disparityThread.cv,subsize,outsurfs[l]), (l*subsize[0]+l+1,0))
        
        # now show on screen:
        pygame.display.flip()
        for p in ports:
            """fade individual screens"""
            retinaThreads[p].cv.blit(fade_surface,(0,0))
        disparityThread.cv.blit(fade_surface,(0,0))    
        # and wait until our frame is over
        pygame.time.wait(time_period - (pygame.time.get_ticks() - stime))
        
    for p in ports:
        retinaThreads[p].stop = True
    disparityThread.stop = True

def startInjecting(label, liveConnection):
    global retinaThreads, ports
    for p in ports:
        print "\tActivating Spike Injector:", retinaThreads[p].label
        retinaThreads[p].startInjecting = True
#     testthr = Thread(target=testh, args=(liveConnection,))
#     testthr.start()    

def testh(sender):
    while True:
        print "seding one test at "
        print repr(time.time())
        sender.send_spike(label="RetL 0", neuron_id=1, send_full_keys=True)
        sender.send_spike(label="RetR 0", neuron_id=1, send_full_keys=True)
        print repr(time.time())
        time.sleep(1)
        
class dvs_reader(Thread):
  def __init__(self, address='/dev/ttyUSB', port=0, baudrate=4000000, buflen=64, colors=None, label=None, liveConnection=None):
    Thread.__init__(self)
    if colors == None:
        self.colors = { "on": pygame.Color(0,255,0,0), "off": pygame.Color(255,0,0,0), "bg": pygame.Color(0,0,0,0)}
    else:
        self.colors = colors
    self.liveConnection = liveConnection
    self.label = label
    self.cv = pygame.Surface((DVSXRES,DVSYRES))
    self.cv.fill(colors["bg"])
    self.onbuf = [(0,0)] * buflen
    self.offbuf = [(0,0)] * buflen
    self.tbuf = [0] * buflen
    self.buflen = buflen
    self.evind = 0
    self.port = port
    self.stop = False
    self.startInjecting = False
    self.alive = True
    self.setDaemon(True)
    self.timeArray = np.ones((DVSXRES,DVSYRES),dtype=np.uint32)
    sio = serial.serial_for_url(address+str(port), baudrate, rtscts=True, dsrdtr=True, timeout=1)
    self.dvsdev = sio
    self.dvs_init()

  def dvs_init(self):
      self.dvsdev.write("R\n")
      time.sleep(0.1)
      self.dvsdev.write("1\n")    # LEDs on
      self.dvsdev.write("!E0\n")    # no timestamps
      self.dvsdev.write("E+\n")   # enable event streaming
    
  def dvs_uninit(self):
      self.dvsdev.write("0\n")    # LED off
      self.dvsdev.write("E-\n")    # event streaming off

  def run(self):
        """read and interpret data from serial port"""
        colors = [ self.colors["off"], self.colors["on"] ]
        try:
            lastx = -1
            lasty = -1
            global lowerBoundX, lowerBoundY, upperBoundX, upperBoundY
            pixelColsPerInjectorPop = maxSpikeInjectorNeuronsPerPop/dimensionRetinaY
            while not self.stop:
#                self.bufbytes = self.dvsdev.inWaiting()
                data = bytearray(self.dvsdev.read(2))
                if (data[0] & 0x80) != 0:
                    x = data[0] & 0x7f
                    y = data[1] & 0x7f
                    p = data[1] >> 7
                    self.cv.set_at((x,DVSXRES-y),colors[p])
                    if lowerBoundX <= x < upperBoundX and lowerBoundY <= y < upperBoundY and self.startInjecting: 
                        if x != lastx or y != lasty:
                            injectorLabel = (x - lowerBoundX) / pixelColsPerInjectorPop
                            injectorNeuronID = (y - lowerBoundY) + ((x - lowerBoundX) % pixelColsPerInjectorPop) * dimensionRetinaY 
#                             print "sendin atr", x, injectorLabel, y, injectorNeuronID
                            self.liveConnection.send_spike(label="{0} {1}".format(self.label, injectorLabel), neuron_id=injectorNeuronID, send_full_keys=True)
                            lastx = x
                            lasty = y
                else:
                    self.dvsdev.read(1)                
            self.dvs_uninit()
            self.startInjecting = False
            
        except self.dvsdev.SerialException, e:
            self.alive = False
            self.dvs_uninit()
            print "something went wrong at port %i" % self.port
            print "disabling this thread."      
        

class spike_plotter(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.colors = { "on": pygame.Color(0,255,0,0), "off": pygame.Color(255,0,0,0), "bg": pygame.Color(0,0,0,0)}
        self.cv = pygame.Surface((DVSXRES,DVSYRES))
        self.cv.fill(self.colors["bg"])
        self.evind = 0
        self.stop = False
        self.alive = True
        self.setDaemon(True)
        self.timeArray = np.ones((DVSXRES,DVSYRES),dtype=np.uint32)
        
    def run(self):
        while not self.stop:
            pass 

    def plotReceivedSpike(self, label, time, neuronIDs):
        populationID = int([s for s in label.split()][1])
        global lowerBoundX, lowerBoundY, logFile
        for neuronID in neuronIDs:   
#             print "Received spike from ", label, neuronID 
            disp = minDisparity
            for d in range(0, maxDisparity+1):
                if populationID in sameDisparityInd[d]:
                    disp = d+minDisparity
                    break
#             print disp + minDisparity
            
            logFile.write(str(disp) + "\n")
            
            normalisedDisp = float(disp - minDisparity)/float(maxDisparity - minDisparity)
            gradientCol = (int(255*normalisedDisp), int(-255*normalisedDisp + 255)) #red and blue values
#             print gradientCol
            
            pixel = 0    
            for p in range(0, dimensionRetinaX):
                if populationID in retinaNbhoodL[p]:
                    pixel = p
                    break
#             print pixel, neuronID
            self.cv.set_at((lowerBoundX + pixel, lowerBoundY + neuronID), pygame.Color(gradientCol[0], 0, gradientCol[1], 0))
#             self.cv.set_at((lowerBoundX + pixel, lowerBoundY + neuronID), pygame.Color(0, 255, 0, 0))
            
                          