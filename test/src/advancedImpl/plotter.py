from pyNN.utility import normalized_filename


def plotSimulationResults(network, retinaLeft, retinaRight):
    # plot results using pyNN plotting functions
    # TODO: replace with matplotlib & co. for finer tunning
    filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
    network.write_data(filename, annotations={'script_name': __file__})
    retinaLeft.write_data(filename, annotations={'script_name': __file__})
    retinaRight.write_data(filename, annotations={'script_name': __file__})
    
    cellActivity = network.get_data().segments[0]
    retinaLeftActivity = retinaLeft.get_data().segments[0]
    retinaRightActivity = retinaRight.get_data().segments[0]
    
    from pyNN.utility.plotting import Figure, Panel
    figure_filename = filename.replace("pkl", "png")
    Figure(Panel(cellActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True), 
           Panel(cellActivity.filter(name='v')[0], ylabel="Membrane potential (mV)", yticks=True, ylim=(-66, -48)), 
           Panel(retinaLeftActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
           Panel(retinaRightActivity.spiketrains, xlabel="Time (ms)", xticks=True, yticks=True),
           title="Simple CoNet", annotations="Simulated with NEST").save(figure_filename)
    print(figure_filename)



