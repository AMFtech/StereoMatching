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
