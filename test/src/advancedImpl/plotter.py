from pyNN.utility import normalized_filename
from network_parameters import dimensionRetinaX, dimensionRetinaY, disparityMin, disparityMax
# from pyNN.nest import *


def plotSimulationResults(network, retinaLeft, retinaRight):
    # plot results using pyNN plotting functions
    # TODO: replace with matplotlib & co. for finer tunning
    filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
    
    retinaLeftMerged = retinaLeft[0][0]
    retinaRightMerged = retinaRight[0][0]
    
    for layer in range(0, dimensionRetinaY):
        for pixel in range(1, dimensionRetinaX):
            retinaLeftMerged += retinaLeft[layer][pixel]
            retinaRightMerged += retinaRight[layer][pixel]
            
    networkMerged = network[0][0][0]
    for layer in range(0, dimensionRetinaY):
        for row in range(disparityMin, disparityMax):
            for pixel in range(1, dimensionRetinaX):
                networkMerged += network[layer][row][pixel]        
            
#     retinaLeftMerged.write_data(filename, annotations={'script_name': __file__})
    
    cellActivity =  network[1][1][1].get_population("Cell Output 2 - 2 - 2").get_data().segments[0]
    cellInhLActivity = network[1][1][1].get_population("Inhibitor Left 2 - 2 - 2").get_data().segments[0]
    cellInhRActivity = network[1][1][1].get_population("Inhibitor Right 2 - 2 - 2").get_data().segments[0]
    retinaLeftActivity = retinaLeft[0][0].get_data().segments[0]
    retinaRightActivity = retinaRight[0][0].get_data().segments[0]
    
#     print network[0][0][0].get_population("Cell Output 1 - 1 - 1")
    
    from pyNN.utility.plotting import Figure, Panel
    figure_filename = filename.replace("pkl", "png")
    Figure(Panel(cellActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
           Panel(cellInhLActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
           Panel(cellInhRActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True),
           Panel(cellActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
           Panel(retinaLeftActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
           Panel(retinaRightActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True)).save(figure_filename)
    print(figure_filename)



