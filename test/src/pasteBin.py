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
#     
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


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

nx = 150
ny = 50

fig = plt.figure()
data = np.zeros((nx, ny))
im = plt.imshow(data, cmap='gist_gray_r', vmin=0, vmax=1)

def init():
    im.set_data(np.zeros((nx, ny)))

def animate(i):
    xi = i // ny
    yi = i % ny
    data[xi, yi] = 1
    im.set_data(data)
    return im

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=nx * ny,
                               interval=50)
plt.show()
