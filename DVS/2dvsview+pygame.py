#!/usr/bin/env python

import serial
import time
import numpy as np
from threading import Thread, Timer
import sys

import pygame

DVSXRES, DVSYRES = 128,128
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
    self.dvsdev.write("1\n")	# LEDs on
    self.dvsdev.write("!E0\n")	# no timestamps
    self.dvsdev.write("E+\n")   # enable event streaming
    
  def dvs_uninit(self):
    self.dvsdev.write("0\n")	# LED off
    self.dvsdev.write("E-\n")	# event streaming off

  def run(self):
        """read and interpret data from serial port"""
        colors = [ self.colors["off"], self.colors["on"] ]
        try:
            while not self.stop:
#                self.bufbytes = self.dvsdev.inWaiting()
                data = bytearray(self.dvsdev.read(2))
                if (data[0] & 0x80) != 0:
                  x = data[0] & 0x7f
                  y = data[1] & 0x7f
                  p = data[1] >> 7
                  self.cv.set_at((y,DVSYRES - x),colors[p])
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
      
      
if __name__ == "__main__":
  time_period = 20	# targeted duration of a single update cycle in ms
  half_time = 100. # targeted half time for after glow in ms
  decay_alpha = int(255. - 255.*(0.5)**(time_period/half_time)) # alpha of periodically blitted surface
  print "setting alpha to",decay_alpha
  ports = [0]
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
  winsize=(DVSXRES*l+l,DVSYRES)
  subsize=(DVSXRES,DVSYRES)
  fade_surface = pygame.Surface(subsize)
  outsurfs = [pygame.Surface(subsize) for i in ports]
  fade_surface.fill(bg_col)
  fade_surface.set_alpha(decay_alpha)
  videoflags=pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF
  screen=pygame.display.set_mode(winsize,videoflags)
  screen.fill(pygame.Color(255,0,0,0),rect=pygame.Rect(subsize[0],0,1,subsize[1])) # red separator
  pygame.event.set_allowed(None) # allow only the 2 event types we process:
  pygame.event.set_allowed([pygame.VIDEORESIZE,pygame.QUIT])

  threads=dict()
  for i,p in enumerate(ports):
    r = dvs_reader(port=p, colors = {"bg": bg_col, "on": on_col, "off": off_col})
    r.start()
    threads[p] = r

  buffill = [0]*l
  while not pygame.event.peek(pygame.QUIT):
    stime = pygame.time.get_ticks()
    if pygame.event.peek(pygame.VIDEORESIZE):
      """first check if we need to resize and act accordingly"""
      event = pygame.event.get(pygame.VIDEORESIZE)[0]
      winsize=event.dict['size']
      subsize=(winsize[0]/l,winsize[1])
      screen=pygame.display.set_mode(winsize,videoflags) # adjust window size
      screen.fill(pygame.Color(255,0,0,0),rect=pygame.Rect(subsize[0],0,1,subsize[1])) # red separator
      outsurfs = [pygame.Surface(subsize) for i in ports] # the new output surfaces
      
    for j, p in enumerate(ports):
      """blit updated surfaces to screen"""
      cv=threads[p].cv
      screen.blit(pygame.transform.scale(cv,subsize,outsurfs[j]), (j*subsize[0]+j,0))
    # now show on screen:
    pygame.display.flip()
    for p in ports:
      """fade individual screens"""
      threads[p].cv.blit(fade_surface,(0,0))
    # and wait until our frame is over
    pygame.time.wait(time_period - (pygame.time.get_ticks() - stime))
  
  for p in ports:
    threads[p].stop = True
         
