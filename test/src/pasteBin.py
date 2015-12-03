#     # connect internally the AND-neurons in an outside function and not during creation
#     internalWeightInhibition = -39.5
#     internalDelayInhibition = 0.1
#     for layer in range(0, dy):
#         for row in range(0, dz):
#             for cell in range(0, dx):
#                 Projection(network[layer][row][cell].get_population("Inhibitor Left {0} - {1} - {2}".format(cell, layer, row)), 
#                         network[layer][row][cell].get_population("Cell Output {0} - {1} - {2}".format(cell, layer, row)),
#                         OneToOneConnector(), StaticSynapse(weight=internalWeightInhibition, delay=internalDelayInhibition))
#                 Projection(network[layer][row][cell].get_population("Inhibitor Right {0} - {1} - {2}".format(cell, layer, row)), 
#                         network[layer][row][cell].get_population("Cell Output {0} - {1} - {2}".format(cell, layer, row)),
#                         OneToOneConnector(), StaticSynapse(weight=internalWeightInhibition, delay=internalDelayInhibition))    
from itertools import repeat



########################33 plotter backup
#     filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
#     
#     retinaLeftMerged = retinaLeft[0][0]
#     retinaRightMerged = retinaRight[0][0]
#     
#     for layer in range(0, dimensionRetinaY):
#         for pixel in range(1, dimensionRetinaX):
#             retinaLeftMerged += retinaLeft[layer][pixel]
#             retinaRightMerged += retinaRight[layer][pixel]
#             
#     networkMerged = network[0][0][0]
#     for layer in range(0, dimensionRetinaY):
#         for row in range(disparityMin, disparityMax):
#             for pixel in range(1, dimensionRetinaX):
#                 networkMerged += network[layer][row][pixel]        
#             
# #     retinaLeftMerged.write_data(filename, annotations={'script_name': __file__})
#     
#     cellActivity =  network[1][1][1].get_population("Cell Output 2 - 2 - 2").get_data().segments[0]
#     cellInhLActivity = network[1][1][1].get_population("Inhibitor Left 2 - 2 - 2").get_data().segments[0]
#     cellInhRActivity = network[1][1][1].get_population("Inhibitor Right 2 - 2 - 2").get_data().segments[0]
#     retinaLeftActivity = retinaLeft[0][0].get_data().segments[0]
#     retinaRightActivity = retinaRight[0][0].get_data().segments[0]
#     
# #     print network[0][0][0].get_population("Cell Output 1 - 1 - 1")
#     imagelist
#     from pyNN.utility.plotting import Figure, Panel
#     figure_filename = filename.replace("pkl", "png")
#     Figure(Panel(cellActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
#            Panel(cellInhLActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
#            Panel(cellInhRActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
#            Panel(cellActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
#            Panel(retinaLeftActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
#            Panel(retinaRightActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True)).save(figure_filename)
#     print(figure_filename)

##############################



# import numpy as np
# import time
# import matplotlib
# matplotlib.use('GTKAgg')
# from matplotlib import pyplot as plt
# 
# 
# def randomwalk(dims=(256, 256), n=20, sigma=5, alpha=0.95, seed=1):
#     """ A simple random walk with memory """
# 
#     r, c = dims
#     gen = np.random.RandomState(seed)
#     pos = gen.rand(2, n) * ((r,), (c,))
#     old_delta = gen.randn(2, n) * sigma
# 
#     while True:
#         delta = (1. - alpha) * gen.randn(2, n) * sigma + alpha * old_delta
#         pos += delta
#         for ii in xrange(n):
#             if not (0. <= pos[0, ii] < r):
#                 pos[0, ii] = abs(pos[0, ii] % r)
#             if not (0. <= pos[1, ii] < c):
#                 pos[1, ii] = abs(pos[1, ii] % c)
#         old_delta = delta
#         yield pos
# 
# 
# def run(niter=1000, doblit=True):
#     """
#     Display the simulation using matplotlib, optionally using blit for speed
#     """
# 
#     fig, ax = plt.subplots(1, 1)
#     ax.set_aspect('equal')
#     ax.set_xlim(0, 255)
#     ax.set_ylim(0, 255)
#     ax.hold(True)
#     rw = randomwalk()
#     x, y = rw.next()
# 
#     plt.show(False)
#     plt.draw()
# 
#     if doblit:
#         # cache the background
#         background = fig.canvas.copy_from_bbox(ax.bbox)
# 
#     points = ax.plot(x, y, 'o')[0]
#     tic = time.time()
# 
#     for ii in xrange(niter):
# 
#         # update the xy data
#         x, y = rw.next()
#         points.set_data(x, y)
# 
#         if doblit:
#             # restore background
#             fig.canvas.restore_region(background)
# 
#             # redraw just the points
#             ax.draw_artist(points)
# 
#             # fill in the axes rectangle
#             fig.canvas.blit(ax.bbox)
# 
#         else:
#             # redraw everything
#             fig.canvas.draw()
# 
#     plt.close(fig)
#     print "Blit = %s, average FPS: %.2f" % (
#         str(doblit), niter / (time.time() - tic))
# 
# if __name__ == '__main__':
#     run(doblit=False)
#     run(doblit=True)


# import numpy as np
# import matplotlib.pyplot as plt
# 
# def f(x,y):
#     return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)
# 
# n = 10
# x = np.linspace(-3,3,3.5*n)
# y = np.linspace(-3,3,3.0*n)
# X,Y = np.meshgrid(x,y)
# Z = f(X,Y)
# print Z
# 
# plt.axes([0.025,0.025,0.95,0.95])
# plt.imshow(Z,interpolation='nearest', cmap='bone', origin='lower')
# plt.colorbar(shrink=.92)
# 
# plt.xticks([]), plt.yticks([])
# # savefig('../figures/imshow_ex.png', dpi=48)
# plt.show()
# from itertools import chain
# 
# lst = [ [[[1], [2], [3]], [[4], [5], [6]]], [[[7], [8], [9]], [[10], [11], [12]]] ]
# for rows in range(0, 2):
#         for colls in range(0, 2):
#             lst[rows][colls] = list(chain.from_iterable(lst[rows][colls]))
# #             lst[colls] = [list(t) for t in zip(*lst)]
# print lst
# 
# newlst = []
# for t in range(0,2):
#     elem = list(zip(*lst[t]))
#     elem = [list(e) for e in elem]
#     print elem
#     newlst.append(elem)
# 
# newlst2 = list(zip(*[list(e) for e in newlst]))
# 
# newlst2 = [list(e) for e in newlst2]
# print newlst2


# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import animation
#  
#  
# fig = plt.figure()
# data = np.array([[[-65.0, -65.0], [-65.0, -65.0]],
#     [[-65.0, -65.0], [-65.0, -65.0]],
#     [[-65.0 ,-65.0], [-65.0, -65.0]],
#     [[-57.828351311545966, -65.0], [-65.0, -65.0]],
#     [[-51.979056114739706, -65.0], [-65.0, -65.0]],
#     [[-102.0, -65.0], [-65.0, -65.0]],
#     [[-96.74140032786413, -65.0], [-65.0, -65.0]],
#     [[-65.33318615046791, -65.0], [-65.0, -64.99999999999999]],
#     [[-62.66515594431097, -65.0], [-65.0, -57.82835131154595]],
#     [[-60.48624485166279, -65.0], [-65.0, -51.97905611473969]],
#     [[-65.0, -65.0], [-65.0, -65.0]],
#     [[-65.0, -65.0], [-65.0, -65.0]],
#     [[-65.0, -65.0], [-65.0, -65.0]]], dtype='float')
# im = plt.imshow(data[3], cmap='gray', interpolation='none')
# plt.colorbar()
#  
# def init():
#     im.set_data([[0, 0], [0, 0]])
#  
# def animate(i):
#     im.set_data(data[i])
#     print data[i]
#     print i
#     return im
#   
# anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(data),
#                                interval=1000)
# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# from matplotlib.colors import LogNorm
# from matplotlib.ticker import MultipleLocator
# 
# s = {'t': 1,
#      'x': [1, 2, 3, 4, 5, 6, 7, 8],
#      'T': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
#      'D': [0.3, 0.5, 0.2, 0.3, 0.5, 0.5, 0.3, 0.4]}
# 
# width = 40
# 
# tot = np.repeat(s['D'],width).reshape(len(s['D']), width)
# tot2 = np.repeat(s['T'],width).reshape(len(s['D']), width)
# 
# fig, (ax1, ax2, ax3) = plt.subplots(1,3)
# 
# fig.suptitle('Title of figure', fontsize=20)
# 
# # Line plots
# ax1.set_title('Title of ax1')
# ax1.plot(s['x'], s['T'])
# ax1.set_ylim(0,1)
# 
# ax2.set_title('Title of ax2')
# ax2.plot(s['x'], s['D'])
# # Set locations of ticks on y-axis (at every multiple of 0.25)
# ax2.yaxis.set_major_locator(MultipleLocator(0.25))
# # Set locations of ticks on x-axis (at every multiple of 2)
# ax2.xaxis.set_major_locator(MultipleLocator(2))
# ax2.set_ylim(0,1)
# 
# ax3.set_title('Title of ax3')
# # Display image, `aspect='auto'` makes it fill the whole `axes` (ax3)
# im3 = ax3.imshow(tot, norm=LogNorm(vmin=0.001, vmax=1), aspect='auto')
# # Create divider for existing axes instance
# divider3 = make_axes_locatable(ax3)
# # Append axes to the right of ax3, with 20% width of ax3
# cax3 = divider3.append_axes("right", size="20%", pad=0.05)
# # Create colorbar in the appended axes
# # Tick locations can be set with the kwarg `ticks`
# # and the format of the ticklabels with kwarg `format`
# cbar3 = plt.colorbar(im3, cax=cax3, ticks=MultipleLocator(0.2), format="%.2f")
# # Remove xticks from ax3
# ax3.xaxis.set_visible(False)
# # Manually set ticklocations
# ax3.set_yticks([0.0, 2.5, 3.14, 4.0, 5.2, 7.0])
# 
# plt.tight_layout()
# # Make space for title
# plt.subplots_adjust(top=0.85)
# plt.show()



data = [[0,1,2,3],[4,5,6,7],[8,9,10],[11,12],[13]]

disp = 3
shiftGlob = 0
newdata = [[0],[1],[2],[3]]
for x in data[1:]:
    
    shiftGlob += 1
    shift = 0
#     print "--", x, shiftGlob
    
    for e in x:
        if (shift+1) % (disp+1) == 0:
            newdata.append([e])
        else:
            newdata[shift+shiftGlob].append(e)
        shift += 1    
            
    
print newdata





