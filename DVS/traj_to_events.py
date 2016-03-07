#!/usr/bin/env python

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

def project_to_vscreens(fx,fy,fz,zr = 0.005, dx = 0.1):
  xproj = lambda t:zr/fz(t) * fx(t)
  yproj = lambda t:zr/fz(t) * fy(t)
  disparity = lambda t: zr/fz(t) * dx
  return xproj, yproj, disparity
  
def dvsify(fx,fy,T,vscreen_pixelsize=0.001):
  last_ev = (0,0)
  last_t = 0.
  Events = []
  Timestamps = []
  quant = lambda x:int(x/vscreen_pixelsize)
  quant2d = lambda x,y:(quant(x),quant(y))
  for t in T:
      next_ev = quant2d(fx(t),fy(t))
      if next_ev != last_ev:
        last_ev = next_ev        
        Events.append(last_ev)
        Timestamps.append(t)
  return Timestamps,Events
  
  
if __name__ == '__main__':
  om = 1.
  xf = lambda t: sin(2*pi/om * t)
  zf = lambda t: 1.2 + cos(2*pi/om * t)
  yf = lambda t: 1.0 * cos(2*pi/(om/2.) *t)

  zr = 0.005 # vscreen focal point z-distance
  dx = 0.1 # focal points x-offset
  T = arange(0,1.,0.001)
  
  # first: show trajectory in 3d
  figure(figsize=(10,10))
  ax3d = axes([0.1,0.6,0.3,0.3],projection = '3d')
#  print shape(xf(T)),shape(yf(T)),shape(zf(T))
  ax3d.plot(xf(T),yf(T),zf(T),label='trajectory',zdir='z')
  ax3d.set_xlabel("x")
  ax3d.set_ylabel("y")
  ax3d.set_zlabel("z")
  
  # next: show trajectorys on virtual screen (retina-pixel-array)
  xf_proj, yf_proj, xdisparity = project_to_vscreens(xf,yf,zf,zr,dx)
  ax2d = axes([0.6,0.6,0.3,0.3])
  X,Y,D = xf_proj(T),yf_proj(T),xdisparity(T)
  X1, X2 = X, X+D
  ax2d.plot(X1,Y)
  ax2d.plot(X2,Y)
  ax2d.set_xlabel("x")
  ax2d.set_ylabel("y")
  
  # now: plot individual traces for x1,x2,y
  axgraph = axes([0.1,0.1,0.8,0.3])
  axgraph.plot(T,X1,label='x1')
  axgraph.plot(T,X2,label='x2')
  axgraph.plot(T,D,label='d')
  axgraph.plot(T,Y,label='y')
  axgraph.legend(loc='best')
  axgraph.set_xlabel("time")
  axgraph.set_ylabel("space")
  
  # finally: superimpose events
  xf1_proj = xf_proj
  xf2_proj = lambda t: xf_proj(t) + xdisparity(t)
  
  Ts1,Evs1 = dvsify(xf1_proj,yf_proj,T,vscreen_pixelsize=0.0004) 
  Ts2,Evs2 = dvsify(xf2_proj,yf_proj,T,vscreen_pixelsize=0.0004)
  # Ts, Evs are the timestamps and event lists to feed into the network
  # Evs should be shifted, clipped to suit your input requirements
  # scaling works via setting lower vscreen_pixelsize above
  axgraph.plot(Ts1,X1[searchsorted(T,Ts1)],"bs",alpha=0.5)
  axgraph.plot(Ts2,X2[searchsorted(T,Ts2)],"go",alpha=0.5)
  
  Evs1,Evs2 = array(Evs1),array(Evs2)
  figure(figsize=(5,10))
  # those are the coodinates of our events
  axev = axes([0.1,0.6,0.8,0.3])
  axev.plot(Ts1,Evs1[::,0],"bs",alpha=0.5)
  axev.plot(Ts2,Evs2[::,0],"go",alpha=0.5)
  axev.set_xlabel("time")
  axev.set_ylabel("x (pixel)")
  
  axev3d = axes([0.1,0.1,0.8,0.3],projection='3d')
  axev3d.scatter(Evs1[:,0],Evs1[::,1],Ts1,color='b',alpha=0.5,zdir='z')
  axev3d.scatter(Evs2[:,0],Evs2[::,1],Ts2,color='g',alpha=0.5,zdir='z')
  axev3d.set_xlabel("x")
  axev3d.set_ylabel("y")
  axev3d.set_zlabel("t")

  print "# left retina:"  
  for t,(x,y) in zip(Ts1,Evs1):
    print t,x,y

  print "#"
  print "# ------------------------------ #"
  print "# right retina"
  for t,(x,y) in zip(Ts1,Evs1):
    print t,x,y
    
  show()
          
