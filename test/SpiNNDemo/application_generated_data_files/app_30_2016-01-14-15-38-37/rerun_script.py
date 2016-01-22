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
runtime = 1000
send_start_notification = True
reset_machine_on_start_up = False
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
placement_to_app_data_files = {(0, 0, 2, 'i1'): ['10.162.177.122_appData_0_0_2.dat'], (0, 11, 4, 'c1'): ['10.162.177.122_appData_0_11_4.dat'], (0, 11, 12, 'c5'): ['10.162.177.122_appData_0_11_12.dat'], (0, 0, 3, 'i2'): ['10.162.177.122_appData_0_0_3.dat'], (11, 0, 2, 'i4'): ['10.162.177.122_appData_11_0_2.dat'], (0, 11, 3, 'c1'): ['10.162.177.122_appData_0_11_3.dat'], (0, 11, 5, 'c2'): ['10.162.177.122_appData_0_11_5.dat'], (11, 0, 3, 'i5'): ['10.162.177.122_appData_11_0_3.dat'], (0, 0, 1, 'i0'): ['10.162.177.122_appData_0_0_1.dat'], (0, 11, 10, 'c4'): ['10.162.177.122_appData_0_11_10.dat'], (0, 11, 1, 'c0'): ['10.162.177.122_appData_0_11_1.dat'], (0, 11, 6, 'c2'): ['10.162.177.122_appData_0_11_6.dat'], (0, 11, 2, 'LiveSpikeReceiver'): ['10.162.177.122_appData_0_11_2.dat'], (0, 11, 11, 'c5'): ['10.162.177.122_appData_0_11_11.dat'], (0, 11, 9, 'c4'): ['10.162.177.122_appData_0_11_9.dat'], (11, 0, 4, 'c0'): ['10.162.177.122_appData_11_0_4.dat'], (11, 0, 1, 'i3'): ['10.162.177.122_appData_11_0_1.dat'], (0, 11, 7, 'c3'): ['10.162.177.122_appData_0_11_7.dat'], (0, 11, 8, 'c3'): ['10.162.177.122_appData_0_11_8.dat']}
verify = False
database_file_path = /home/dikov/git/StereoMatching/test/SpiNNDemo/application_generated_data_files/latest/input_output_database.db
wait_for_read_confirmation = True
app_folder = "/home/dikov/git/StereoMatching/test/SpiNNDemo/application_generated_data_files/latest"
processor_to_app_data_base_address = {(0, 0, 2, 'i1'): {'start_address': 1612972052, 'memory_used': 144, 'memory_written': 144}, (0, 11, 4, 'c1'): {'start_address': 1612972052, 'memory_used': 44424, 'memory_written': 4344}, (0, 11, 12, 'c5'): {'start_address': 1613016484, 'memory_used': 44424, 'memory_written': 4344}, (0, 11, 10, 'c4'): {'start_address': 1613060916, 'memory_used': 44424, 'memory_written': 4344}, (11, 0, 2, 'i4'): {'start_address': 1612972052, 'memory_used': 144, 'memory_written': 144}, (0, 0, 3, 'i2'): {'start_address': 1612972204, 'memory_used': 144, 'memory_written': 144}, (0, 11, 5, 'c2'): {'start_address': 1613105348, 'memory_used': 197632, 'memory_written': 17552}, (11, 0, 3, 'i5'): {'start_address': 1612972204, 'memory_used': 144, 'memory_written': 144}, (0, 0, 1, 'i0'): {'start_address': 1612972356, 'memory_used': 144, 'memory_written': 144}, (0, 11, 3, 'c1'): {'start_address': 1613302988, 'memory_used': 197632, 'memory_written': 17552}, (0, 11, 1, 'c0'): {'start_address': 1613500628, 'memory_used': 44424, 'memory_written': 4344}, (0, 11, 6, 'c2'): {'start_address': 1613545060, 'memory_used': 44424, 'memory_written': 4344}, (0, 11, 2, 'LiveSpikeReceiver'): {'start_address': 1613589492, 'memory_used': 144, 'memory_written': 144}, (0, 11, 11, 'c5'): {'start_address': 1613589644, 'memory_used': 197632, 'memory_written': 17552}, (0, 11, 9, 'c4'): {'start_address': 1613787284, 'memory_used': 197632, 'memory_written': 17552}, (11, 0, 1, 'i3'): {'start_address': 1612972356, 'memory_used': 144, 'memory_written': 144}, (11, 0, 4, 'c0'): {'start_address': 1612972508, 'memory_used': 197632, 'memory_written': 17552}, (0, 11, 7, 'c3'): {'start_address': 1613984924, 'memory_used': 197632, 'memory_written': 17552}, (0, 11, 8, 'c3'): {'start_address': 1614182564, 'memory_used': 44424, 'memory_written': 4344}}
scamp_connection_data = "None"
executable_targets = ExecutableTargets()
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 1)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 3)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 4)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 5)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 6)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 7)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 8)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 9)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 10)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 11)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 0, 11, 12)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/sPyNNaker/spynnaker/pyNN/model_binaries/IF_curr_exp.aplx", 11, 0, 4)
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 0, 0, 1)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 0, 0, 2)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 0, 0, 3)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 11, 0, 1)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 11, 0, 2)
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/reverse_iptag_multicast_source.aplx", 11, 0, 3)
executable_targets.add_binary(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/live_packet_gather.aplx")
executable_targets.add_processor(r"/home/dikov/SpiNNaker/spinn-dev-git_2016-01-11_11-12-05/dev/SpiNNFrontEndCommon/spinn_front_end_common/common_model_binaries/live_packet_gather.aplx", 0, 11, 2)
xml_paths = list()
iptags.append(
    IPTag("10.162.177.122", 1, "0.0.0.0", 17895, True)) 
iptags.append(
    IPTag("10.162.177.122", 0, "0.0.0.0", 17896, True)) 
reverse_iptags.append(ReverseIPTag("10.162.177.120", 2, 12004, 11, 0, 2)) 
reverse_iptags.append(ReverseIPTag("10.162.177.122", 2, 12001, 0, 0, 2)) 
reverse_iptags.append(ReverseIPTag("10.162.177.120", 4, 12002, 0, 0, 3)) 
reverse_iptags.append(ReverseIPTag("10.162.177.120", 6, 12005, 11, 0, 3)) 
reverse_iptags.append(ReverseIPTag("10.162.177.122", 5, 12000, 0, 0, 1)) 
reverse_iptags.append(ReverseIPTag("10.162.177.120", 0, 12003, 11, 0, 1)) 
reload_routing_table = ReloadRoutingTable()
routing_tables.add_routing_table(reload_routing_table.reload("picked_routing_table_for_0_11"))
reload_routing_table = ReloadRoutingTable()
routing_tables.add_routing_table(reload_routing_table.reload("picked_routing_table_for_0_0"))
reload_routing_table = ReloadRoutingTable()
routing_tables.add_routing_table(reload_routing_table.reload("picked_routing_table_for_11_0"))
socket_addresses.append(SocketAddress("localhost", 19996, None))
socket_addresses.append(SocketAddress("localhost", 19999, None))

reloader = Reload(machine_name, machine_version, reports_states, bmp_details, down_chips, down_cores, number_of_boards, height, width, auto_detect_bmp, enable_reinjection, xml_paths, scamp_connection_data,boot_port_num, placement_to_app_data_files, verify, routing_tables, processor_to_app_data_base_address, executable_targets, buffered_tags, iptags, reverse_iptags, buffered_placements, app_folder, wait_for_read_confirmation, socket_addresses, database_file_path, runtime, time_scale_factor,send_start_notification, reset_machine_on_start_up)
