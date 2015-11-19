

def plotSimulationResults(network=None):
    
    assert network is not None, "Uninitialised network! Visualising failed."
    
    print "Nicely visualising results..."
    cellOut = network.get_population("Cell Output Population of Network")
    
    from pyNN.utility import normalized_filename
    filename = normalized_filename("Results", "cell_type_demonstration", "pkl", "nest")
    
    from pyNN.utility.plotting import Figure, Panel
    figure_filename = filename.replace("pkl", "png")
    Figure(
        Panel(cellOut.get_data().segments[0].filter(name='v')[0],
              ylabel="Membrane potential (mV)", xlabel="Time (ms)",
              data_labels=[cellOut.label], yticks=True, xticks=True, ylim=(-110, -40)),
           Panel(cellOut.get_data().segments[0].spiketrains,
              ylabel="Index", xlabel="Time (ms)",
              data_labels=[cellOut.label], yticks=True, xticks=True, ylim=(-110, -40)),
        title="Rearranged Cooperative Network",
        annotations="Simulated with NEST"
    ).save(figure_filename)