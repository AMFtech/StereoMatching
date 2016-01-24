from NetworkBuilder import sameDisparityInd, retinaNbhoodL
from SimulationAndNetworkSettings import dimensionRetinaX, dimensionRetinaY, maxDisparity, minDisparity, simulationTime
from spynnaker_external_devices_plugin.pyNN.connections.spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection
import spynnaker_external_devices_plugin.pyNN as ExternalDevices

import time
import serial
import numpy as np
from threading import Thread, Timer
import sys

import pygame
retinaImg = []   
DVSXRES, DVSYRES = 128,128

def setupVisualiser(network=None):
    global retinaImg
    
    print "Setting up Visualiser..."
    for x in range(0, dimensionRetinaX):
        zeroList = []
        for y in range(0, dimensionRetinaY):    
            zeroList.append(0)
        retinaImg.append(zeroList)   
    
    panelsDrawer = Thread(target=setupPanels, args=(network,))
    panelsDrawer.start()

def setupPanels(network=None):
    
    time_period = 20    # targeted duration of a single update cycle in ms
    half_time = 100. # targeted half time for after glow in ms
    decay_alpha = int(255. - 255.*(0.5)**(time_period/half_time)) # alpha of periodically blitted surface
#     print "setting alpha to",decay_alpha
    ports = [1,0]
    l=len(ports)
    
    pygame.init()
    colorset="rg"
    if colorset=="bw":
        bg_col=pygame.Color(128,128,128,0)
        on_col=pygame.Color(220,220,220,0)
        off_col=pygame.Color(36,36,36,0)
    if colorset=="rg":
        bg_col=pygame.Color(0,0,0,0)
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
    
    retinaThreads = dict()
    for p in ports:
        retina = dvs_reader(port=p, colors = {"bg": bg_col, "on": on_col, "off": off_col})
        retinaThreads[p] = retina
        retina.start()
    
    disparityThread = spike_plotter(network=network)
    disparityThread.start()
    
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
#         print outsurfs
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
        
class dvs_reader(Thread):
  def __init__(self, address = '/dev/ttyUSB', port = 0, baudrate = 6000000, buflen = 64, colors = None):
    Thread.__init__(self)
    if colors == None:
      self.colors = { "on": pygame.Color(0,255,0,0), "off": pygame.Color(255,0,0,0), "bg": pygame.Color(0,0,0,0)}
    else:
      self.colors = colors
    self.cv = pygame.Surface((DVSXRES,DVSYRES))
    self.cv.fill(colors["bg"])
    self.onbuf = [(0,0)] * buflen
    self.offbuf = [(0,0)] * buflen
    self.tbuf = [0] * buflen
    self.buflen = buflen
    self.evind = 0
    self.port = port
    self.stop = False
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
            while not self.stop:
#                self.bufbytes = self.dvsdev.inWaiting()
                data = bytearray(self.dvsdev.read(2))
                if (data[0] & 0x80) != 0:
                    y = data[0] & 0x7f
                    x = data[1] & 0x7f
                    p = data[1] >> 7
                    self.cv.set_at((x,DVSXRES-y),colors[p])
                  # check time delta vs last spike of this pixel
#                  now = pygame.time.get_ticks()
#                  dt = now - self.timeArray[x,y]
#                  self.timeArray[x,y] = now
                  # or just the simple -not again- test:
#                  if x != lastx and y != lasty:
#                    sendEvent()
                else:
                    self.dvsdev.read(1)                
            self.dvs_uninit()
            
        except dvsdev.SerialException, e:
            self.alive = False
            self.dvs_uninit()
            print "something went wrong at port %i" % self.port
            print "disabling this thread."      
        

class spike_plotter(Thread):
    def __init__(self, network=None):
        Thread.__init__(self)
        self.colors = { "on": pygame.Color(0,255,0,0), "off": pygame.Color(255,0,0,0), "bg": pygame.Color(0,0,0,0)}
        self.cv = pygame.Surface((DVSXRES,DVSYRES))
        self.cv.fill(self.colors["bg"])
        self.evind = 0
        self.stop = False
        self.alive = True
        self.setDaemon(True)
        self.timeArray = np.ones((DVSXRES,DVSYRES),dtype=np.uint32)
        self.setupSpikeReceiver(network)
        
    def run(self):
        pass
       
    def setupSpikeReceiver(self, network=None):
        print "\tSetting up Spike Receiver..."
        networkLabels = []
        for pop in network:
            ExternalDevices.activate_live_output_for(pop[1], database_notify_host="localhost", database_notify_port_num=19996)
            networkLabels.append(pop[1].label)
           
        liveConnection = SpynnakerLiveSpikesConnection(receive_labels=networkLabels, local_port=19996, send_labels=None)   
        
        for label in networkLabels:
            liveConnection.add_receive_callback(label, self.plotReceivedSpike)    

    def plotReceivedSpike(self, label, time, neuronIDs):
        global retinaImg
        populationID = int([s for s in label.split()][1])
        for neuronID in neuronIDs:   
#             print "Received spike from ", label, neuronID 
            disp = minDisparity
            for d in range(0, maxDisparity+1):
                if populationID in sameDisparityInd[d]:
                    disp = d+minDisparity
                    break
        #     print "Detected disp: ", disp + minDisparity
            normalisedDisp = float(disp - minDisparity)/float(maxDisparity - minDisparity)
#             print "normalised disp", normalisedDisp
            gradientCol = (int(255*normalisedDisp), int(-255*normalisedDisp + 255))
#             print gradientCol
            pixel = 0    
            for p in range(0, dimensionRetinaX):
                if populationID in retinaNbhoodL[p]:
                    pixel = p
                    break
            self.cv.set_at((pixel, neuronID), pygame.Color(gradientCol[0], 0, gradientCol[1], 0))
            
                          