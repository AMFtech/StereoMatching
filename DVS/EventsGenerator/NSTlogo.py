from pylab import *
import numpy
from numpy import vectorize
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
    
    letterOffset = (0, 1, 2)
    interval = 1.0/6.0
    scalingFactor = 1.0
    spacing = 0.1
    
    def xf(t):
        xval = 1.0
        # 1st segment |
        if 0*interval <= t < 1*interval:
            xval = 1.0
        # 2nd segment  \
        elif 1*interval <= t < 2*interval:
            xval = 1*t + 1.0 - interval
        # # # 3rd segment   |
        elif 2*interval <= t < 3*interval:
            xval = 1.0 + interval
        # # 4th segment     S
        elif 3*interval <= t < 4*interval:
            xval = 1.0 + interval + spacing - 0.08*sin(60*t + 10)
        # # 5th segment       |
        elif 4*interval <= t < 5*interval:
            xval = 1.0 + 3*interval
        # 6th segment         --
        else:
            xval = t + 0.6
#         print "xval", xval    
        return xval * scalingFactor        
       
    def yf(t):
        yval = 1.0
        # 1st segment |
        if 0*interval <= t < 1*interval:
            yval = t
        # 2nd segment  \
        elif 1*interval <= t < 2*interval:
            yval = -1*t + 2*interval
        # # 3rd segment   |
        elif 2*interval <= t < 3*interval:
            yval = t
        # 4th segment     S
        elif 3*interval <= t < 4*interval:
            yval = 2.5*t - 1.0
        # 5th segment       |
        elif 4*interval <= t < 5*interval:
            yval = t - interval
        # 6th segment         --
        else:
            yval = 4*interval    
        return yval * scalingFactor   
       
    def zf(t):
        zval = 1.0
        # 1st segment |
        if 0*interval <= t < 1*interval:
            zval = 1.0 
        # 2nd segment  \
        elif 1*interval <= t < 2*interval:
            zval = 1.0
        # # # 3rd segment   |
        elif 2*interval <= t < 3*interval:
            zval = 1.0
        # # 4th segment     S
        elif 3*interval <= t < 4*interval:
            zval = 2.0
        # # 5th segment       |
        elif 4*interval <= t < 5*interval:
            zval = 3.0
        # 6th segment         --
        else:
            zval = 3.0
        return zval * scalingFactor   
    
    vxf = vectorize(xf)
    vyf = vectorize(yf)
    vzf = vectorize(zf)
    
    zr = 0.005 # vscreen focal point z-distance
    dx = 0.1 # focal points x-offset
    T = arange(0,1.,0.001)
    
    # first: show trajectory in 3d
    figure(figsize=(10,10))
    ax3d = axes([0.1,0.6,0.3,0.3],projection = '3d')
    #   print shape(xf(T)),shape(yf(T)),shape(zf(T))
    
      
    ax3d.plot(vxf(T),vyf(T),vzf(T),label='trajectory',zdir='z')
    ax3d.set_xlabel("x")
    ax3d.set_ylabel("y")
    ax3d.set_zlabel("z")
    
    # next: show trajectorys on virtual screen (retina-pixel-array)
    xf_proj, yf_proj, xdisparity = project_to_vscreens(vxf,vyf,vzf,zr,dx)
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
    
    if isinstance(D, float):
        D = [D]*len(T)
    
        
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
    
    eventsFile = open('./NSTlogo.dat', 'w')
    
    dimX = dimY = 128
    
    minD = min([x for x in D])
    maxD = max([x for x in D])
    
    minXR = min([x[0] for x in Evs1])
    minY = min([x[1] for x in Evs1])
    
    maxXL = max([x[0] for x in Evs2])
    maxY = max([x[1] for x in Evs1])
    
    distX = abs(maxXL - minXR)
    distY = abs(maxY - minY)
    
    offset_minX = 0 - minXR
    offset_minY = 0 - minY
    
    
    maxTime_us = 1000000 
    for repetitions in range(0, 10):
    #       print "# right retina:"
          for t,(x,y) in zip(Ts1,Evs1):
    #         print t,x,y
              eventsFile.write(str(int(t * maxTime_us + repetitions * maxTime_us)) + " " + str(x+offset_minX + dimX/2 - distX/2) + " " + str(y+offset_minY + dimY/2 - distY/2) + " " + str(0) + " " + str(1) + "\n")
    #       print "#"
    #       print "# ------------------------------ #"
    #       print "# left retina"
          for t,(x,y) in zip(Ts2,Evs2):
    #         print t,x,y
              eventsFile.write(str(int(t * maxTime_us + repetitions * maxTime_us)) + " " + str(x+offset_minX + dimX/2 - distX/2) + " " + str(y+offset_minY + dimY/2 - distY/2) + " " + str(0) + " " + str(0) + "\n")
    
    print len(Ts1)
    eventsFile.close()
      
    print minXR, maxXL
    print minY, maxY   
    print minD, maxD
    print maxD/float(minD)
    
    show()
    
    
    
    
    
    
#     def xf(T):
#         xvals = numpy.zeros(shape=(len(T),1))
#         for t, ind in zip(T, range(0, len(T))):
#             # 1st segment |
#             if 0*interval <= t < 1*interval:
#                 xvals[ind] = 0.0
#             # 2nd segment  \
#             elif 1*interval <= t < 2*interval:
#                 xvals[ind] = t
#             # 3rd segment   |
#             elif 2*interval <= t < 3*interval:
#                 xvals[ind] = 2*interval
#             # 4th segment     S
#             elif 3*interval <= t < 4*interval:
#                 xvals[ind] = sin(t)
#             # 5th segment       |
#             elif 4*interval <= t < 5*interval:
#                 xvals[ind] = 4*interval
#             # 6th segment         --
#             else:
#                 xvals[ind] = t
#         return xvals        
#        
#     def yf(T):
#         yvals = numpy.zeros(shape=(len(T),1))
#         for t, ind in zip(T, range(0, len(T))):
#             # 1st segment |
#             if 0*interval <= t < 1*interval:
#                 yvals[ind] = t
#             # 2nd segment  \
#             elif 1*interval <= t < 2*interval:
#                 yvals[ind] = -1.0*t
#             # 3rd segment   |
#             elif 2*interval <= t < 3*interval:
#                 yvals[ind] = t
#             # 4th segment     S
#             elif 3*interval <= t < 4*interval:
#                 yvals[ind] = t
#             # 5th segment       |
#             elif 4*interval <= t < 5*interval:
#                 yvals[ind] = t
#             # 6th segment         --
#             else:
#                 yvals[ind] = 0.5 
#         return yvals    
#        
#     def zf(T):
#         zvals = numpy.zeros(shape=(len(T),1))
#         for t, ind in zip(T, range(0, len(T))):
#             # 1st segment |
#             if 0*interval <= t < 1*interval:
#                 zvals[ind] = 0.0 
#             # 2nd segment  \
#             elif 1*interval <= t < 2*interval:
#                 zvals[ind] = 0.0
#             # 3rd segment   |
#             elif 2*interval <= t < 3*interval:
#                 zvals[ind] = 0.0
#             # 4th segment     S
#             elif 3*interval <= t < 4*interval:
#                 zvals[ind] = 1.0
#             # 5th segment       |
#             elif 4*interval <= t < 5*interval:
#                 zvals[ind] = 2.0
#             # 6th segment         --
#             else:
#                 zvals[ind] = 2.0
#         return zvals    
          
