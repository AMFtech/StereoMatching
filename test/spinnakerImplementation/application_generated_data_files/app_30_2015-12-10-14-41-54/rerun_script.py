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
runtime = 20.0
send_start_notification = True
time_scale_factor = 10.0
machine_name = "spin5b"
machine_version = 5
bmp_details = "None"
down_chips = "None"
down_cores = "None"
number_of_boards = None
height = None
width = None
auto_detect_bmp = False
enable_reinjection = True
placements = dict()
boot_port_num = None
placement_to_app_data_files = {(0, 0, 3, 'Blocker Left'): ['spin5b_appData_0_0_3.dat'], (0, 0, 2, 'Retina Right'): ['spin5b_appData_0_0_2.dat'], (0, 0, 5, 'Cell Output'): ['spin5b_appData_0_0_5.dat'], (0, 0, 4, 'Blocker Right'): ['spin5b_appData_0_0_4.dat'], (0, 0, 1, 'Retina Left'): ['spin5b_appData_0_0_1.dat']}
verify = False
database_file_path = None
wait_for_read_confirmation = True
processor_to_app_data_base_address = {(0, 0, 2, 'Retina Right'): {'start_address': 1612976356, 'memory_used': 144, 'memory_written': 132}, (0, 0, 3, 'Blocker Left'): {'start_address': 1612976500, 'memory_used': 2072, 'memory_written': 1268}, (0, 0, 5, 'Cell Output'): {'start_address': 1612972032, 'memory_used': 4168, 'memory_written': 3364}, (0, 0, 1, 'Retina Left'): {'start_address': 1612976200, 'memory_used': 156, 'memory_written': 132}, (0, 0, 4, 'Blocker Right'): {'start_address': 1612978572, 'memory_used': 2072, 'memory_written': 1268}}
scamp_connection_data = "None"
executable_targets = ExecutableTargets()
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 0, 0, 1)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 0, 0, 2)
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 0, 3)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 0, 4)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2015-11-25_15-40-54/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 0, 5)
xml_paths = list()
iptags.append(
    IPTag("10.162.242.32", 0, "0.0.0.0", 17896, True)) 
reload_routing_table = ReloadRoutingTable()
routing_tables.add_routing_table(reload_routing_table.reload("picked_routing_table_for_0_0"))
vertex = ReloadBufferedVertex("Retina Left:0:0", [(2, "Retina Left_0_0_2", 1048576) ])
buffered_placements.add_placement(Placement(vertex, 0, 0, 1))
buffered_tags.add_ip_tag(IPTag("10.162.242.32", 0, "0.0.0.0", 17896, True), vertex) 
vertex = ReloadBufferedVertex("Retina Right:0:0", [(2, "Retina Right_0_0_2", 1048576) ])
buffered_placements.add_placement(Placement(vertex, 0, 0, 2))
buffered_tags.add_ip_tag(IPTag("10.162.242.32", 0, "0.0.0.0", 17896, True), vertex) 

reloader = Reload(machine_name, machine_version, reports_states, bmp_details, down_chips, down_cores, number_of_boards, height, width, auto_detect_bmp, enable_reinjection, xml_paths, scamp_connection_data,boot_port_num, placement_to_app_data_files, verify, routing_tables, processor_to_app_data_base_address, executable_targets, buffered_tags, iptags, reverse_iptags, buffered_placements, wait_for_read_confirmation, socket_addresses, database_file_path, runtime, time_scale_factor,send_start_notification)
