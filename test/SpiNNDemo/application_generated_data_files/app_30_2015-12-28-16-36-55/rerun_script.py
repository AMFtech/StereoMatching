"""
general reload script - note that imports are required so don't remove them!
"""

# pacman imports
from pacman.model.placements.placements import Placements
from pacman.model.placements.placement import Placement
from pacman.model.routing_info.routing_info import RoutingInfo
from pacman.model.routing_info.subedge_routing_info import SubedgeRoutingInfo
from pacman.model.routing_tables.multicast_routing_tables import \
    MulticastRoutingTables
from pacman.model.tags.tags import Tags

# spinnman imports
from spinnman.model.core_subsets import CoreSubsets
from spinnman.model.core_subset import CoreSubset

# spinnmachine imports
from spinn_machine.tags.iptag import IPTag
from spinn_machine.tags.reverse_iptag import ReverseIPTag

# front end common imports
from spinn_front_end_common.utilities.report_states import ReportState
from spinn_front_end_common.utilities.reload.reload import Reload
from spinn_front_end_common.utilities.reload.reload_application_data \
    import ReloadApplicationData
from spinn_front_end_common.utilities.executable_targets \
    import ExecutableTargets
from spinn_front_end_common.utilities.reload.reload_routing_table import \
    ReloadRoutingTable
from spinn_front_end_common.utilities.reload.reload_buffered_vertex import \
    ReloadBufferedVertex
from spinn_front_end_common.utilities.notification_protocol.\
    socket_address import SocketAddress

# general imports
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
for handler in logging.root.handlers:
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)-15s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"))

application_data = list()
binaries = ExecutableTargets()
iptags = list()
reverse_iptags = list()
buffered_tags = Tags()
buffered_placements = Placements()

routing_tables = MulticastRoutingTables()
# database params
socket_addresses = list()

reports_states = ReportState(False, False, False, False, False,
                             False, False, False, False, False)
runtime = 10000
send_start_notification = True
time_scale_factor = 1
machine_name = "10.162.177.122"
machine_version = 5
bmp_details = "0;0;10.162.177.123/0,2,4"
down_chips = "None"
down_cores = "None"
number_of_boards = None
height = None
width = None
auto_detect_bmp = False
enable_reinjection = False
placements = dict()
boot_port_num = None
placement_to_app_data_files = {(0, 0, 2, 'spike_injector_backward'): ['10.162.177.122_appData_0_0_2.dat'], (0, 0, 4, 'pop_forward'): ['10.162.177.122_appData_0_0_4.dat'], (0, 0, 5, 'pop_backward'): ['10.162.177.122_appData_0_0_5.dat'], (0, 0, 3, 'LiveSpikeReceiver'): ['10.162.177.122_appData_0_0_3.dat'], (0, 0, 1, 'spike_injector_forward'): ['10.162.177.122_appData_0_0_1.dat']}
verify = False
database_file_path = /home/dikov/git/StereoMatching/test/SpiNNDemo/application_generated_data_files/latest/input_output_database.db
wait_for_read_confirmation = True
processor_to_app_data_base_address = {(0, 0, 2, 'spike_injector_backward'): {'start_address': 1613141192, 'memory_used': 132, 'memory_written': 132}, (0, 0, 4, 'pop_forward'): {'start_address': 1613141464, 'memory_used': 169028, 'memory_written': 9024}, (0, 0, 1, 'spike_injector_forward'): {'start_address': 1613141060, 'memory_used': 132, 'memory_written': 132}, (0, 0, 5, 'pop_backward'): {'start_address': 1612972032, 'memory_used': 169028, 'memory_written': 9024}, (0, 0, 3, 'LiveSpikeReceiver'): {'start_address': 1613141324, 'memory_used': 140, 'memory_written': 140}}
scamp_connection_data = "None"
executable_targets = ExecutableTargets()
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 0, 0, 1)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 0, 0, 2)
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/live_packet_gather.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/live_packet_gather.aplx", 0, 0, 3)
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 0, 4)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 0, 5)
xml_paths = list()
iptags.append(
    IPTag("10.162.177.122", 6, "0.0.0.0", 17895, True)) 
reverse_iptags.append(ReverseIPTag("10.162.177.122", 3, 12345, 0, 0, 2)) 
reverse_iptags.append(ReverseIPTag("10.162.177.122", 0, 12346, 0, 0, 1)) 
reload_routing_table = ReloadRoutingTable()
routing_tables.add_routing_table(reload_routing_table.reload("picked_routing_table_for_0_0"))
socket_addresses.append(SocketAddress("localhost", 19996, None))
socket_addresses.append(SocketAddress("localhost", 19999, None))

reloader = Reload(machine_name, machine_version, reports_states, bmp_details, down_chips, down_cores, number_of_boards, height, width, auto_detect_bmp, enable_reinjection, xml_paths, scamp_connection_data,boot_port_num, placement_to_app_data_files, verify, routing_tables, processor_to_app_data_base_address, executable_targets, buffered_tags, iptags, reverse_iptags, buffered_placements, wait_for_read_confirmation, socket_addresses, database_file_path, runtime, time_scale_factor,send_start_notification)
